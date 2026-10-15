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
- Edition switch (1st Edition, XWA).
- Database: full 1E browser with filters, search, owned flags and paging; XWA card browser from xwing-data2.
- Rules tab: read in the page and download, per edition.
- Campaign tools from earlier versions: HotAC 2.07.04 XP shop and mission tracker, Battlestar Pallas hangar and unlocks, AI ship random generator, game tracker with scenarios.

Not built:
- Squad builder.
- 1E rules documents.
- XWA points companion, ban and restricted lists.
- Campaign books in the library.

## 4. Build order

1. Squad builder for 1st Edition: pilots, upgrades by slot, 100-point limit, unique cards, slot and restriction checks, save, copy as text, XWS import and export.
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
