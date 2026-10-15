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

The main bar has Cockpit (the hero builder, opens by default) and Tools. Tools holds Campaign (with Hangar and Missions buttons inside), AI Ships, Squad Builder, Database, Rules and Books, Rules / Play and Settings. Saved sessions that opened on the builder move to the cockpit once.

## 14. Pilot cockpit (replaces the pilot sheet)

Modelled on screenshots of the former xwingunlimited.com. The Pilots tab is now a cockpit: class and XP header, callsign selector, Loadout (slots of the selected ship plus rank slots), Ships (buy for 5 XP from rank 2), Rank 1 to 5 (cost 9, 12, 15, 18 XP, initiative rank plus 1), and a Hand / Deck / Store panel with search and slot filter. The older sheet is still available through "Classic pilot sheet".

Data: `data/hotac_catalog.json` (304 Rebel-usable upgrades from xwing-data2, built by `scripts/build_hotac_data.py`) and `data/hotac_aces.json` (48 pilot ability cards, OCR of Dovi Anderson's Alternate Pilot Abilities PDF merged with names, XP and associated pilots from the HotAC 2nd Edition Ship and Ability Points List). Text from OCR may contain icon garbage; check it against the PDF in Rules and Books.

Known gaps: only two classes are entered (The Old School, The Force User); the other classes, their ships and their rank grants are unknown. Ship slot bars for A-Wing, B-Wing, HWK-290, Eta-2 Actis and Delta-7 are guesses from xwing-data2 and the screenshots. Store prices are card cost values and the HotAC ability list; the original site showed different numbers for some cards, so every price is editable. Cards that use more than one slot occupy only their first slot.

## 15. Card art from project-goldenrod

CrazyVulcan/x-wing2.0-project-goldenrod holds images only (no card text): full cards in `src/images/En/pilots` and `En/upgrades`, cropped art in `Art/pilots` and `Art/upgrades`, all named by xws id. The cockpit Store uses `Art/upgrades/<xws>.jpg` from raw.githubusercontent.com, and the XWA online ship browser falls back to `En/pilots/<xws>.png` when the original image fails. Card text and costs still come from xwing-data2. Live image loading from the browser is untested from the build sandbox.

## 16. Starfield

A fixed canvas behind the page draws drifting, twinkling stars that also shift slightly as you scroll. Cards and the header sit above it. It stays still when the system asks for reduced motion and is hidden when printing.

## 17. Upgrades window

The Upgrades button in the cockpit header opens a window of every upgrade the selected ship can use, with Buy and Install. A checkbox shows every upgrade, including ones this ship cannot use yet (wrong slot, other ship, rank or initiative too low) with the reason; those can still be bought and installed later. Installing into a full slot replaces the card there.

Starting XP: new pilots start with 10 XP (HotAC 2.07 gives X-wing pilots 10). Change it with HC_STARTXP.

Hero creation now asks for a starting ship: X-Wing (10 XP) or Y-Wing (16 XP) for The Old School, Eta-2 Actis or Delta-7 for The Force User (10 XP, unconfirmed).

Pilots saved before the starting-XP change (0 XP, nothing bought) get their starting XP once when the cockpit first opens them.

## 18. XWA card database with pictures

`data/cards2.json` (built by `scripts/build_cards2.py` from xwing-data2) holds all 672 pilots, 524 upgrades and 89 ships with text, cost, loadout, slots and legality. The XWA Database tab loads it from the site itself (no CDN), so it no longer depends on jsDelivr. Cards show the full card image from project-goldenrod (`En/<kind>/<xws>.png`), then the cropped art, then the same names without the expansion suffix, then the original xwing-data2 image. Some of the newest cards are not in the goldenrod repo and rely on that last fallback. The points tables from the PDFs stay under "Points: upgrades" and "Points: pilots".

The cockpit Store and Upgrades window use the same fallback chain, starting with the cropped art. The first version only tried the exact xws name, which failed for cards with expansion suffixes such as "-battleofyavin".

## 19. Header links

The header links to Patreon (https://www.patreon.com/cw/ianmcg, same page the FreeSpace 4x game uses), the website (https://ianmcgo.github.io/website/) and the Cabal Coffers site.

## 20. Visitor log

The visitor log panel and the Visitor Origins globe use the same module as the main website (https://ianmcgo.github.io/website/), copied into `visitors/visitors.js` and `visitors/visitors.css`. The panel and globe markup sit at the end of `index.html`, and `window.VisitorTrackerConfig` sets the client, the storage prefix `xwcockpit2` and the share card text.

The counts are for this app only. They are stored in the FreeSpace 4X Supabase project in two tables of their own, `xw_visit` (one row per visit, with its country) and `xw_device` (visits per day and device kind), so nothing mixes with the website or the FreeSpace game counters. The module's calls were renamed to match: `xw_bump_site_views`, `xw_get_site_views`, `xw_bump_site_view_device`, `xw_get_country_views`, `xw_get_daily_views`, `xw_get_country_firsts`, `xw_get_country_daily`, `xw_get_hour_views`, `xw_my_country` and `xw_get_device_views`. All are security-definer functions; the tables have row level security on and no direct access. The country comes from the `cf-ipcountry` request header, and `ZZ` means unknown (the moon on the globe). A browser counts once per UTC day. The older `xwing_visits` table and its two functions are unused and can be dropped.

## 21. Card zoom

Clicking an upgrade picture in the cockpit (the loadout, the store and the upgrades window) opens the full card in a dark overlay. A click anywhere, or Escape, closes it. It is added to the page body, so redraws of the cockpit do not remove it.

## 22. Store filter and top bar

The Store tab and the upgrades window list only cards the pilot can afford and could fit on the current ship. A checkbox shows everything. The season and mission line was removed from the top bar.

## 23. Tab icon

The browser tab icon is an inline SVG data link in the page head: a dark disc with a goldenrod ring, four wing strokes in an X with cyan engine tips and a red cockpit light. It is an original design, so it needs no extra file.

The page title and header now read X-Wing HotAC Cockpit.

## 24. Top bar layout

The top bar reads, left to right: the title, the edition drop down, then (pushed right) the Support on Patreon, My Website and Cabal Coffers links and the visitor log. There is no footer any more.

The visitor log panel is hidden on screens up to 700px wide (phones); the globe and counting still run.

The visitor files are loaded with a ?v= number; raise it whenever the files change so browsers do not keep an older copy.

In the top bar the visitor log is a compact strip (the open-map footer line is hidden); clicking it still opens the globe.

## 25. Pilot creation order

The Create new pilot screen starts with no class selected. Choosing The Old School or The Force User then shows that class's starting ships, and the pilot can only be created once a class and one of those ships are picked.

## 26. Faction classes

Four community conversion classes were added beside the two HotAC 2.07 classes: Scum and Villainy (Z-95 Headhunter, Y-Wing, HWK-290, Mining Guild TIE), The Resistance (T-70 X-Wing, RZ-2 A-Wing), The First Order (TIE/fo, TIE/sf, later the Silencer) and The Galactic Republic (V-19 Torrent, Clone Z-95 Headhunter, Delta-7). They come from a pasted community summary that could not be checked against a HotAC source, so each shows "Community conversion: ships are unverified". Everything else keeps the confirmed rules: a pilot starts with 10 XP and rank 1, and ships cost 5 XP from rank 2.

Slot bars for the new ships are built from the real 2nd edition ship data (the slots that most of that ship's pilots have, leaving out Talent, Force and Device since rank grants those). The summary's "Y-TIE" and "TYE-Wing" were left out because they are not real ships, and its 35 starting points were ignored because they conflict with the 10 XP start. Enemy AI decks for these factions are not included.

On the create screen, once a faction is chosen the other faction cards are hidden, and a Back to factions button near the bottom clears the choice and shows them all again.

The Separatists class (Vulture Droid, Droid Tri-Fighter, Hyena Droid Bomber, Belbullab-22, Nantex-class) was added the same way, from another pasted community summary that could not be verified. Its slot bars come from the ship data; the Nantex has none beyond the rank slot. The catalog has no Tactical Relay cards yet, so that slot stays empty. The credits economy, the droid wingman and the Republic enemy AI are not built.

## 27. Print, save and export a pilot

Four buttons sit under the pilot name in the cockpit.

- **Print pilot:** opens a white pilot sheet with callsign, class, ship, rank, initiative, XP, kills, ships owned, the full loadout with card text and XP prices, the owned but uninstalled deck, and twelve blank mission log rows. Its Print button uses the browser print dialog (choose Save as PDF there for a file). When printing, everything else on the page is hidden.
- **Save pilot (JSON):** downloads `<callsign>-hotac-pilot.json` holding the whole pilot, with the format name `hotac-cockpit-pilot`.
- **Load pilot:** reads such a file and adds it as a new pilot.
- **Export for Infinite Arenas:** downloads `<callsign>-xws.json` in the XWS 2.0 squad format, which Infinite Arenas and other squad builders import. It holds one ship: the generic pilot of that ship nearest the pilot's initiative, plus the installed upgrades that exist as real cards. HotAC pilot abilities (Aces) are not real upgrade cards, so they are listed in the description instead. The points are the generic pilot's base cost, since HotAC XP is not squad points. The import into Infinite Arenas itself was not tested because the site could not be reached from here.

## 28. Legal line

Every page ends with a footer reading: Unofficial fan tool, not affiliated with or endorsed by Lucas Films, Disney, Fantasy Flight Games or Atomic Mass Games. The credits sentence was removed from the landing page; the credits remain in README.md and docs/sources.md.

## 29. Pirate Lords of the Aturi Cluster

Pirate Lords of the Aturi Cluster (PLotAC), the Scum and Villainy campaign from evolvingdeveloper.com, is now an optional campaign module (Tools, Campaign, Campaign module). While it is selected, the Missions sub-tab shows its 31 missions in arcs: Introduction (Vape Bait), Mining Guild, Acts of Piracy, Illicit Activity, Rivals, Lost Loot, Bonus and the Pirate Hunter wrap-up. Each mission opens to a one-line summary, the objective and notes such as rewards and special rules, with Won, Lost and Clear buttons saved under `S.plotac`. Links point to the author's overview page, the easy-navigation rules page and the threat level calculator.

The author publishes the campaign as web pages, with no PDF, so there is nothing to put in the library downloads. The summaries were written from those pages and are short; Rivals 6 and Lost Loot 5B are incomplete in the source, and the Letter of Marque missions beyond number 1 and the canyon mission's name were not found. Setups, enemy lists and maps stay on the author's site.

PLotAC does not use the cockpit's XP and ranks: its pilots start at 0 XP and 0 credits with a career (Organizer, Professional, Gambler, Slicer, Gearhead, Demolitions, Cyborg or Miner) and spend credits. The cockpit does not model careers or credits yet.

## 30. Expansion choice at pilot creation

After picking a faction on the create screen, a faction with more than one ruleset asks "Are you playing an expansion?". Only Scum and Villainy has a choice so far: Heroes of the Aturi Cluster 2.07 (standard) or Pirate Lords of the Aturi Cluster. The other factions use the standard rules and skip the question. The pilot stores the choice as `exp`.

Choosing Pirate Lords changes the cockpit like this: the pilot picks a career (Organizer, Professional, Gambler, Slicer, Gearhead, Demolitions, Cyborg or Miner); starts at 0 XP and initiative 1 (rank n gives initiative n, not n+1); gets a credits counter in the top row with an Add credits button (amounts in thousands); the campaign module switches to Pirate Lords so the Missions tab shows its missions; and the print sheet shows the career and credits. The career ships (TYE-Wing, TNT, Escape Craft) are custom cards missing from the card data, so the pilot flies the closest real ship. Store prices stay in XP, because the PLotAC upgrade prices were not found.

The note about default store prices at the bottom of the cockpit was removed.

## 31. Kills by ship type

The Add kill button next to the Kills field opens a list of every 2nd edition ship type from the card data, with a search box and a faction filter. Each tap logs one kill of that type, adds one to the Kills total and stays open so several kills can be logged in a row; Other ship type takes a typed name. The pilot keeps the log in `killLog` (ship name and time). Under the pilot's name a row of tags shows the count per ship type; clicking a tag removes one of that type and lowers the total. The Kills number can still be typed by hand, which changes the total but not the log. The print sheet lists kills by ship type. Kills logged before this change show in the total only.

## 32. The Empire class and unlock estimates

The Empire class (Flight Group Alpha style) starts in the TIE/ln Fighter with 15 XP, the TIE/sa Bomber with 10 XP or the TIE/in Interceptor with 5 XP. Those starting values were supplied by the user and are not checked against a source. The higher ships unlock later, and the user asked for estimates. The numbers are guesses, shown with "(estimate)" in the hangar and kept in `HC_UNLOCK` so they are easy to change:

- TIE Advanced x1: rank 2 (initiative 3), 8 XP
- Alpha-class Star Wing: rank 3 (initiative 4), 10 XP
- TIE/D Defender: rank 4 (initiative 5), 14 XP

Every other ship keeps the standard rule of rank 2 and 5 XP. The slot bars come from the real ship data.

## 33. Galactic Republic update and Force User removal

The Galactic Republic class now starts in the V-19 Torrent (15 XP), ARC-170 (8 XP) or Delta-7 Aethersprite (3 XP), values supplied by the user. Later unlocks are estimates kept in `HC_UNLOCK`, which is now keyed by class: the N-1 Starfighter at rank 2 (initiative 3) for 8 XP and the Eta-2 Actis at rank 3 (initiative 4) for 10 XP. The card data has only the Naboo Royal N-1 Starfighter, so that ship stands in for the N-1; a separate Naboo Royal Guard chassis was not added. Starting XP is now looked up by class and ship, so the same ship can start with different XP in different classes.

The Force User class was removed because the Republic covers it. Pilots saved as Force Users become Republic pilots automatically when the page loads.

## 34. Separatists update

Separatists now start in the Vulture-class Droid Fighter (18 XP), Droid Tri-Fighter (12 XP), Hyena Droid Bomber (10 XP) or Nantex-class Fighter (5 XP), values supplied by the user. The Belbullab-22 is a later unlock at initiative 3 or more; the user gave no cost, so it is an estimate of rank 2 and 8 XP in `HC_UNLOCK`, shown as "(estimate)".
