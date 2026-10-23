"""Figures of the How To and Tutorials pages, made with the code shown on the pages.

Usage, with the conda environment of the notebooks (see tools/run_notebooks.py) first in the PATH:
    PATH=~/.local/share/mamba/envs/profile/bin:$PATH python tools/page_figures.py

The code below must stay identical to the code shown on the pages, except legend_below(), which is the
helper of the notebooks (keep the copies identical).
"""
import math
import os
import maboss
import matplotlib.pyplot as plt
from matplotlib.offsetbox import HPacker

plt.rcParams.update({"savefig.dpi": 150, "savefig.bbox": "tight", "figure.constrained_layout.use": True})


def legend_below():
    """Move the legend of the current figure below the plot, in centered rows of similar widths."""
    figure, legend = plt.gcf(), plt.gca().get_legend()
    handles, labels = legend.legend_handles, [text.get_text() for text in legend.get_texts()]
    legend.remove()
    legend = figure.legend(handles, labels, loc="outside lower center", ncols=1)
    # Matplotlib fills the rows from the left: we rearrange the entries of the legend in centered rows,
    # as few as possible within the width of the plot, and of similar widths
    column = legend._legend_handle_box.get_children()[0]
    entries, column.align = column.get_children(), "center"
    sep = legend.columnspacing * legend.prop.get_size_in_points() * figure.dpi / 72
    widths = [entry.get_bbox(figure.canvas.get_renderer()).width + sep for entry in entries]
    max_width = 0.8 * figure.get_figwidth() * figure.dpi
    for n_rows in range(math.ceil(sum(widths) / max_width), len(entries) + 1):
        rows, row_widths = [[]], [0]
        for entry, width in zip(entries, widths):
            if rows[-1] and row_widths[-1] + width / 2 > sum(widths) / n_rows:
                rows.append([])
                row_widths.append(0)
            rows[-1].append(entry)
            row_widths[-1] += width
        if max(row_widths) <= max_width:
            break
    column._children = [HPacker(sep=sep, align="baseline", children=row) for row in rows]


html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "html")

# How To: the p53/Mdm2 example
sim = maboss.load(f"{html}/pub/example.bnd", f"{html}/pub/example.cfg")
sim.network.set_istate(["p53_b1", "p53_b2"], {(0, 0): 1, (1, 0): 0, (1, 1): 0})
sim.network.set_istate("Mdm2cyt", [1, 0])
sim.network.set_istate("Mdm2nuc", [1, 0])
sim.network.set_istate("DNAdam", [0.4, 0.6])
sim.update_parameters(max_time=4, sample_count=10000)
res = sim.run()
res.plot_node_trajectory(); legend_below(); plt.savefig(f"{html}/files/HowTo/pymaboss_node_trajectory.png")
res.plot_trajectory(); legend_below(); plt.savefig(f"{html}/files/HowTo/pymaboss_trajectory.png")
res.plot_piechart(); legend_below(); plt.savefig(f"{html}/files/HowTo/pymaboss_piechart.png")
mutant = maboss.copy_and_mutate(sim, ["Mdm2nuc"], "ON")
mutant_res = mutant.run()
mutant_res.plot_piechart(); legend_below(); plt.savefig(f"{html}/files/HowTo/pymaboss_mutant_piechart.png")

# Tutorials: the prostate cancer model
model = maboss.load(f"{html}/files/ProstateCancer/Montagud2022_Prostate_Cancer.bnd",
                    f"{html}/files/ProstateCancer/Montagud2022_Prostate_Cancer.cfg")
result = model.run()
result.plot_piechart(); legend_below(); plt.savefig(f"{html}/files/ProstateCancer/pymaboss_piechart.png")
result.plot_trajectory(); legend_below(); plt.savefig(f"{html}/files/ProstateCancer/pymaboss_probtraj.png")
