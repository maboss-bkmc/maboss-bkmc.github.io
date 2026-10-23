# maboss.curie.fr

Website of MaBoSS (Markovian Boolean Stochastic Simulator), developed by the Computational Systems Biology of
Cancer group at Institut Curie. Static site, no build step: everything served is in `html/`.

## Deployment

- `Dockerfile`: `httpd` image, copies `html/` to the Apache web root. Nothing outside `html/` is deployed.
- `.gitlab-ci.yml`: builds and pushes the image on **tags** only.
- Branches: work on `master`; `main` is the main branch for PRs.

## Structure of `html/`

- `index.html`: the whole site, a single page (~1700 lines).
- `style.css`: all the styles. `script.js`: navigation (~80 lines, no framework, no dependencies).
- `images/`: logos, team photos (`firstname.lastname.jpg`), `images/ecosystem/` for the MaBoSS ecosystem pages.
- `files/<Model>/`: one folder per model page: `.bnd`/`.cfg` files, notebook, zip, `figures/` produced by the notebook,
  and static images (influence graphs, published figures, screenshots).
  Folders: `ToyModel`, `CellCycle`, `CellFate`, `p53Dam`, `DrosoPattern`, `EGF_TNF`, `ProstateCancer`
  (also hosts the Tutorials screenshots), `SizekCellCycle`, `HowTo` (How To figures).
- `UPMaBoSS/`: UPMaBoSS cell fate model, its two notebooks, zip and `figures/`.
- `EnsembleMaBoSS/index.html`: fetched at load time into `#maboss_ensemblemaboss` (menu entry commented out).
- `pub/`: PDFs, example model (`example.bnd`/`example.cfg`, used by How To), old MaBoSS tarballs.
- `Cours/`, `PerlScript/`: legacy material, linked from the site.
- Redirect stubs for old URLs (meta refresh): `UPMaBoSS/index.html` → `../index.html#upmaboss`;
  `WebMaBoSS/index.html` and `webmaboss/index.html` → https://webmaboss.vincent-noel.fr.

## index.html conventions

- Each page is a `<div id="maboss_<name>" class="hidden">` inside `#content`, between
  `<!-- NAME : BEGIN -->` / `<!-- NAME : END -->` comments. Its menu entry is
  `<a href="#" id="mi_<name>" class="menu_item" onclick="show('<name>');return false;">` in `nav#menu`.
- `show(name)` hides all `maboss_*`, shows one, highlights `mi_<name>`, scrolls to top, closes the mobile menu, and
  writes `#<name>` in the URL; `show_from_hash()` opens the page of the URL hash at load.
- Pages: `home`, `installation`, `howto`, `tutorials`, `documentation`, `model_toy`, `model_cell_cycle`,
  `model_cell_fate`, `model_p53`, `model_drosophila`, `model_egftnf`, `model_prostate`, `model_sizek`, `upmaboss`
  (UPMaBoSS Cell Fate model), `eco_profile`, `eco_physiboss`, `eco_upmaboss`, `eco_ensemble`, `eco_exastolog`,
  `publication`, `team`, `contact`.
- Tabs (Installation, How To, Tutorials have pyMaBoSS / WebMaBoSS / command line tabs): links
  `id="<group>_tab_<name>" class="tab"` + panels `id="<group>_panel_<name>" class="tab_panel"`, switched with
  `show_tab(group, name)`. Links to another page's tab: `onclick="show('installation');show_tab('installation', 'pymaboss');return false;"`.
- Indentation: tabs inside page divs, `<pre>` blocks start at column 0 (their content is literal).
- Links: `class="clean-link"`; inline code: `<span class="tt">`. Accents: both HTML entities (`&eacute;`) and
  UTF-8 are used; follow the surrounding text.
- Publications page: `<h4>` sections with `<ul class="pub-list"><li class="list">`, authors as `Stoll G, Viara E, ...`,
  then title, journal in `<i>`, year;volume:pages, `doi:` link.

### Reusable blocks (style.css)

- Figure: `<figure class="figure"><a href="X"><img src="X" alt="..."/></a><figcaption>...</figcaption></figure>`;
  add `class="figure_small"` on the img for small figures (max 420px).
- Related figures side by side (stacked on phones): wrap figures in `<div class="figure_grid">`;
  `figure_grid figure_grid_narrow` for narrow images (Drosophila patterns), plus `figure_grid_small` to cap the width.
- Tables: `<div class="df_wrapper"><table class="df_table">` (scrolls horizontally on phones); `doc_table`.
- Model pages: `notebook_box` with `notebook_title`, and download links `notebook_button` / `notebook_button_alt`.
- Cards: `doc_cards` > `doc_card` > `doc_card_title` (links lists, used on Documentation and ecosystem pages).
- Team: `team_grid` > `team_card` (`team_photo`, `team_name`, `team_tagline` — playful taglines).
- Ecosystem pages: logo `<img class="eco_logo">` floated next to the first paragraph.

### Style and responsive rules

- Colours as CSS variables in `:root` (`--orange` #FF7F00, `--orange-dark` for links, `--text`, `--border`...).
- One breakpoint: `@media (max-width: 760px)` (two blocks in style.css). On phones: the menu is hidden, shown by the
  hamburger `#menu_toggle` (`toggle_menu()` / `set_menu_open()`), positioned just below the orange header line on the
  right; page titles get a right padding to avoid it; the content is full width (`#content` width 100%,
  `overflow-wrap: anywhere`), so nothing may be wider than the screen (wide content must scroll inside its box:
  `pre`, `df_wrapper`).
- Check phone rendering with headless Chromium (`/snap/bin/chromium --headless --screenshot`; it cannot go below
  ~500px wide), and check for horizontal overflow by comparing `scrollWidth` and `clientWidth` on every page.

## Notebooks

One notebook per model page (`files/<Model>/<Model>.ipynb`, `UPMaBoSS/*.ipynb`). They reproduce the figures of
their page, which are the PNGs saved in `figures/`. Each has a zip next to it (notebook + model files) for download.

Standards (asked by the maintainer):
- Keep them simple. Plot with the **built-in pyMaBoSS functions**: `plot_node_trajectory`, `plot_trajectory`,
  `plot_piechart`, and also `plot_entropy_trajectory`, `plot_fixpoint`, `plot_observed_graph`. Use a pandas plot
  only when nothing built-in fits (comparing several simulations on one axis, UPMaBoSS population ratios,
  Hamming distances...).
- One plot per figure (no multi-panel figures: they are unreadable on phones).
- Legends below the plot, horizontally, in centered rows of similar widths: call `legend_below()` before each
  `plt.savefig` of a figure with a legend. It is defined in the setup cell of every notebook (and in
  `tools/page_figures.py`); the copies must stay identical. It uses matplotlib internals (`_children` of the legend
  box) to center the rows.
- Setup cell: imports, `os.makedirs("figures", exist_ok=True)`, `plt.rcParams.update({"savefig.dpi": 150,
  "savefig.bbox": "tight", "figure.constrained_layout.use": True})`, `legend_below`. Figures are saved with
  `plt.savefig("figures/<name>.png")`.
- Markdown cells explain each step; the text of the page and of the notebook must agree with the results.

Running them:
- `python3 tools/run_notebooks.py <notebooks...>` executes in place with the conda env
  `~/.local/share/mamba/envs/profile` (pyMaBoSS 0.8.16, MaBoSS 2.6.6, MaBoSS_256n, pygraphviz), strips the
  "ipylab module is not installed" output, refreshes the zip, and deletes the UPMaBoSS run folders.
  The system Python lacks MaBoSS_256n and pygraphviz.
- Machine limits (see `~/.claude/CLAUDE.md`): run under a memory cap, e.g.
  `systemd-run --user --scope -q -p MemoryMax=8G -p MemorySwapMax=0 python3 tools/run_notebooks.py ...`, and keep
  to 10 cores: one batch of notebooks at a time (MaBoSS runs use `thread_count` 4 in Cell Cycle and Sizek, and the
  cfg values elsewhere). Peak memory of the notebooks has not been measured yet: pilot with `/usr/bin/time -v` first.
- UPMaBoSS reuses existing run folders (`WT/`, `NoFB/`, `WT_R1/`...): delete stale ones before a run.
  `CellFateModel_uppmaboss.ipynb` (mutant screen) takes 30-60 min; Drosophila ~4 min; others < 3 min.
- How To and Tutorials figures (`files/HowTo/pymaboss_*.png`, `files/ProstateCancer/pymaboss_{piechart,probtraj}.png`):
  `PATH=~/.local/share/mamba/envs/profile/bin:$PATH python tools/page_figures.py` (code identical to the pages).
- After changing figures: update the page text, remove figure files nothing references any more, check the
  pages on a phone width.

Model-specific notes:
- EGF-TNF: all nodes start inactive except EGF (0.5), to reproduce the publication; two fixed points.
- Drosophila: `get_fptable()` is not sorted (the expected patterning is FP 6); pattern pictures are drawn with a
  small `plot_pattern` helper; the noisy simulation declares all nodes internal to keep output files small.
- Prostate (133 nodes) needs MaBoSS_256n; compares conditions with stacked bars of final states (one color per state).
- Cell Cycle: the asymptotic behaviour is shown with `plot_piechart()` of the random-initial-condition run.

## Other facts

- Ecosystem pages: PROFILE, PhysiBoSS (figure `images/ecosystem/physicell_3.png` from the talks), UPMaBoSS,
  EnsembleMaBoSS, ExaStoLog (MATLAB toolbox, pyExaStoLog on PyPI, GPU version paraExaStoLog by A. Šmelko).
- Team page: Gautier Stoll, Laurence Calzone, Eric Viara, Vincent Noël. Proposed additions (from the publications)
  are pending a decision of the team: Emmanuel Barillot, Andrei Zinovyev, Arnau Montagud, Marco Ruscone,
  Adam Šmelko, Jonas Béal (runners-up: Aurélien Naldi, Gaëlle Letort, Mihály Koltai, Saran Pankaew).

## Open items

- `WebMaBoSS/index.html` and `webmaboss/index.html` have the `<title>` "UPMaBoSS" (copied from the UPMaBoSS stub).
- `images/ecosystem/physiboss_spheroid.png` is no longer used (replaced by `physicell_3.png`).
