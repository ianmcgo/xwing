# X-Wing Squad Builder and Reference: Build Plan

## 1. Scope

A single-page web app, hosted at ianmcgo.github.io/xwing, that does three things:

1. Squad builder for four editions.
2. Database of ships, pilots, upgrades and cards with card art.
3. Reference library for campaigns and rules (HotAC and its community descendants, plus each edition's rules).

Not in scope: an on-screen board, movement, dice, or online play. The campaign trackers built in v0.1 and v0.2 (pilot sheets, XP, mission tracker, XWA game tracker, Pallas hangar, AI ship generator) stay as a secondary Tools area and are not the focus.

## 2. Editions and data

| Edition | Squad scale | Data source | Pinned version (default) |
| --- | --- | --- | --- |
| 1st Edition | 100 points, pilot skill | guidokessels/xwing-data (297 pilots, 367 upgrades, 56 ships) plus card art from voidstate/xwing-card-images and the xwing-data images folder | master |
| 2.0 | 200 points, pilot costs in the 40s | xwingtmg/xwing-data2 | tag xwing-2.0 (data version 2.5.3) |
| 2.5 / AMG | 20 squad points, per-ship loadout value; rulebook v1.1.1, Rules Reference v1.4.6, Errata v1.8.2, ship points 2024-09-06, upgrade points 2024-11-01 | xwing-data2 tag 3.9.1 for card text and art (its points predate the 2024 sheets); the points PDFs are the source of truth | 3.9.1 |
| XWA (X-Wing Alliance) | Community-run organized play body (volunteer group formed June 2024, not affiliated with Lucasfilm or Asmodee). Documents per your description: 50P Points Companion, XWA Core Rules and Rules Reference, errata, ban and restricted lists. Not yet supplied. | Points and legality from the XWA documents, card data from xwing-data2 | 3.9.1 placeholder |

Checked against the real tags: points on the 2.0 tag are on the old 200-point scale, and every 3.x tag is on the new 20-point scale with loadout values.

The pinned tags are my best mapping of your four editions to data releases. Each is a dropdown in Settings (all 60 tags are listed), so you can repin an edition to the exact release you mean without code changes. Data loads at runtime from jsDelivr, for example `cdn.jsdelivr.net/gh/xwingtmg/xwing-data2@3.1.0/data/manifest.json`.

## 3. Architecture

- One `index.html` with inline CSS and JavaScript, no build step, no server. Works from GitHub Pages or a local file.
- A data layer with one normalizing adapter per source (1E, data2) that turns every edition into the same internal shape: ships, pilots, upgrades, slots, costs, restrictions, art URLs.
- Caching: fetched JSON kept in IndexedDB keyed by edition and version, so the app works offline after first load.
- State in localStorage (squads, settings, pinned versions), export and import as JSON, plus shareable squads in XWS format and a URL hash.
- No comments in code; explanations live here.

## 4. Squad builder

- Pick edition, faction, game mode (point limit editable per edition).
- Add ship pilots from a filterable list; add upgrades to the slots the ship offers.
- Legality checks per edition:
  - 1E and 2.0: total points under the limit, slot match, unique and limited cards, upgrade restrictions.
  - 2.5, AMG, XWA: squad points under 20, upgrade cost sum under the ship's loadout value, 3 to 8 ships, one faction, limited and solitary cards, restricted and ban list counts, standard loadout ships take no upgrades.
- Live totals, warnings, a printable list, XWS import and export, copy as text.
- Saved squads list with rename, duplicate and delete.

## 5. Database

- Browsers for ships, pilots, upgrades and conditions, by faction and slot.
- Search and filters: name, ship, initiative, cost, slot, faction, unique, text.
- Card detail with art, ability text, restrictions, and the cost under each of the four editions side by side.
- "Owned" flags per ship and upgrade, plus an owned-only filter; optional inventory import.
- Errata handling for XWA: flag cards covered by Errata v1.8.2 and link the printout.

## 6. Campaigns and rules library

Static content pages, one per entry, each with summary, what it needs, link to the source file, and credits.

| Section | Entries |
| --- | --- |
| Core rules | 1E, 2.0, 2.5, AMG, XWA summaries (phases, round count, squad building, scenarios); XWA from rulebook v1.1.1 and Rules Reference v1.4.6 |
| HotAC family | HotAC 1E (original), HotAC 2.07.04 (2E conversion), Optional Rules, Alternate Pilot Abilities, Terrain stat cards, Ground Assault, Battlestar Pallas, Defenders of the Empire, Flight Group Alpha and Omega One, Scum AI set |
| Community campaigns | Clone Wars, Pandemonium in the Aturi Cluster, Last Vestige of the Jedi, Heroes of the Old Republic |

Contents are hand-written summaries, not copies of the books. Where a rule table is short and factual (XP costs, territory types) it is encoded as data.

## 7. Repository and hosting

```
index.html
design.md
README.md
docs/sources.md
```

Hosting: GitHub Pages from the `main` branch root gives ianmcgo.github.io/xwing. It needs one setting I cannot change from here: repository Settings, Pages, Source "Deploy from a branch", branch `main`, folder `/ (root)`.

## 8. Milestones

1. M1 Data layer: 1E adapter and data2 adapter, version pinning, IndexedDB cache, normalized model, tests against the five pinned versions.
2. M2 Database: browsers, search, card detail, cost-across-editions view, owned flags.
3. M3 Squad builder, 2.0 and 1E: slots, points, restrictions, save and export.
4. M4 Squad builder, 2.5, AMG, XWA: squad points, loadout values, standard loadouts, restricted list, ban list.
5. M5 Rules and campaigns library: all core rules pages and every campaign entry.
6. M6 Polish: URL sharing, printing, mobile layout, accessibility, offline.
7. M7 Move the existing campaign trackers under a Tools tab.

## 9. Risks

- Edition-to-release mapping may not match what the community calls 2.5 and AMG 2.5. The Settings dropdown is the fix.
- Ban and restricted lists, per-ship upgrade bars and the official points sheets live on atomicmassgames.com, which I cannot reach from here. They need uploading or a data file you maintain.
- 1E data in xwing-data is community maintained and stops at the last wave it covers.
- Art belongs to FFG, AMG and Lucasfilm. The app links to art at its source and bundles none.
- Card and campaign PDFs with symbol fonts (AI cards, elite pilot cards) are image-only; the library links to them rather than transcribing them.

## 10. Open questions

1. Which data2 release do you consider "2.5" and which "AMG 2.5"? Defaults are 3.1.0 and 3.6.3.
2. Can you upload the AMG points and loadout sheets, ban list and restricted list?
3. Should the existing campaign trackers stay, or be removed to keep the app focused on builder, database and library?

## 11. Existing prototype (v0.2)

The current `index.html` already contains the campaign trackers, an AI ship generator seeded from the HotAC spreadsheet, a basic 2E and 1E card browser, the HotAC 2.07.04 XP shop and mission tracker, and an XWA game tracker. M1 reuses its card loading and its tab and storage scaffolding.

## 12. Update v0.3

- Editions are now 1st Edition, 2.0, 2.5 / AMG (one edition) and XWA. The rules documents earlier labelled XWA were the 2.5 / AMG documents, so the tracker is relabelled and XWA has no rules yet.
- New Rules tab: per edition, a document list with an in-page reader (browser PDF viewer) and download buttons for rulebook, rules reference, errata and points. 2.5 / AMG has all five documents hosted in `files/2.5/` (rules reference recompressed from 75 MB to 12 MB, text unchanged). 1E, 2.0 and XWA show what is still needed.
- Card browser now loads the pinned data release per edition: 2.0 uses tag xwing-2.0, 2.5 / AMG and XWA use 3.9.1.
- Next: parse the ship and upgrade points PDFs into data so the 2.5 / AMG builder uses the 2024 costs, loadout values, upgrade bars and legality columns.

## 13. Update v0.4

- 1st Edition database: all 297 pilots and 367 upgrades from guidokessels/xwing-data are embedded in `index.html`, so the list no longer depends on a live file-listing API. Card art loads from raw.githubusercontent.com. Filters by faction, ship or slot, text search, owned flags, paging.
- The previous 1E tab depended on the jsDelivr file-listing API, which I could not reach from my environment and had only tested against a stub. That is the likely reason the cards did not show.
- Database is now the default tab.
- Still not built: the squad builder.

## 14. XWA definition

XWA is the X-Wing Alliance, a community organization running organized play and rules and points updates for X-Wing. A June 2025 roadmap article states it is a volunteer group formed in June 2024 with elected council, planned a Q4 2025 points update and a March 2026 world championship, and does not represent Lucasfilm or Asmodee. The article does not list its documents or version numbers, so the document list above comes from your description and is unverified. The XWA site and documents are not reachable from the build environment; they need uploading. The XWA edition then gets the same Rules tab treatment as 2.5 / AMG and its own builder rules (points scale, ban and restricted lists).
