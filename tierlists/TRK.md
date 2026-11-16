# TRK: Tierliste (Vorhersage)

Erzeugt mit `analysis/predict_model.py` und `analysis/make_tierlist.py`.
Score = Modell aus Kartenwerten und Regeltext (gelernt an älteren Sets)
plus Forge-Simulation mit blindem Draft. Höher ist besser; Einheit: Standardabweichungen
der erwarteten GIH WR innerhalb des Sets.

## Tier A (15 Karten)

| Karte | Farbe | Seltenheit | Score |
|---|---|---|---|
| Excalbian Gamemaster | W | M | 3.82 |
| U.S.S. Enterprise-A, Free Spirit | W | M | 3.72 |
| Borg Cube | WB | M | 3.37 |
| Captain Jean-Luc Picard | W | M | 2.99 |
| Captain James T. Kirk | R | M | 2.92 |
| Hologram Stalker | G | U | 2.89 |
| Holo-Engineer | G | R | 2.76 |
| Rok-Tahk, Budding Scientist | G | M | 2.72 |
| MACO Strike Team | G | R | 2.32 |
| Wesley Crusher, Starfleet Cadet | U | R | 2.29 |
| Captain Jonathan Archer | G | R | 2.27 |
| Kobayashi Maru Scenario | U | M | 2.14 |
| Georgiou, Terran Emperor | B | M | 2.09 |
| Salt Vampire | B | R | 2.09 |
| Species 8472 | G | U | 1.94 |

## Tier B (45 Karten)

| Karte | Farbe | Seltenheit | Score |
|---|---|---|---|
| Crystalline Entity | farblos | M | 1.90 |
| U.S.S. Discovery, at Black Alert | G | R | 1.81 |
| Captain Benjamin Sisko | W | R | 1.81 |
| Antagonist Incorporator | W | R | 1.80 |
| Miles O'Brien, Transporter Ops | W | R | 1.76 |
| Armus, Skin of Evil | B | R | 1.75 |
| The Inner Light | WG | R | 1.67 |
| Dr. Leonard "Bones" McCoy | G | R | 1.63 |
| The Measure of a Man | W | U | 1.58 |
| Neelix, Moral Support | G | U | 1.58 |
| Sela, Tal Shiar Paradox | B | R | 1.46 |
| Locutus, the One Who Speaks | WB | U | 1.43 |
| Seven of Nine, Unassimilated | U | M | 1.37 |
| Gwyndala, the Progeny | U | R | 1.37 |
| The City on the Edge of Forever | WB | R | 1.35 |
| Ghost of Illyria | W | U | 1.34 |
| Mugato | G | U | 1.32 |
| Amok Time | G | U | 1.29 |
| Captain Kathryn Janeway | G | M | 1.28 |
| Gul Dukat, Colonial Prefect | B | M | 1.19 |
| Romulan Bird-of-Prey | U | R | 1.18 |
| The Wrath of Khan | R | R | 1.15 |
| The Unicomplex | farblos | R | 1.14 |
| Jake Sisko, War Correspondent | G | U | 1.14 |
| Dathon, His Heart Open | URG | R | 1.13 |
| Daniels, Temporal Agent | BG | U | 1.12 |
| D-7 Battle Cruiser | R | R | 1.12 |
| Blastoneuron | B | U | 1.11 |
| Nog, Ambitious Cadet | BG | R | 1.10 |
| Khan, Vengeful Heart | B | M | 1.09 |
| Quark, Humble Proprietor | R | M | 1.09 |
| Hemmer, Fixing What Is Broken | WU | U | 1.04 |
| Assembly Specialist | W | U | 1.03 |
| Lieutenant Commander Data | U | M | 0.99 |
| Ni'Var Science Academy | farblos | R | 0.98 |
| Kira Nerys, Firebrand | WR | R | 0.94 |
| Jadzia Dax, Living Legacy | G | M | 0.91 |
| Sulu, Space Swashbuckler | W | R | 0.85 |
| The Duras Sisters | BR | U | 0.85 |
| Subcommander T'Pol | U | R | 0.83 |
| Q, Stacking the Deck | R | M | 0.80 |
| Dr. Beverly Crusher | W | M | 0.79 |
| Temporal Conqueror | G | C | 0.79 |
| Munitions Enthusiast | R | U | 0.77 |
| Rutherford, Upgraded Ensign | W | U | 0.74 |

## Tier C (89 Karten)

| Karte | Farbe | Seltenheit | Score |
|---|---|---|---|
| U.S.S. Excelsior, Cutting Edge | W | U | 0.73 |
| Spatial Anomaly | farblos | U | 0.70 |
| Vash, Freelance Archaeologist | BG | U | 0.70 |
| The Destruction of Praxis | B | R | 0.69 |
| Collation Trimatrix | B | R | 0.69 |
| Brad Boimler, Eager Ensign | W | U | 0.68 |
| Sarek, Federation Ambassador | WUG | R | 0.66 |
| Cloak and Phaser | U | U | 0.66 |
| Elim Garak, Simple Tailor | B | R | 0.66 |
| Overflow Submatrix | B | R | 0.66 |
| Saavik, Stoic Student | W | U | 0.65 |
| Gowron, Eager for Battle | BR | R | 0.64 |
| Shuttle Ace | W | C | 0.64 |
| Q Continuum | farblos | R | 0.63 |
| In the Pale Moonlight | B | U | 0.63 |
| Phlox, Unorthodox Doctor | WG | U | 0.62 |
| Cleveland Booker, Empath | RG | U | 0.61 |
| U.S.S. Reliant, From Hell's Heart | B | R | 0.59 |
| Primary Unimatrix Adjunct | W | R | 0.59 |
| Khaaaaaaaaaaaannn! | R | U | 0.59 |
| Grand Nagus Zek | B | R | 0.55 |
| Adversary by Algorithm | G | U | 0.54 |
| Impossible Choice | B | U | 0.53 |
| Artificial Anomaly | farblos | U | 0.53 |
| Set Phasers to . . . | W | C | 0.52 |
| Federation Outpost | farblos | R | 0.49 |
| Subspace Anomaly | farblos | U | 0.49 |
| All Good Things . . . | UG | R | 0.49 |
| Command Subadjunct | W | U | 0.47 |
| Dr. Joseph M'Benga | G | M | 0.44 |
| Moopsy | G | C | 0.41 |
| Sylvia Tilly, Joy of Discovery | G | U | 0.41 |
| Brazen Bluff | R | R | 0.36 |
| Genesis Effect | R | C | 0.35 |
| Deanna Troi, Psychic Counsel | W | R | 0.35 |
| Cloistered Telepath | U | C | 0.34 |
| Saurian Explorer | G | C | 0.33 |
| Syndicate Liquidators | G | U | 0.33 |
| Quark's Bar | farblos | R | 0.31 |
| 70,000 Light-Years from Home | W | U | 0.31 |
| Scotty, Miracle Worker | U | M | 0.31 |
| Emergency Medical Hologram | W | C | 0.31 |
| Pah-Wraith | R | R | 0.31 |
| Captain Pike, Fullness of Time | G | R | 0.27 |
| Deep Space 9 | farblos | M | 0.27 |
| Encounter the Unknown | R | R | 0.26 |
| The Caretaker | U | R | 0.25 |
| Mr. Spock, Science Officer | U | M | 0.24 |
| Dal R'El, Augment Orphan | RG | U | 0.20 |
| Eject the Warp Core | B | C | 0.19 |
| U.S.S. Enterprise-D, Galaxy-Class | farblos | R | 0.17 |
| Dominion Supervisor | G | C | 0.17 |
| Test of Loyalty | B | U | 0.17 |
| V'Ger, the Intruder | U | U | 0.16 |
| L'Rell, Fierce Visionary | BR | U | 0.16 |
| Spock, Always Your Friend | UR | U | 0.16 |
| David and Carol Marcus, Creators | G | U | 0.15 |
| Resistance Is Futile | B | U | 0.13 |
| Rogue Artificial Intelligence | B | C | 0.13 |
| Interstellar Effigy | U | C | 0.13 |
| Worf, Intelligence Contractor | R | R | 0.13 |
| Test of Priorities | U | U | 0.13 |
| Savvy Profiteer | R | C | 0.12 |
| Jett Reno, Problem Solver | U | U | 0.11 |
| Beckett Mariner, Impetuous Ensign | R | U | 0.11 |
| Relentless Drednok | B | C | 0.11 |
| Those Old Scientists | U | U | 0.10 |
| Photosynthetic Physician | G | C | 0.10 |
| Tasha Yar, Out of Time | R | R | 0.09 |
| Test of Identity | R | U | 0.08 |
| Cha'DIch Investigator | B | C | 0.08 |
| Peace in Our Time | W | R | 0.07 |
| Picard, Leading by Example | W | U | 0.05 |
| Gaseous Anomaly | farblos | U | 0.04 |
| Energize | U | U | 0.04 |
| First Contact | G | C | 0.03 |
| Command Decision | W | C | 0.03 |
| Cold-Blooded Crew | G | C | 0.02 |
| The Doctor, EMH | WG | U | 0.02 |
| Khan, Despot by Design | R | U | 0.02 |
| Commander Raffi Musiker | B | U | -0.01 |
| Will Riker, First in the Field | R | R | -0.01 |
| Guidance Failure | U | C | -0.01 |
| Test of Conviction | W | U | -0.02 |
| Planetary Bombardment | R | C | -0.02 |
| Bat'leth | B | U | -0.04 |
| Temporal Anomaly | farblos | U | -0.05 |
| Una Chin-Riley, Number One | W | U | -0.05 |
| The Needs of the Many | W | R | -0.06 |

## Tier D (88 Karten)

| Karte | Farbe | Seltenheit | Score |
|---|---|---|---|
| Zero, Incorporeal Sensate | WB | U | -0.06 |
| The Traveler | UG | U | -0.08 |
| Federation Field Medic | W | C | -0.09 |
| Malfunctioning Holodeck | W | C | -0.09 |
| Make It So | U | C | -0.10 |
| Nyota Uhura, Communications | U | R | -0.10 |
| Tenacious Drone | B | C | -0.11 |
| Constable Odo | WU | U | -0.11 |
| Astute Terraformer | G | C | -0.12 |
| Fugitive Listener | B | C | -0.14 |
| General Chang, Cold Warrior | B | R | -0.15 |
| Academy Instructor | R | U | -0.15 |
| Test of Courage | G | U | -0.16 |
| Troubling Tribbles | W | R | -0.16 |
| Vexing Drone | W | C | -0.17 |
| Branching Timeline | G | R | -0.18 |
| Federation Probe | U | C | -0.18 |
| Melkotian Adjudicator | U | C | -0.18 |
| Kai Winn, Faithless Leader | B | R | -0.21 |
| Targ Wrangler | R | U | -0.22 |
| Captain Michael Burnham | R | U | -0.22 |
| Dathon and Picard at El-Adrel | G | C | -0.24 |
| Storied Veteran | B | U | -0.25 |
| Dr. McCoy, Surly Surgeon | W | U | -0.25 |
| Dominion Assault Force | G | C | -0.25 |
| Suurok-Class Science Vessel | U | C | -0.28 |
| Oberth-Class Starship | W | C | -0.29 |
| Hologram Janeway | W | U | -0.34 |
| Temple Garden | farblos | R | -0.35 |
| Kirk, Commanding Officer | WR | U | -0.35 |
| Hallowed Fountain | farblos | R | -0.37 |
| Free Borg Revolutionaries | W | C | -0.37 |
| Xindi Surveyors | G | C | -0.39 |
| Stomping Ground | farblos | R | -0.40 |
| Deep Space Scan | U | R | -0.41 |
| Lt. Cmdr. Geordi La Forge | U | R | -0.43 |
| Hoshi Sato, Exolinguist | U | U | -0.44 |
| Breeding Pool | farblos | R | -0.45 |
| Tactical Officer | W | C | -0.45 |
| Perils of the Past | R | C | -0.47 |
| Federation Resupply | W | R | -0.48 |
| Cantankerous Captain | R | C | -0.48 |
| Rules of Acquisition | U | U | -0.48 |
| Saru, Unthreatened | G | U | -0.49 |
| Consider the Prime Directive | U | C | -0.49 |
| Sickbay | farblos | U | -0.49 |
| Andromedan Automatons | W | C | -0.50 |
| De-evolve | B | U | -0.51 |
| Lwaxana Troi, Charming Guest | R | R | -0.52 |
| Godless Shrine | farblos | R | -0.57 |
| H.M.S. Bounty, Unlikely Timeship | U | R | -0.57 |
| Humpback Whales | U | C | -0.59 |
| Steam Vents | farblos | R | -0.60 |
| Automated Warfare System | B | C | -0.61 |
| Shields Up! | W | C | -0.61 |
| Starfleet Security | R | C | -0.61 |
| Live Long and Prosper | WU | R | -0.62 |
| There's Coffee in that Nebula | W | U | -0.62 |
| I'm a Doctor, Not a . . . | G | C | -0.62 |
| Death Is Irrelevant | B | M | -0.63 |
| Dominion Saboteur | U | U | -0.63 |
| Infinite Diversity | R | M | -0.64 |
| Year of Hell | UR | R | -0.64 |
| Xenobotanist | G | C | -0.66 |
| DOT-7 Repair Squad | W | C | -0.66 |
| Overgrown Tomb | farblos | R | -0.66 |
| Starfleet Academy | farblos | M | -0.67 |
| He's Dead, Jim | B | C | -0.67 |
| Tea, Earl Grey, Hot | farblos | C | -0.67 |
| Silicate Surveyor | R | C | -0.67 |
| Boarding Action | R | C | -0.67 |
| Blood Crypt | farblos | R | -0.68 |
| Ravenous Cosmozoan | R | U | -0.71 |
| Culber and Stamets, Star-Crossed | G | U | -0.72 |
| Zefram Cochrane, Warp Pioneer | U | U | -0.72 |
| Stray from History | B | C | -0.73 |
| U.S.S. Voyager, Lone Wanderer | G | U | -0.74 |
| Replicator | farblos | R | -0.74 |
| Mirror Universe Intrusion | UB | R | -0.74 |
| Lore, Positronic Provocateur | UB | U | -0.74 |
| Sacred Foundry | farblos | R | -0.75 |
| D'Ghor Bloodletter | B | U | -0.76 |
| Planetary Patrol | R | C | -0.76 |
| Stable Wormhole | G | R | -0.78 |
| Pet Sehlat | W | C | -0.79 |
| Organic Avulsion Unit | B | U | -0.79 |
| Dahar Master | R | C | -0.79 |
| Cetacean Ops | U | C | -0.79 |

## Tier F (59 Karten)

| Karte | Farbe | Seltenheit | Score |
|---|---|---|---|
| Tal Shiar Operative | B | C | -0.79 |
| Cybernetic Specialist | farblos | C | -0.80 |
| Engineered Explosives | farblos | R | -0.81 |
| Dominion Infiltration | R | R | -0.82 |
| Highly Illogical | U | U | -0.82 |
| U.S.S. Cerritos, Following Up | farblos | U | -0.83 |
| Horta | R | C | -0.83 |
| Vulcan Mind-Meld | U | U | -0.83 |
| Transporter Malfunction | R | U | -0.87 |
| Enterprise NX-01 | U | U | -0.88 |
| Hive Mind Coprocessor | B | U | -0.90 |
| Emergency Holographic Crew | U | C | -0.95 |
| Data, New Life | U | U | -0.95 |
| Gabriel Lorca, Mirror Menace | B | U | -0.97 |
| La'An Noonien-Singh, Security | R | U | -0.98 |
| Battle-Scarred Survivalist | B | C | -0.99 |
| Ensign Pavel Chekov | U | U | -1.00 |
| Collective Drone | B | U | -1.03 |
| Suus Mahna Practitioner | U | C | -1.03 |
| A Good Day to Die | B | C | -1.04 |
| Marooned | U | C | -1.05 |
| Pure Energy | W | C | -1.05 |
| Genesis Device | G | R | -1.08 |
| Open Communications | U | C | -1.08 |
| Common Goal | G | C | -1.09 |
| Watery Grave | farblos | R | -1.10 |
| Obsidian Order Operative | B | C | -1.10 |
| Conquest Mission | W | U | -1.10 |
| Sarcophagus, Ship of the Dead | R | U | -1.11 |
| Tal Shiar Analyst | R | C | -1.12 |
| Starfleet Spanner Jockey | U | C | -1.13 |
| Plasma Cascade | R | C | -1.18 |
| D'Vana Tendi, Optimistic Ensign | UG | U | -1.19 |
| Gray and Adira, Forever Joined | UR | U | -1.21 |
| Support Mission | G | U | -1.25 |
| Seven of Nine | UB | U | -1.32 |
| Warp Speed | G | U | -1.33 |
| Class-F Shuttlecraft | farblos | C | -1.45 |
| Red Alert! | R | U | -1.45 |
| Unexplored Territory | farblos | C | -1.47 |
| Erica Ortegas, Plucky Pilot | R | U | -1.50 |
| Anthropological Mission | U | U | -1.55 |
| Assault Drone | B | C | -1.55 |
| Isolinear Processor | farblos | U | -1.56 |
| Hit It! | RG | R | -1.56 |
| The Naked Time | R | U | -1.63 |
| Pattern Buffer Preservation | B | C | -1.70 |
| Final Frontier | G | C | -1.71 |
| Worf, Honor-Bound Warrior | WR | U | -1.79 |
| Warp Core | farblos | C | -1.84 |
| Type-2 Phaser | farblos | U | -1.95 |
| Captain's Tutelage | R | C | -1.95 |
| Reckless Impulse | R | C | -1.97 |
| Tell Me What You See | B | U | -2.07 |
| Tricorder | farblos | C | -2.07 |
| Vengeance Mission | B | U | -2.35 |
| Exploratory Mission | R | U | -2.36 |
| The Holodeck | farblos | R | -2.54 |
| Combadge | farblos | U | -2.87 |
