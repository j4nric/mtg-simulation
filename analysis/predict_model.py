"""Predicts 17Lands GIH WR of a new set from card features, trained on older sets.

Usage: python analysis/predict_model.py --features data/features.csv \
           --train EOE FIN TDM ... [--text] [--sim-weight W] [--predict TRK] [--out tierlist.csv]

The target is GIH WR standardised within each set (z-score), since only the
order inside one set matters and sets differ in overall win rate. Evaluation is
leave-one-set-out: each training set is predicted by a model fitted on the
others, and the Spearman correlation with the real values is reported.

With --sim-weight W, the blind simulation of a set (data/<set>_blind1/cards.csv,
see make_blind_rankings.py) is blended in: score = z(model) + W * z(sim GIH WR).
Few sets are simulated, so the simulation is blended in rather than learned as a feature.
"""
import argparse
import os

import lightgbm as lgb
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SIM_COLS = ["sim_gih", "sim_iwd", "sim_gp"]


def zscore(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std()


def real_target(code: str, min_n: int) -> pd.DataFrame:
    r = pd.read_csv(os.path.join(DATA, "17lands", f"{code.lower()}_real.csv"))
    r = r[r["GIH_n"] >= min_n].copy()
    r["card"] = r["card"].str.split(" // ").str[0]
    r["y"] = zscore(r["GIH_WR"])
    return r[["card", "y", "GIH_WR"]]


def sim_features(code: str, min_n: int = 10, shrink: int = 100) -> pd.DataFrame | None:
    """Simulated GIH WR z-scores, shrunk towards 0 by n / (n + shrink) for rarely seen cards."""
    path = os.path.join(DATA, f"{code.lower()}_blind1", "cards.csv")
    if not os.path.exists(path):
        return None
    s = pd.read_csv(path)
    s = s[s["GIH_n"] >= min_n].copy()
    s["card"] = s["card"].str.split(" // ").str[0]
    s["sim_gih"] = zscore(s["GIH_WR"]) * s["GIH_n"] / (s["GIH_n"] + shrink)
    s["sim_iwd"] = zscore(s["IWD"])
    s["sim_gp"] = zscore(s["GP_WR"])
    return s[["card"] + SIM_COLS]


def with_sim(df: pd.DataFrame, code: str) -> pd.DataFrame:
    s = sim_features(code)
    if s is None:
        df = df.copy()
        for c in SIM_COLS:
            df[c] = np.nan
        return df
    return df.merge(s, on="card", how="left")


def spearman(a, b) -> float:
    return pd.Series(a).rank().corr(pd.Series(b).rank())


class Model:
    """Average of a ridge regression and gradient-boosted trees."""

    def __init__(self, cols, text=False):
        self.cols = cols
        self.text = text

    def _ridge_X(self, X: pd.DataFrame):
        num = csr_matrix(self.scaler.transform(X[self.cols].fillna(0).values))
        if not self.text:
            return num
        return hstack([num, self.tfidf.transform(X["oracle"].fillna(""))]).tocsr()

    def fit(self, X: pd.DataFrame, y):
        self.scaler = StandardScaler().fit(X[self.cols].fillna(0).values)
        if self.text:
            # word 1-3-grams of rules text, e.g. "destroy target creature"
            self.tfidf = TfidfVectorizer(ngram_range=(1, 3), min_df=5, sublinear_tf=True)
            self.tfidf.fit(X["oracle"].fillna(""))
        self.ridge = Ridge(alpha=30).fit(self._ridge_X(X), y)
        self.gbm = lgb.LGBMRegressor(n_estimators=300, learning_rate=0.03, num_leaves=8,
                                     min_child_samples=20, subsample=0.8, subsample_freq=1,
                                     colsample_bytree=0.7, verbose=-1, random_state=1, n_jobs=1)
        self.gbm.fit(X[self.cols], y)
        return self

    def predict(self, X: pd.DataFrame, which="both"):
        r = self.ridge.predict(self._ridge_X(X))
        g = self.gbm.predict(X[self.cols])
        return {"ridge": r, "gbm": g, "both": (r + g) / 2}[which]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", default=os.path.join(DATA, "features.csv"))
    ap.add_argument("--train", nargs="+", required=True)
    ap.add_argument("--predict", default=None)
    ap.add_argument("--sim-weight", type=float, default=0.0,
                    help="blend in the blind simulation's GIH WR z-score with this weight")
    ap.add_argument("--text", action="store_true", help="add rules-text n-grams to the ridge model")
    ap.add_argument("--min-n", type=int, default=500, help="min 17Lands GIH games per card")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    feats = pd.read_csv(args.features)
    cols = [c for c in feats.columns if c not in ("card", "set", "oracle")]
    sets = {code: feats[feats["set"] == code].merge(real_target(code, args.min_n), on="card")
            for code in args.train}

    rows = []
    for code, test in sets.items():
        train = pd.concat([d for c, d in sets.items() if c != code])
        m = Model(cols, args.text).fit(train, train["y"])
        row = {"set": code, "cards": len(test), "rarity": spearman(test["rarity"], test["y"])}
        for w in ["ridge", "gbm", "both"]:
            row[w] = spearman(m.predict(test, w), test["y"])
        if args.sim_weight and sim_features(code) is not None:
            t = with_sim(test, code)
            row["sim_only"] = spearman(t["sim_gih"], t["y"])
            row["blend"] = spearman(blend(m.predict(t), t["sim_gih"], args.sim_weight), t["y"])
        rows.append(row)
    res = pd.DataFrame(rows)
    print("Leave-one-set-out Spearman with real GIH WR:")
    print(res.round(3).to_string(index=False))
    print("mean:", res.drop(columns=["set", "cards"]).mean().round(3).to_dict())

    if args.predict:
        train = pd.concat(sets.values())
        m = Model(cols, args.text).fit(train, train["y"])
        target = with_sim(feats[feats["set"] == args.predict], args.predict).copy()
        target["model"] = zscore(pd.Series(m.predict(target), index=target.index))
        target["score"] = blend(target["model"], target["sim_gih"], args.sim_weight)
        imp = pd.Series(m.gbm.booster_.feature_importance("gain"), index=cols)
        print("\nMost important features:", ", ".join(imp.sort_values(ascending=False).index[:12]))
        out = target[["card", "rarity", "model", "sim_gih", "score"]].sort_values("score", ascending=False)
        if args.out:
            out.to_csv(args.out, index=False, float_format="%.3f")
        print(out.head(30).to_string(index=False))


def blend(model_pred, sim_gih, weight: float) -> pd.Series:
    """Model prediction (as z-score) plus weight * simulated GIH WR z-score; 0 where unsimulated."""
    z = zscore(pd.Series(np.asarray(model_pred, dtype=float), index=sim_gih.index))
    return z + weight * sim_gih.fillna(0)


if __name__ == "__main__":
    main()
