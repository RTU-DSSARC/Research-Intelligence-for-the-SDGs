# RTU Research Intelligence for the SDGs

An interactive, static HTML dashboard for Rizal Technological University, based on two uploaded Scopus CSV exports and a 30-slide presentation report. No server, backend, developer account, API key, or JavaScript library is needed.

## GitHub Pages: deployment in 6 steps

1. Create a GitHub repository, for example `rtu-sdg-dashboard`.
2. Extract the `RTU_SDG_GitHub_Pages.zip` archive **before** uploading.
3. Upload `index.html`, `assets/`, `data/`, and `README.md` to the **root** of the repository. The `index.html` file must not be nested inside a subfolder if you want the site at the repository's Pages URL.
4. Commit the files to the `main` branch.
5. In your repository, open **Settings → Pages**. Under **Build and deployment**, select **Deploy from a branch**. Select **main** and **/(root)**, then Save.
6. Open the GitHub Pages URL shown there, usually `https://YOUR-USERNAME.github.io/rtu-sdg-dashboard/`. Publication can take some time; GitHub will display the actual status.

**Alternative:** Upload the standalone HTML file renamed to `index.html` as the only file in your repository. That edition embeds the transparent RTU logo and publication data directly in the HTML. It requires no subfolders. The included `.zip` edition is easier to update and audit.

## Dashboard pages

- **Overview:** filtered publication counts, SDG coverage, citations, open access, annual output, top goals, and insights.
- **SDG Atlas:** all 17 UN SDGs with official goal colors, thematic-paper counts, clickable cards, SDG-year heatmap, and multi-label statistics.
- **Trends & Impact:** annual publication output, citations by publication year, citations per SDG-linked paper, document formats, and top-cited publications.
- **Publications:** searchable, filterable, sortable, paginated bibliographic records; DOI links; filtered CSV export.
- **Researcher Explorer:** searchable author-directory records with Scopus Author IDs and links into the publication dataset.
- **Strategy & Methods:** the PowerPoint's suggested 2029 targets, source comparison, categorization protocol, and interpretation caveats.

## Why this dashboard does not match all numbers in the PowerPoint

| Source | Date / coverage | Publications | Citations | Researcher field |
|---|---|---:|---:|---|
| Uploaded Scopus publications CSV | Publication years 2021–2026 (export timestamp unknown) | **109** | **370** | Publication author IDs; not verified as all RTU employees |
| Uploaded Scopus authors CSV | Separate author export | n/a | n/a | **113** valid Scopus Author IDs |
| presentation (slide deck) | 2019–6 October 2026 | **110** | **315** | **105** RTU-affiliated researchers reported |

The data source populations/times differ; the dashboard **does not reconcile or combine** them. The interactive views use the 109-record publication CSV. 2026 is partial. The CSV also includes two separate EIDs for an identical title about Philippine SDG 4; both were retained as separate records. Manual bibliographic de-duplication is advisable before any audited institutional reporting.

## SDG classification: important limitation

The uploaded Scopus export has **no validated Scopus/ SDG tags**. For this dashboard, 109 titles were manually audited using a conservative, title-based mapping with selective abstract review. One publication can be assigned to more than one SDG; a publication can also be left unassigned. As initially coded, **90/109** records have at least one *assigned* SDG tag, and **19** are unassigned. The covered goals are 14/17. The categorization is an **exploratory thematic proxy**, not evidence of United Nations-endorsed alignment, SDG target attainment, community impact, or a citation-causal effect.

To review the exact mappings, open `data/sdg_mapping.csv` or `data/data.json`. The assignment rules are also readable in `build_data.py` (the `CURATED` list).

## Updating the dashboard with a new export (optional)

The deployed website is fully static. To regenerate the local data bundle, install Python 3.10+ and pandas, then save the two fresh input files in a new `source/` folder with these exact filenames:

- `source/RTU Scopus Publications 2019-2026.csv`
- `source/RTU Scopus Authors.csv`

Run:

```bash
python -m pip install pandas
python build_data.py
```

For custom paths:

```bash
RTU_PUB_CSV=/path/to/publications.csv RTU_AUTH_CSV=/path/to/authors.csv python build_data.py
```

**Important:** `build_data.py` intentionally requires one documented, manually audited title pattern per publication. New records will trigger a validation error until they are explicitly reviewed and assigned. Update the PowerPoint snapshot fields manually in the script if that source changes. Commit the updated `data/data.js`, `data/data.json`, and `data/sdg_mapping.csv` to GitHub.

Do **not** upload the raw Scopus CSVs or full abstracts to your public GitHub repository without first reviewing contractual redistribution rights and privacy concerns. The dashboard includes selected bibliographic data and source links, not the CSV's full abstracts.

## Files

```text
index.html             Main dashboard
assets/rtu-logo-transparent.png   Background-free RTU seal
assets/site-icon.png        Small favicon/preview asset
data/data.js            Prebuilt public browser data
data/data.json           Auditable data snapshot
data/sdg_mapping.csv   Publication–SDG mapping review table
build_data.py            Optional rebuild utility
README.md              This guide
```

## Technical details

Client-side vanilla JavaScript; zero third-party libraries, trackers, cookies, or API keys. Filtering, charts, tables, and CSV export run in the browser. Works with GitHub Pages or other static hosting. The multi-file edition can also be opened locally by double-clicking `index.html` in modern browsers; the standalone HTML edition is completely self-contained.

Prepared for RTU Data Science and Smart Analytics Research Center · November 2026.


## November 2026 overview refinements

The overview now contains native, interactive presentation-reference charts for research-theme publication and citation shares, collaborating countries, partner institutions, and acknowledged funders. Click or keyboard-select a bar to inspect the exact value. These reporting figures are fixed snapshots and do not respond to the publication CSV filters.

Both the transparent RTU seal and the Data Science and Smart Analytics Research Center logo are displayed at the bottom of the dashboard. The informational comparison banner above the filters was removed; source details remain available under Strategy & Methods.
