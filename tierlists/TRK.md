# TRK: Tierliste (Vorhersage)

Erzeugt mit `analysis/predict_model.py` und `analysis/make_tierlist.py`.
Score = Modell aus Kartenwerten und Regeltext (gelernt an älteren Sets)
plus Forge-Simulation mit blindem Draft (Gewicht 1,0, 1.584 Partien). Höher ist besser; Einheit: Standardabweichungen
der erwarteten GIH WR innerhalb des Sets.

## Tier A (15 Karten)

| Karte | Farbe | Seltenheit | Score |
|---|---|---|---|
| Excalbian Gamemaster | W | M | 3.91 |
| U.S.S. Enterprise-A, Free Spirit | W | M | 3.82 |
| Borg Cube | WB | M | 3.41 |
| Captain Jean-Luc Picard | W | M | 3.29 |
| Hologram Stalker | G | U | 3.01 |
| Holo-Engineer | G | R | 2.88 |
| Captain James T. Kirk | R | M | 2.84 |
| Rok-Tahk, Budding Scientist | G | M | 2.82 |
| Captain Jonathan Archer | G | R | 2.36 |
| MACO Strike Team | G | R | 2.31 |
| Wesley Crusher, Starfleet Cadet | U | R | 2.21 |
| Georgiou, Terran Emperor | B | M | 2.17 |
| Salt Vampire | B | R | 2.14 |
| Species 8472 | G | U | 2.13 |
| Kobayashi Maru Scenario | U | M | 2.04 |

## Tier B (45 Karten)

| Karte | Farbe | Seltenheit | Score |
|---|---|---|---|
| U.S.S. Discovery, at Black Alert | G | R | 2.03 |
| Antagonist Incorporator | W | R | 1.97 |
| Crystalline Entity | farblos | M | 1.85 |
| Captain Benjamin Sisko | W | R | 1.81 |
| Neelix, Moral Support | G | U | 1.79 |
| The Measure of a Man | W | U | 1.73 |
| Armus, Skin of Evil | B | R | 1.71 |
| Miles O'Brien, Transporter Ops | W | R | 1.70 |
| The Inner Light | WG | R | 1.70 |
| Dr. Leonard "Bones" McCoy | G | R | 1.62 |
| Locutus, the One Who Speaks | WB | U | 1.62 |
| Ghost of Illyria | W | U | 1.52 |
| Mugato | G | U | 1.48 |
| Sela, Tal Shiar Paradox | B | R | 1.47 |
| Jake Sisko, War Correspondent | G | U | 1.35 |
| The City on the Edge of Forever | WB | R | 1.34 |
| Captain Kathryn Janeway | G | M | 1.34 |
| Amok Time | G | U | 1.34 |
| Seven of Nine, Unassimilated | U | M | 1.28 |
| Gwyndala, the Progeny | U | R | 1.28 |
| Nog, Ambitious Cadet | BG | R | 1.20 |
| The Wrath of Khan | R | R | 1.20 |
| The Unicomplex | farblos | R | 1.14 |
| Dathon, His Heart Open | URG | R | 1.13 |
| Romulan Bird-of-Prey | U | R | 1.11 |
| Daniels, Temporal Agent | BG | U | 1.11 |
| Khan, Vengeful Heart | B | M | 1.11 |
| Hemmer, Fixing What Is Broken | WU | U | 1.09 |
| Ni'Var Science Academy | farblos | R | 1.08 |
| Quark, Humble Proprietor | R | M | 1.08 |
| Assembly Specialist | W | U | 1.07 |
| Gul Dukat, Colonial Prefect | B | M | 1.06 |
| The Duras Sisters | BR | U | 1.00 |
| D-7 Battle Cruiser | R | R | 0.99 |
| Kira Nerys, Firebrand | WR | R | 0.99 |
| Temporal Conqueror | G | C | 0.97 |
| Rutherford, Upgraded Ensign | W | U | 0.96 |
| Jadzia Dax, Living Legacy | G | M | 0.95 |
| Lieutenant Commander Data | U | M | 0.95 |
| Dr. Beverly Crusher | W | M | 0.95 |
| Shuttle Ace | W | C | 0.93 |
| Blastoneuron | B | U | 0.92 |
| Sulu, Space Swashbuckler | W | R | 0.89 |
| Phlox, Unorthodox Doctor | WG | U | 0.88 |
| U.S.S. Excelsior, Cutting Edge | W | U | 0.87 |

## Tier C (89 Karten)

| Karte | Farbe | Seltenheit | Score |
|---|---|---|---|
| Gowron, Eager for Battle | BR | R | 0.84 |
| Vash, Freelance Archaeologist | BG | U | 0.83 |
| Subcommander T'Pol | U | R | 0.80 |
| Brad Boimler, Eager Ensign | W | U | 0.80 |
| Munitions Enthusiast | R | U | 0.78 |
| Q, Stacking the Deck | R | M | 0.78 |
| Adversary by Algorithm | G | U | 0.76 |
| Khaaaaaaaaaaaannn! | R | U | 0.76 |
| Q Continuum | farblos | R | 0.75 |
| In the Pale Moonlight | B | U | 0.74 |
| Collation Trimatrix | B | R | 0.71 |
| Elim Garak, Simple Tailor | B | R | 0.71 |
| Overflow Submatrix | B | R | 0.68 |
| Sarek, Federation Ambassador | WUG | R | 0.66 |
| Cleveland Booker, Empath | RG | U | 0.65 |
| Primary Unimatrix Adjunct | W | R | 0.65 |
| Spatial Anomaly | farblos | U | 0.64 |
| Saavik, Stoic Student | W | U | 0.62 |
| Command Subadjunct | W | U | 0.60 |
| Artificial Anomaly | farblos | U | 0.58 |
| The Destruction of Praxis | B | R | 0.58 |
| Cloak and Phaser | U | U | 0.57 |
| Set Phasers to . . . | W | C | 0.57 |
| Peace in Our Time | W | R | 0.56 |
| Moopsy | G | C | 0.53 |
| Subspace Anomaly | farblos | U | 0.51 |
| U.S.S. Reliant, From Hell's Heart | B | R | 0.50 |
| Federation Outpost | farblos | R | 0.47 |
| Sylvia Tilly, Joy of Discovery | G | U | 0.47 |
| Captain Pike, Fullness of Time | G | R | 0.47 |
| Deanna Troi, Psychic Counsel | W | R | 0.47 |
| Grand Nagus Zek | B | R | 0.45 |
| Dr. Joseph M'Benga | G | M | 0.44 |
| Impossible Choice | B | U | 0.42 |
| Emergency Medical Hologram | W | C | 0.40 |
| Dal R'El, Augment Orphan | RG | U | 0.39 |
| Syndicate Liquidators | G | U | 0.38 |
| 70,000 Light-Years from Home | W | U | 0.38 |
| All Good Things . . . | UG | R | 0.37 |
| Brazen Bluff | R | R | 0.36 |
| Encounter the Unknown | R | R | 0.33 |
| Scotty, Miracle Worker | U | M | 0.33 |
| Pah-Wraith | R | R | 0.33 |
| Resistance Is Futile | B | U | 0.32 |
| Quark's Bar | farblos | R | 0.30 |
| Deep Space 9 | farblos | M | 0.30 |
| Savvy Profiteer | R | C | 0.30 |
| Genesis Effect | R | C | 0.29 |
| Saurian Explorer | G | C | 0.28 |
| Test of Loyalty | B | U | 0.27 |
| Beckett Mariner, Impetuous Ensign | R | U | 0.27 |
| Cloistered Telepath | U | C | 0.26 |
| Spock, Always Your Friend | UR | U | 0.25 |
| L'Rell, Fierce Visionary | BR | U | 0.24 |
| Picard, Leading by Example | W | U | 0.23 |
| Eject the Warp Core | B | C | 0.21 |
| V'Ger, the Intruder | U | U | 0.19 |
| Worf, Intelligence Contractor | R | R | 0.19 |
| Una Chin-Riley, Number One | W | U | 0.18 |
| Test of Identity | R | U | 0.18 |
| Relentless Drednok | B | C | 0.16 |
| The Doctor, EMH | WG | U | 0.16 |
| Dominion Supervisor | G | C | 0.16 |
| Test of Conviction | W | U | 0.16 |
| Cold-Blooded Crew | G | C | 0.15 |
| Cha'DIch Investigator | B | C | 0.15 |
| Mr. Spock, Science Officer | U | M | 0.14 |
| Tasha Yar, Out of Time | R | R | 0.14 |
| David and Carol Marcus, Creators | G | U | 0.13 |
| U.S.S. Enterprise-D, Galaxy-Class | farblos | R | 0.12 |
| Khan, Despot by Design | R | U | 0.12 |
| The Caretaker | U | R | 0.12 |
| Photosynthetic Physician | G | C | 0.10 |
| Rogue Artificial Intelligence | B | C | 0.08 |
| Those Old Scientists | U | U | 0.08 |
| Will Riker, First in the Field | R | R | 0.07 |
| Command Decision | W | C | 0.07 |
| Planetary Bombardment | R | C | 0.06 |
| Interstellar Effigy | U | C | 0.06 |
| Bat'leth | B | U | 0.05 |
| Gaseous Anomaly | farblos | U | 0.04 |
| Commander Raffi Musiker | B | U | 0.03 |
| Temporal Anomaly | farblos | U | 0.02 |
| Jett Reno, Problem Solver | U | U | 0.00 |
| The Needs of the Many | W | R | -0.02 |
| Federation Field Medic | W | C | -0.03 |
| First Contact | G | C | -0.03 |
| Guidance Failure | U | C | -0.03 |
| Energize | U | U | -0.03 |

## Tier D (88 Karten)

| Karte | Farbe | Seltenheit | Score |
|---|---|---|---|
| Test of Priorities | U | U | -0.04 |
| Zero, Incorporeal Sensate | WB | U | -0.05 |
| Astute Terraformer | G | C | -0.06 |
| The Traveler | UG | U | -0.08 |
| Malfunctioning Holodeck | W | C | -0.09 |
| Fugitive Listener | B | C | -0.09 |
| Make It So | U | C | -0.10 |
| Vexing Drone | W | C | -0.10 |
| Melkotian Adjudicator | U | C | -0.13 |
| General Chang, Cold Warrior | B | R | -0.15 |
| Constable Odo | WU | U | -0.15 |
| Troubling Tribbles | W | R | -0.17 |
| Tenacious Drone | B | C | -0.20 |
| Dominion Assault Force | G | C | -0.20 |
| Targ Wrangler | R | U | -0.20 |
| Academy Instructor | R | U | -0.22 |
| Test of Courage | G | U | -0.24 |
| Captain Michael Burnham | R | U | -0.24 |
| Dr. McCoy, Surly Surgeon | W | U | -0.27 |
| Temple Garden | farblos | R | -0.27 |
| Dathon and Picard at El-Adrel | G | C | -0.28 |
| Hologram Janeway | W | U | -0.28 |
| Suurok-Class Science Vessel | U | C | -0.28 |
| Oberth-Class Starship | W | C | -0.29 |
| Xindi Surveyors | G | C | -0.29 |
| Hallowed Fountain | farblos | R | -0.30 |
| Federation Probe | U | C | -0.30 |
| Branching Timeline | G | R | -0.30 |
| Nyota Uhura, Communications | U | R | -0.31 |
| Storied Veteran | B | U | -0.31 |
| Sickbay | farblos | U | -0.32 |
| Cantankerous Captain | R | C | -0.32 |
| Free Borg Revolutionaries | W | C | -0.32 |
| Stomping Ground | farblos | R | -0.35 |
| Kai Winn, Faithless Leader | B | R | -0.36 |
| Kirk, Commanding Officer | WR | U | -0.39 |
| Tactical Officer | W | C | -0.40 |
| Lt. Cmdr. Geordi La Forge | U | R | -0.41 |
| Breeding Pool | farblos | R | -0.42 |
| Deep Space Scan | U | R | -0.43 |
| Andromedan Automatons | W | C | -0.44 |
| Perils of the Past | R | C | -0.45 |
| Federation Resupply | W | R | -0.45 |
| DOT-7 Repair Squad | W | C | -0.48 |
| Death Is Irrelevant | B | M | -0.49 |
| Consider the Prime Directive | U | C | -0.51 |
| Hoshi Sato, Exolinguist | U | U | -0.53 |
| Silicate Surveyor | R | C | -0.54 |
| De-evolve | B | U | -0.55 |
| Lwaxana Troi, Charming Guest | R | R | -0.55 |
| Starfleet Security | R | C | -0.56 |
| Humpback Whales | U | C | -0.57 |
| Shields Up! | W | C | -0.59 |
| Godless Shrine | farblos | R | -0.59 |
| Dominion Saboteur | U | U | -0.59 |
| Automated Warfare System | B | C | -0.61 |
| Ravenous Cosmozoan | R | U | -0.61 |
| I'm a Doctor, Not a . . . | G | C | -0.62 |
| Steam Vents | farblos | R | -0.63 |
| Rules of Acquisition | U | U | -0.64 |
| Tea, Earl Grey, Hot | farblos | C | -0.64 |
| Year of Hell | UR | R | -0.65 |
| Zefram Cochrane, Warp Pioneer | U | U | -0.66 |
| Infinite Diversity | R | M | -0.67 |
| Saru, Unthreatened | G | U | -0.67 |
| Xenobotanist | G | C | -0.68 |
| There's Coffee in that Nebula | W | U | -0.68 |
| Planetary Patrol | R | C | -0.70 |
| Boarding Action | R | C | -0.70 |
| Culber and Stamets, Star-Crossed | G | U | -0.71 |
| Starfleet Academy | farblos | M | -0.71 |
| Overgrown Tomb | farblos | R | -0.71 |
| Pet Sehlat | W | C | -0.72 |
| Stray from History | B | C | -0.73 |
| Live Long and Prosper | WU | R | -0.74 |
| Organic Avulsion Unit | B | U | -0.74 |
| Blood Crypt | farblos | R | -0.75 |
| Cybernetic Specialist | farblos | C | -0.75 |
| H.M.S. Bounty, Unlikely Timeship | U | R | -0.75 |
| Dahar Master | R | C | -0.76 |
| Horta | R | C | -0.78 |
| Lore, Positronic Provocateur | UB | U | -0.78 |
| Stable Wormhole | G | R | -0.80 |
| Engineered Explosives | farblos | R | -0.81 |
| He's Dead, Jim | B | C | -0.81 |
| Dominion Infiltration | R | R | -0.82 |
| Hive Mind Coprocessor | B | U | -0.82 |
| U.S.S. Voyager, Lone Wanderer | G | U | -0.83 |

## Tier F (59 Karten)

| Karte | Farbe | Seltenheit | Score |
|---|---|---|---|
| Gabriel Lorca, Mirror Menace | B | U | -0.85 |
| Sacred Foundry | farblos | R | -0.85 |
| Mirror Universe Intrusion | UB | R | -0.86 |
| D'Ghor Bloodletter | B | U | -0.87 |
| Cetacean Ops | U | C | -0.88 |
| Transporter Malfunction | R | U | -0.88 |
| U.S.S. Cerritos, Following Up | farblos | U | -0.90 |
| Replicator | farblos | R | -0.92 |
| Tal Shiar Operative | B | C | -0.95 |
| Vulcan Mind-Meld | U | U | -0.97 |
| La'An Noonien-Singh, Security | R | U | -0.97 |
| Data, New Life | U | U | -0.98 |
| Emergency Holographic Crew | U | C | -0.99 |
| Pure Energy | W | C | -0.99 |
| Battle-Scarred Survivalist | B | C | -1.04 |
| Highly Illogical | U | U | -1.04 |
| Collective Drone | B | U | -1.05 |
| Marooned | U | C | -1.08 |
| Enterprise NX-01 | U | U | -1.10 |
| Suus Mahna Practitioner | U | C | -1.11 |
| Tal Shiar Analyst | R | C | -1.11 |
| Common Goal | G | C | -1.11 |
| Ensign Pavel Chekov | U | U | -1.11 |
| Genesis Device | G | R | -1.12 |
| A Good Day to Die | B | C | -1.12 |
| Obsidian Order Operative | B | C | -1.16 |
| Open Communications | U | C | -1.16 |
| Sarcophagus, Ship of the Dead | R | U | -1.17 |
| Support Mission | G | U | -1.17 |
| Starfleet Spanner Jockey | U | C | -1.24 |
| Conquest Mission | W | U | -1.26 |
| Gray and Adira, Forever Joined | UR | U | -1.26 |
| Plasma Cascade | R | C | -1.27 |
| Watery Grave | farblos | R | -1.35 |
| Class-F Shuttlecraft | farblos | C | -1.44 |
| Warp Speed | G | U | -1.44 |
| D'Vana Tendi, Optimistic Ensign | UG | U | -1.48 |
| Hit It! | RG | R | -1.48 |
| Assault Drone | B | C | -1.49 |
| Seven of Nine | UB | U | -1.51 |
| Erica Ortegas, Plucky Pilot | R | U | -1.51 |
| Red Alert! | R | U | -1.57 |
| Isolinear Processor | farblos | U | -1.61 |
| Unexplored Territory | farblos | C | -1.61 |
| Anthropological Mission | U | U | -1.79 |
| The Naked Time | R | U | -1.80 |
| Warp Core | farblos | C | -1.89 |
| Pattern Buffer Preservation | B | C | -2.00 |
| Final Frontier | G | C | -2.00 |
| Captain's Tutelage | R | C | -2.11 |
| Reckless Impulse | R | C | -2.11 |
| Tricorder | farblos | C | -2.13 |
| Type-2 Phaser | farblos | U | -2.16 |
| Tell Me What You See | B | U | -2.32 |
| Vengeance Mission | B | U | -2.32 |
| Worf, Honor-Bound Warrior | WR | U | -2.33 |
| Exploratory Mission | R | U | -2.38 |
| The Holodeck | farblos | R | -2.43 |
| Combadge | farblos | U | -3.29 |
