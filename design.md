# X-Wing HotAC Companion: Design Plan

## 1. Goal

A browser app that runs a co-operative X-Wing campaign in the style of Heroes of the Aturi Cluster (HotAC) and its fan descendants, with one switch for edition: 1E, 2E, 2.5E, XWA. It replaces the paper bookkeeping (pilot sheets, XP, upgrades, mission cards, AI ship cards, random ship tables) and lets players use any expansion they own. It is a table companion, not a full digital miniatures game: players still push miniatures and roll dice on the table.

Non-goals for v1: a full 2D tactical simulator with automated dice, online multiplayer, official FFG/Asmodee art redistribution.

## 2. Findings from the supplied material

| Input | What it is | Use in the app |
| --- | --- | --- |
| Star_Wars_X-Wing_Miniatures_Game-9_4_0.vmod | VASSAL module v9.4.0 (Wave XI, July 2022), 18k entries, 3,209 images, buildFile.xml (1.7 MB), per-faction pilot JSON, dials, tokens, condition tokens, 3'x3' map tiles, arc SVGs | Mine for 1E asset names, dial art, tokens, arcs and map backgrounds; use as an extraction source only, not redistributed |
| XWing_HotAC_AI_Ship_Random_Generator_v0.5.xlsx | Two sheets: "AI Random Draw" (ship, level Basic/Elite/PS4/PS6/PS8, d28 roll) and "Tables" (28 numbered loadouts across TIE Interceptor 1-6, Bomber 7-12, Advanced 13-16, Defender 17-20, Phantom 21-24, Lambda 25-28; per-ship PS table, basic upgrade, elite upgrades, PS4/PS6/PS8 named pilots) | Seed data for the random AI generator; port the VLOOKUP logic to a typed table plus a roll function |
| Defenders of the Empire v1.7 (DotE) and mission playtesting 14-16 | Fully co-operative Imperial campaign by Storgar: XP, player ships/pilots, getting shot down, title upgrades, elite talents, AI rules, mission scaling, Rebel and Scum squadrons, missions 1-10 incl. Mugaari campaign | Second campaign module after HotAC; Imperial player side and Rebel/Scum AI |
| Rebel_AI_v5, Rebel_Elite_v4, Scum_AIs_and_SPCs_v04, Imperial_player_cards_v4/v4.1 | Card sheets: AI ship cards and player cards (PDF, symbol-font text) | Data entry targets for the AI card engine; image-only layers need OCR or manual transcription |
| Flight Group Alpha v002, FGA Cardpack v002, Omega One v206 | Fully co-operative adaptation of the TIE Fighter PC game, 13 missions, plus expansion | Campaign module with mission-scripted content |
| Battlestar "Pallas" v0.9.8 | HotAC supplement: captured Gozanti carrier as mothership; starting XP per ship, unlock table with prerequisites, docking/undocking, buying energy/hull/shields with escalating XP cost, Normal vs Hardcore mode | Campaign module with a mothership entity and hangar |
| xwingtmg/xwing-data2 v3.9.1 | JSON for 2E/2.5E pilots, upgrades, quick-builds, actions, conditions, damage decks; 108 pilot files, 22 upgrade files, MIT licensed, has manifest.json and images fields | Primary data source for 2E and 2.5E |
| voidstate/xwing-card-images | 568 1E card images by type (pilots by faction/ship, upgrades by slot) | 1E card art, fetched at build/use time |
| Hinny/HotAC-2nd-edition | Core campaign v0.3 outputs (rulebook, mission book, points lists, pilot sheets, automation cards) and Experience Tree add-on; source folder is a placeholder | Rules and content reference for 2E HotAC; art is rendered PNG/PDF, so content needs transcription |

Reachability from the build environment: GitHub repos work. Google Drive, x-wing-ai.com, YASB, xwing.life, infinitearenas.com and the Steam Workshop are not reachable from here, so the Drive rulebooks, AI card sets and cardboard/token assets must be supplied as files or fetched from a machine with open network access.

## 3. Edition model

Each edition is a pack, selected per campaign and fixed for the life of that campaign.

| Pack | Rules basis | Ship/upgrade data | AI source |
| --- | --- | --- | --- |
| 1E | Original HotAC by Josh Derksen | Derived from VASSAL module JSON and xwing-data (v1) shape; card art from voidstate | x-wing-ai.com 1E AI cards |
| 2E | HotAC 2nd Edition by Hinny | xwing-data2, pre-2.5 points | HotAC 2E automation cards |
| 2.5E | HotAC 2E with 2.5 point/ruleset updates | xwing-data2 current (v3.9.1) | x-wing-ai.com 2E/2.5 AI cards |
| XWA | Newest ruleset: Rulebook v1.1.1 (10/30/2023), Rules Reference v1.4.6, Errata v1.8.2 | xwing-data2 current plus errata printouts | To be defined; HotAC AI cards for this ruleset not yet supplied |

A pack provides: ship and pilot catalog, upgrade catalog with slots, points or XP costs, maneuver dials, action bar, damage deck, AI card set, mission set, campaign rules module. The engine never branches on edition id; it calls pack interfaces.

## 4. Architecture

Current implementation (v0.1): the whole app is a single `index.html` with inline CSS and JavaScript, no build step, opened directly or served from GitHub Pages. It keeps state in localStorage with JSON export and import. The AI random tables from the spreadsheet are embedded (typos normalized). Card data loads at runtime from jsDelivr: xwing-data2 for 2E, 2.5E and XWA, voidstate card images for 1E. Implemented: edition switch, campaign and season tracker, pilot sheets, shot-down handling, Pallas hangar/mothership/unlocks, random AI generator with enemy squadron, card browser with owned-ship filter, settings, export and import. The multi-file layering below is the target if the single file outgrows itself.

- Static single-page app, TypeScript, React, Vite. Hosted on GitHub Pages (matches existing use of GitHub Pages) so no server is required.
- Layers:
  1. data: normalized JSON per pack plus a build script that ingests xwing-data2, the xlsx, the vmod and hand-transcribed card data into one schema.
  2. rules: pure functions with no UI imports. Campaign state reducer, XP and upgrade purchase, shot-down handling, mission scaling, AI maneuver selection, random ship generation.
  3. ui: screens that read state and dispatch actions.
  4. storage: IndexedDB for campaigns and imported inventories, JSON export and import for sharing and backup.
- Deterministic randomness: seeded RNG stored in the campaign so rolls can be replayed and tested.
- Assets are resolved through an asset manifest keyed by pack and card id. Remote art is loaded from its source repo at runtime; nothing proprietary is committed. Users may also drop in a local art folder.
- Tests: unit tests on the rules layer, schema validation of every pack, and snapshot tests that the xlsx random tables reproduce the same outputs as the spreadsheet for every roll.

## 5. Feature set

### 5.1 Campaign manager
- Create campaign: choose edition pack, campaign module (HotAC core, Battlestar Pallas, DotE, FGA, Omega One), player count 1-4, Normal or Hardcore, owned expansions.
- Pilot sheets: ship, pilot skill or initiative, XP, kills, upgrades, elite talents, titles, ace status (e.g. Predator after five kills of a type).
- Hangar: shared upgrade pool, owned and spare ships, buying a replacement ship (Pallas: 5 XP, Z-95 fallback with negative XP).
- Mothership (Pallas): purchasable energy, hull, shields with escalating cost, ordnance tubes, docking state, unlock table with prerequisites.
- Mission log, season tracking, unlock prerequisites, save and load.

### 5.2 Mission runner
- Mission cards with setup diagram, objectives, scaling by player count and level.
- Per-round helper: initiative order, AI activation list, reminders for special mission rules.
- Mission result entry feeds XP and unlocks.

### 5.3 AI engine
- AI ship card model: facing arc, target-priority rules, maneuver table by range and bearing, action priorities, per-level modifiers (Basic, Elite, PS4, PS6, PS8).
- Random AI generator: port of the spreadsheet (d28 table, ship picker, level picker, re-roll) with named pilots and upgrades.
- Step-through resolver: player enters distance, arc and bearing of nearest target, app shows the maneuver and action; manual override always available.
- Scum, Rebel and Imperial AI sets, plus elite variants.

### 5.4 Squad builder (YASB-style, secondary)
- Build player squads and Rebel squadrons for DotE under pack points rules, using xwing-data2 for 2E/2.5E and 1E data. Import and export XWS JSON.

### 5.5 Collection and expansions
- Expansion toggle list; filters ships, upgrades, pilots and missions to what the user owns.
- Optional inventory import compatible with xwingtmg2-inventory-rs output.

### 5.6 Print and reference
- Printable pilot sheets, AI cards and mission cards; searchable card browser with art.

## 6. Data pipeline

1. ingest-xwing-data2: read data/pilots, upgrades, damage-decks, actions, quick-builds; emit pack files; keep upstream xws ids as keys.
2. ingest-xlsx: read Tables sheet into typed AI draw tables (ship type, PS table, basic upgrade, elite upgrades, PS4/PS6/PS8 pilot, roll ranges 1-6, 7-12, 13-16, 17-20, 21-24, 25-28). Known typos in the sheet (for example "Outmaeuver", "Chiranear", "Chiraneau") are normalized against xwing-data names and listed in a report.
3. ingest-vmod: unzip, read buildFile.xml and per-faction pilot JSON, map to 1E ids, list art and token assets available for local use.
4. transcribe-cards: AI and player card PDFs use a symbol font that extracts as garbage text, so card data is produced by rasterizing pages and transcribing (OCR plus manual review) into YAML, one file per campaign module, checked by a schema.
5. validate: every upgrade slot, pilot, ship and AI reference must resolve; build fails otherwise.

## 7. Repository layout

```
/design.md
/README.md
/docs/sources.md
/data/packs/{1e,2e,2.5e,xwa}/
/data/campaigns/{hotac,pallas,dote,fga,omega-one}/
/data/ai/
/scripts/ingest-*.ts
/src/rules/ /src/ui/ /src/storage/
/tests/
```

## 8. Milestones

1. M0 Foundations: repo scaffold, TypeScript, lint, tests, CI, Pages deploy, pack schema.
2. M1 Data: xwing-data2 ingest for 2E and 2.5E; card browser; edition switch working on read-only data.
3. M2 Campaign core (2E): pilot sheets, XP, upgrades, hangar, save and load, HotAC core missions list.
4. M3 AI engine: random generator ported from the xlsx with parity tests, AI card model, step-through resolver for TIE Interceptor, Bomber, Advanced, Defender, Phantom, Lambda.
5. M4 1E pack: voidstate art mapping, vmod ingest, 1E HotAC rules.
6. M5 Modules: Battlestar Pallas, DotE with Rebel and Scum AI, mission scaling.
7. M6 FGA and Omega One missions, expansions toggle and inventory import.
8. M7 Squad builder, printing, polish, accessibility, mobile layout.
9. M8 XWA pack once defined.

## 9. Risks

- Copyright and licensing: this is an unofficial fan tool. FFG/Asmodee art, HotAC, DotE, FGA and Pallas content belong to their authors. Do not commit proprietary art; link or load at runtime; ask each campaign author for permission before bundling transcribed text; keep a credits page. xwing-data2 is MIT; check LICENSE of every other source before reuse.
- Card data is trapped in PDFs with symbol fonts: transcription is the largest manual cost.
- 1E and 2E data shapes differ; the normalized schema must cover both without edition branches.
- Source sites unreachable from the build environment; ingestion scripts must support local file inputs.
- Spreadsheet is v0.5 with typos; treat it as seed data, not truth.

## 10. Open questions

1. XWA edition: is this the Flight Group Alpha style adaptation of the X-Wing Alliance PC game, or a custom ruleset? Which document defines it?
2. 2.5 edition: should it track the current xwing-data2 points and errata only, or also AMG-era HotAC changes you have notes on?
3. The two Drive folders: please upload the HotAC 1E rulebook, AI card set and mission books, since Drive is not reachable from here.
4. Primary mode: pure table companion (recommended), or also an on-screen board with movement and dice?
5. Hosting target: GitHub Pages under ianmcgo/xwing, or a custom domain such as cabalc.com?

## 11. Update log

### v0.2
- XWA tab: game tracker (squad points, deficit mission points, 12 rounds, five phases, 20 mission point end condition) and the four standard scenarios, from the uploaded XWA rulebook. Scoring text is summarized for Satellite Array and Chance Engagement; Salvage Mission and Scramble the Transmissions point to the rulebook.
- HotAC 2.07.04 (Tiernan conversion of Derksen's campaign) from the Campaign Book and Mission Pack: starting X-wing 10 XP and Y-wing 16 XP, XP shop with the rule costs, mission list for all five arcs with territory and turn limits, XP tally per mission, eject rolls by territory, banking XP.
- Eject interpretation (mine, check against the book): each attack die is 3 hits, 2 crits, 2 focus, 1 blank. Two or more crits kill the pilot, one crit loses the most expensive talent, each hit loses the most expensive upgrade, one focus halves XP, two focus zero it. Lost cards are reported in the log and removed by hand because card costs are not tracked yet.

### Newly supplied material
- HOTAC Campaign Book and Mission Pack 2.07.04 (text extractable, used above), Optional Rules, Terrain stat cards, Additional Printable Materials, Alternate Pilot Abilities, Ground Assault campaign (book and components).
- Elite Pilot Cards, Rebel Pilot Cards and Imperial Ship A.I. cards (FGA v7.3): image-only, need transcription before an AI engine can use them.
- 1stEdition.zip: original campaign book, decks, stat cards, terrain.
- CWCC-Entries.zip: community campaigns (Clone Wars, Pandemonium in the Aturi Cluster, Last Vestige of the Jedi, Heroes of the Old Republic) with droid AI cards and components.
- Next: add Ground Assault and the community campaigns as campaign modules, transcribe AI cards.
