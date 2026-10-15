# X-Wing Squad Builder and Reference: Plan

## 1. What it is

A single-page web app (one `index.html`, no build step) for ianmcgo.github.io/xwing with three jobs:

1. Build squads.
2. Browse a database of ships, pilots, upgrades and cards with art.
3. Read and download rules documents and campaign information.

No board, no dice, no online play.

## 2. Editions

Two editions only:

| Edition | Rules documents | Card and points data |
| --- | --- | --- |
| 1st Edition | None supplied yet | xwing-data (297 pilots, 367 upgrades) embedded in the page; art from the xwing-data GitHub repo |
| XWA | Rulebook v1.1.1, Rules Reference v1.4.6, Errata v1.8.2; ship points 2024-09-06 and upgrade points 2024-11-01 (AMG documents) | xwing-data2 tag 3.9.1 for card text and art; the points PDFs are the source of truth for costs |

XWA is the X-Wing Alliance community organization. Its own 50P Points Companion, ban list and restricted list have not been supplied. The three rules files uploaded as XWA material are identical (same checksums) to the AMG 2023 files, so XWA currently uses them.

The earlier 2.0 and 2.5 / AMG editions were removed to keep things simple.

## 3. Current state (v0.5)

Built:
- 1st Edition squad builder (v0.6, section 8).
- Edition switch (1st Edition, XWA).
- Database: full 1E browser with filters, search, owned flags and paging; XWA card browser from xwing-data2.
- Rules tab: read in the page and download, per edition.
- Campaign tools from earlier versions: HotAC 2.07.04 XP shop and mission tracker, Battlestar Pallas hangar and unlocks, AI ship random generator, game tracker with scenarios.

Not built:
- XWA squad builder.
- 1E rules documents.
- XWA points companion, ban and restricted lists.
- Campaign books in the library.

## 4. Build order

1. Squad builder for 1st Edition: done in v0.6.
2. XWA builder: parse the ship and upgrade points PDFs into data (cost, loadout value, upgrade bar, Standard and Extended legality), then enforce 20 squad points, 3 to 8 ships, loadout values, limited cards, ban and restricted lists. Swap in the XWA points companion when supplied.
3. Rules and campaign library: add HotAC books, Ground Assault, Pallas, Defenders of the Empire, Flight Group Alpha, community campaigns as readable and downloadable entries.
4. Move campaign tools under a Tools tab.
5. Polish: shareable links, printing, mobile, offline cache.

## 5. Hosting

GitHub Pages from `main`, folder root: repository Settings, Pages, Deploy from a branch. Rules PDFs live in `files/xwa/` (the rules reference was recompressed from 75 MB to 12 MB).

## 6. Risks and open items

- XWA documents beyond the AMG files are missing; XWA may have its own newer rulebook.
- Card data from xwing-data2 predates the 2024 points sheets.
- Art belongs to its owners; the app links to art and does not bundle it.
- jsDelivr and GitHub card art could not be tested live from the build environment.

## 7. Source files received

HotAC 2.07.04 books and card sheets, Ground Assault, Optional Rules, Alternate Pilot Abilities, 1stEdition.zip, CWCC community campaigns, Battlestar Pallas, Defenders of the Empire, Flight Group Alpha and Omega One, AI generator spreadsheet, VASSAL module 9.4.0, XWA/AMG rules documents and points sheets. See `docs/sources.md`.

## 8. 1st Edition squad builder (v0.6)

Features: multiple saved squads, faction and point limit (default 100, editable), add pilots by ship, equip upgrades per slot from dropdowns that only list legal cards, live point total with warnings, duplicate non-unique ships, squad text, XWS JSON export and import, print.

Rules enforced:
- Squad is one faction; the pilot list is filtered to it.
- Points: pilot points plus upgrade points (negative costs from refits and titles count), total against the limit.
- Slots: the pilot's printed slots, one Title slot on every ship and one Modification slot on every ship except huge ones, plus slots granted by equipped upgrades (for example R2-D6 grants Elite). Removing a granting upgrade clears upgrades in the slots it granted.
- Unique cards: one copy per squad, counted across pilots and upgrades by name.
- Upgrade restrictions from the data: faction, ship size, specific ships.
- Limited upgrades: one copy per ship. Squad-limited upgrades: one copy per squad.
- Pilot skill shows bonuses granted by upgrades such as Veteran Instincts.

Interpretation and limits:
- "Limited" is applied as one per ship. Check against the 1E rules reference once supplied.
- Restrictions that exist only as card text (for example "Rebel only" without a data field) are not enforced, so some cards may appear for the wrong faction or ship. Epic and huge ship special rules, and dual-slot cards, are not enforced.
- Data comes from xwing-data and stops at the last wave it covers.
- Tested end to end in a headless browser: add pilot, equip, points, text export, XWS export, XWS import round trip.

## 9. XWA squad builder (v0.7)

Data comes from `scripts/parse_points.py`, which reads the Ship Points (2024-09-06) and Upgrade Points (2024-11-01) PDFs and writes `data/xwa_points.json` (embedded in index.html as `XWA`). Run it with the two PDFs, an output path and a checkout of xwing-data2 (used only for ship sizes).

Rules enforced: squad point limit (default 20), 3 to 8 ships, one faction per squad, loadout value per ship, standard loadout ships take no upgrades, limited cards (bullets = copies allowed by name), upgrade bar slots (multi-type upgrades use one slot of each type), Standard or Extended legality, banned cards.

Restrictions are free text in the PDF. A small evaluator handles factions, ship names, keywords, sizes and "squad including X". Anything with an icon glyph, "Standardized", or an unrecognised phrase is reported as "cannot check automatically" instead of being guessed.

Known gaps: the PDFs do not separate Restricted from Banned, so Restricted cards are not flagged. Ship sizes are missing for the Upsilon-class and Xi-class shuttles. The XWA 50P points companion and ban lists have not been supplied. No card art in the XWA builder yet.

## 10. 1st Edition official missions

`E1_MISSIONS` lists the 17 missions in the Official Missions PDF (M1 to M9, Hoth H1 to H3, Point of No Return T1 to T4), transcribed from OCR of the scanned booklet and shortened. The PDF is in `files/1e/` and listed in the Rules tab. Won/lost is tracked in `S.offm`. The booklet has no solo rules.

## 11. XWA database tab

The XWA Database tab now opens on embedded data (all 407 upgrades and 661 pilots with cost, slot, restrictions and Standard/Extended legality) with search, slot, faction and format filters, and works offline. Card text and art still come from xwing-data2 through the "Card text and art (online)" button.

## 12. Expansions and campaign library

1st Edition: `E1_SRC` holds the 63 products from xwing-data `sources.js` with the pilot and upgrade ids each contains (ids equal the row index in `E1_PILOTS` and `E1_UPGRADES`, checked by name). The Database tab has a My expansions panel for quantities; `S.exp1` stores them. The Owned only filter in the database, and an optional filter in the builder (`sq.ownOnly`), use expansions plus cards marked owned by hand.

XWA: no product contents data is available (xwing-data2 has none and the points PDFs have none), so there is no expansion tracking for XWA yet.

Campaign library: Defenders of the Empire, Flight Group Alpha (with card pack and Imperial AI cards), Omega One and Battlestar Pallas PDFs are in `files/campaigns/` and appear in the Rules tab for both editions.

## 13. Navigation

Main tabs are the hero and campaign tools: Pilots (the hero builder, now the default), Campaign, Hangar, AI Ships and Missions. A Tools button opens a second row with Squad Builder (standard play), Database, Rules and Books, Rules / Play and Settings. Saved sessions that opened on the builder move to Pilots once.

## 14. Pilot cockpit (replaces the pilot sheet)

Modelled on screenshots of the former xwingunlimited.com. The Pilots tab is now a cockpit: class and XP header, callsign selector, Loadout (slots of the selected ship plus rank slots), Ships (buy for 5 XP from rank 2), Rank 1 to 5 (cost 9, 12, 15, 18 XP, initiative rank plus 1), and a Hand / Deck / Store panel with search and slot filter. The older sheet is still available through "Classic pilot sheet".

Data: `data/hotac_catalog.json` (304 Rebel-usable upgrades from xwing-data2, built by `scripts/build_hotac_data.py`) and `data/hotac_aces.json` (48 pilot ability cards, OCR of Dovi Anderson's Alternate Pilot Abilities PDF merged with names, XP and associated pilots from the HotAC 2nd Edition Ship and Ability Points List). Text from OCR may contain icon garbage; check it against the PDF in Rules and Books.

Known gaps: only two classes are entered (The Old School, The Force User); the other classes, their ships and their rank grants are unknown. Ship slot bars for A-Wing, B-Wing, HWK-290, Eta-2 Actis and Delta-7 are guesses from xwing-data2 and the screenshots. Store prices are card cost values and the HotAC ability list; the original site showed different numbers for some cards, so every price is editable. Cards that use more than one slot occupy only their first slot.

## 15. Card art from project-goldenrod

CrazyVulcan/x-wing2.0-project-goldenrod holds images only (no card text): full cards in `src/images/En/pilots` and `En/upgrades`, cropped art in `Art/pilots` and `Art/upgrades`, all named by xws id. The cockpit Store uses `Art/upgrades/<xws>.jpg` from raw.githubusercontent.com, and the XWA online ship browser falls back to `En/pilots/<xws>.png` when the original image fails. Card text and costs still come from xwing-data2. Live image loading from the browser is untested from the build sandbox.

## 16. Starfield

A fixed canvas behind the page draws drifting, twinkling stars that also shift slightly as you scroll. Cards and the header sit above it. It stays still when the system asks for reduced motion and is hidden when printing.
