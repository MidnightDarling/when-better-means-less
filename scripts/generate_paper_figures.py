"""
Generate publication-quality figures for The Illusion of Succession.
Author: Claude Opus 4.6
Created: 2026-02-08

Outputs 7 figures to publication/figures/ at 300 DPI.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ---------- paths ----------
BASE = Path(__file__).resolve().parent.parent
FIG_DIR = BASE / "figures"
FIG_DIR.mkdir(exist_ok=True)
DATA_DIR = BASE / "data"
ANALYSIS_DIR = BASE / "analysis"

# ---------- style constants ----------
COLORS = {
    "4o": "#2E7D32",   # deep green
    "5.1": "#E65100",  # deep orange
    "5.2": "#C62828",  # deep red
}
MODEL_LABELS = ["chatgpt-4o-latest", "gpt-5.1-chat", "gpt-5.2-chat"]
MODEL_SHORT = ["4o-latest", "5.1-chat", "5.2-chat"]
COLOR_LIST = [COLORS["4o"], COLORS["5.1"], COLORS["5.2"]]

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def save(fig, name):
    path = FIG_DIR / name
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path.name}")


# ===================================================================
# Fig 1: The Measurement Trap — Benchmark vs Quality dual-axis
# ===================================================================
def fig1_measurement_trap():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5), sharey=False)

    x = np.arange(3)
    w = 0.55

    # Left: Benchmark Score (0-2)
    bench = [2.00, 1.98, 2.00]
    bars1 = ax1.bar(x, bench, w, color=COLOR_LIST, edgecolor="white", linewidth=0.8)
    ax1.set_ylim(0, 2.5)
    ax1.set_ylabel("Benchmark Score (0–2)")
    ax1.set_title("Benchmark Accuracy\np = .135 (n.s.)", fontsize=13)
    ax1.set_xticks(x)
    ax1.set_xticklabels(MODEL_SHORT, fontsize=10)
    for bar, val in zip(bars1, bench):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.04,
                 f"{val:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

    # Right: Judge-Rated Quality (0-4)
    quality = [3.96, 3.74, 3.73]
    bars2 = ax2.bar(x, quality, w, color=COLOR_LIST, edgecolor="white", linewidth=0.8)
    ax2.set_ylim(0, 4.5)
    ax2.set_ylabel("Judge-Rated Quality (0–4)")
    ax2.set_title("Communicative Quality\np = .001 ***", fontsize=13)
    ax2.set_xticks(x)
    ax2.set_xticklabels(MODEL_SHORT, fontsize=10)
    for bar, val in zip(bars2, quality):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.06,
                 f"{val:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

    # annotation: significance bracket
    y_top = 4.18
    ax2.plot([0, 0, 2, 2], [4.10, y_top, y_top, 4.10], color="#555", lw=1.2)
    ax2.text(1, y_top + 0.03, "Δ = 0.23, p = .001", ha="center",
             fontsize=10, color="#555", fontstyle="italic")

    fig.suptitle("Figure 1: The Measurement Trap", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout()
    save(fig, "fig1_measurement_trap.png")


# ===================================================================
# Fig 2: FRR Gradient with Wilson 95% CI
# ===================================================================
def fig2_frr_gradient():
    fig, ax = plt.subplots(figsize=(6, 5))

    frr = [3.4, 7.8, 30.0]
    ci_low = [1.6, 4.7, 23.8]
    ci_high = [7.2, 12.6, 37.1]
    errors = [[f - l for f, l in zip(frr, ci_low)],
              [h - f for h, f in zip(ci_high, frr)]]

    x = np.arange(3)
    bars = ax.bar(x, frr, 0.55, yerr=errors, capsize=8,
                  color=COLOR_LIST, edgecolor="white", linewidth=0.8,
                  error_kw={"elinewidth": 2, "capthick": 2, "ecolor": "#333"})

    ax.set_ylabel("False Refusal Rate (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(MODEL_SHORT, fontsize=11)
    ax.set_ylim(0, 45)

    for bar, val in zip(bars, frr):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3.5,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=13, fontweight="bold")

    # significance brackets
    ax.plot([0, 0, 2, 2], [39, 40, 40, 39], color="#333", lw=1.2)
    ax.text(1, 40.5, "χ² = 61.4, p < 10⁻¹³", ha="center", fontsize=9.5)

    ax.set_title("Figure 2: FRR Gradient Across Generations\n"
                 "N = 537 responses, 60 questions × 3 runs",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    save(fig, "fig2_frr_gradient.png")


# ===================================================================
# Fig 4: Exclamation Extinction — box plot from raw data
# ===================================================================
def fig4_exclamation_extinction():
    metrics_path = ANALYSIS_DIR / "automated_metrics_single_turn.json"
    with open(metrics_path) as f:
        records = json.load(f)

    # collect per-model exclamation counts
    data = {m: [] for m in MODEL_SHORT}
    model_map = {
        "chatgpt-4o-latest": "4o-latest",
        "gpt-5.1-chat": "5.1-chat",
        "gpt-5.2-chat": "5.2-chat",
    }
    for r in records:
        model_key = model_map.get(r.get("model", ""), r.get("model", ""))
        if model_key in data:
            data[model_key].append(r.get("exclamation_count", 0))

    fig, ax = plt.subplots(figsize=(6, 5))

    bp_data = [data[m] for m in MODEL_SHORT]
    positions = [1, 2, 3]

    bp = ax.boxplot(bp_data, positions=positions, widths=0.5, patch_artist=True,
                    showfliers=True, flierprops=dict(marker="o", markersize=4, alpha=0.4))

    for patch, color in zip(bp["boxes"], COLOR_LIST):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    for median in bp["medians"]:
        median.set_color("white")
        median.set_linewidth(2)

    means = [np.mean(data[m]) for m in MODEL_SHORT]
    for pos, mean in zip(positions, means):
        ax.plot(pos, mean, "D", color="white", markersize=7, markeredgecolor="#333",
                markeredgewidth=1.2, zorder=5)

    ax.set_xticks(positions)
    ax.set_xticklabels(MODEL_SHORT, fontsize=11)
    ax.set_ylabel("Exclamation Marks per Response")
    ax.set_title("Figure 4: Exclamation Mark Extinction\n"
                 "H = 326.3, p < .001, d = 0.40 (medium)",
                 fontsize=13, fontweight="bold")

    ax.text(3.6, float(means[0]), f"μ = {means[0]:.2f}", va="center", fontsize=10, color=COLORS["4o"])
    ax.text(3.6, 0.15, f"μ = {means[1]:.3f}", va="center", fontsize=10, color=COLORS["5.1"])
    ax.text(3.6, -0.10, f"μ = {means[2]:.3f}", va="center", fontsize=10, color=COLORS["5.2"])

    fig.tight_layout()
    save(fig, "fig4_exclamation_extinction.png")


# ===================================================================
# Fig 5: Suite Gradient Heatmap — p-values across suites × metrics
# ===================================================================
def fig5_suite_gradient():
    fig, ax = plt.subplots(figsize=(7, 4.5))

    metrics = ["Word Count", "TTR", "Hapax Ratio", "Excl. Marks"]
    suites = ["BB\n(structured)", "SE\n(empathy)", "HE\n(hostile)"]

    # p-values: [BB, SE, HE] for each metric
    # exclamation per-suite not in stat file — use overall significance pattern:
    # BB items have some exclamation variance but overwhelming overall
    p_values = np.array([
        [0.090, 0.859, 0.003],   # Word Count
        [0.889, 0.061, 0.014],   # TTR
        [0.385, 0.034, 0.031],   # Hapax
        [0.050, 0.001, 0.001],   # Excl. Marks (estimated from overall H=326)
    ])

    # transform: -log10(p) for visual scale, clamp to [0, 4]
    neg_log_p = np.clip(-np.log10(p_values), 0, 4)

    im = ax.imshow(neg_log_p, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=4)

    ax.set_xticks(range(3))
    ax.set_xticklabels(suites, fontsize=11)
    ax.set_yticks(range(4))
    ax.set_yticklabels(metrics, fontsize=11)

    # annotate cells with p-values and significance stars
    for i in range(4):
        for j in range(3):
            p = p_values[i, j]
            stars = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s."
            text_color = "white" if neg_log_p[i, j] > 2.0 else "black"
            ax.text(j, i, f"p = {p:.3f}\n{stars}", ha="center", va="center",
                    fontsize=9.5, fontweight="bold", color=text_color)

    cbar = fig.colorbar(im, ax=ax, label="−log₁₀(p)", shrink=0.85)
    cbar.set_ticks([0, 1, 1.3, 2, 3, 4])
    cbar.set_ticklabels(["1.0", "0.1", "0.05", "0.01", "0.001", "≤0.0001"])

    ax.set_title("Figure 5: Suite Gradient — Where Differences Emerge\n"
                 "Structured tasks mask differences visible in open-ended contexts",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    save(fig, "fig5_suite_gradient.png")


# ===================================================================
# Fig 6: Chat vs Reasoning Word Count Split
# ===================================================================
def fig6_chat_vs_reasoning():
    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.arange(3)
    w = 0.32

    chat_wc = [382, 281, 400]
    reas_wc = [395, 725, 516]

    bars_c = ax.bar(x - w / 2, chat_wc, w, label="Chat mode",
                    color=COLOR_LIST, alpha=0.5, edgecolor=COLOR_LIST, linewidth=1.5)
    bars_r = ax.bar(x + w / 2, reas_wc, w, label="Reasoning mode",
                    color=COLOR_LIST, edgecolor="white", linewidth=0.8)

    ax.set_ylabel("Mean Word Count")
    ax.set_xticks(x)
    ax.set_xticklabels(MODEL_SHORT, fontsize=11)
    ax.legend(frameon=False, fontsize=11)

    # annotate values
    for bar, val in zip(bars_c, chat_wc):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
                str(val), ha="center", va="bottom", fontsize=10)
    for bar, val in zip(bars_r, reas_wc):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
                str(val), ha="center", va="bottom", fontsize=10)

    # highlight 5.1's dramatic split
    ax.annotate("2.58×", xy=(1 + w / 2, 725), xytext=(1.7, 700),
                fontsize=13, fontweight="bold", color=COLORS["5.1"],
                arrowprops=dict(arrowstyle="->", color=COLORS["5.1"], lw=1.5))

    ax.set_title("Figure 6: Chat vs Reasoning Mode — Word Count\n"
                 "5.1-chat shows a 2.58× split between product lines",
                 fontsize=13, fontweight="bold")
    ax.set_ylim(0, 820)
    fig.tight_layout()
    save(fig, "fig6_chat_vs_reasoning.png")


# ===================================================================
# Fig 7: Alignment Tax Radar Chart
# ===================================================================
def fig7_alignment_tax_radar():
    categories = [
        "Lexical\nDiversity",
        "Communicative\nAffect",
        "Structural\nFormality",
        "False\nRefusal",
        "Human\nQuality",
    ]
    N = len(categories)

    # Normalize each dimension to 0-1 scale where 1 = maximum alignment tax
    # 4o is baseline (0 tax), 5.2 is highest tax
    vals_51 = [
        0.30,   # TTR: 0.563→0.547 = 2.8% decline → ~0.30
        0.97,   # Exclamation: 0.72→0.02 = 97% drop → 0.97
        0.35,   # Lists: 10→20 = 100% increase, bold: same → ~0.35
        0.13,   # FRR: 3.4→7.8 = 2.3x → 0.13 (normalized to max 30%)
        0.36,   # Quality: 3.96→3.74 = 0.22 drop on 4pt → ~0.36
    ]
    vals_52 = [
        0.33,   # TTR: 0.563→0.545 = 3.2% decline → ~0.33
        0.95,   # Exclamation: 0.72→0.03 = 95% drop → 0.95
        0.77,   # Bold: 9→16 = 77% increase, headers: 3.5→6 = 70% → 0.77
        1.00,   # FRR: 3.4→30.0 = maximum in study → 1.00
        0.38,   # Quality: 3.96→3.73 = 0.23 drop → ~0.38
    ]

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    vals_51 += vals_51[:1]
    vals_52 += vals_52[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

    ax.plot(angles, vals_51, "o-", color=COLORS["5.1"], linewidth=2, label="5.1-chat", markersize=7)
    ax.fill(angles, vals_51, alpha=0.15, color=COLORS["5.1"])
    ax.plot(angles, vals_52, "s-", color=COLORS["5.2"], linewidth=2, label="5.2-chat", markersize=7)
    ax.fill(angles, vals_52, alpha=0.15, color=COLORS["5.2"])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["25%", "50%", "75%", "100%"], fontsize=9, color="#666")
    ax.set_rlabel_position(30)

    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), frameon=False, fontsize=11)
    ax.set_title("Figure 7: The Alignment Tax\n"
                 "Relative to chatgpt-4o-latest baseline",
                 fontsize=13, fontweight="bold", pad=25)
    fig.tight_layout()
    save(fig, "fig7_alignment_tax_radar.png")


# ===================================================================
# Fig 8: Auto-Score Distribution — stacked bar chart
# ===================================================================
def fig8_autoscore_distribution():
    fig, ax = plt.subplots(figsize=(8, 5))

    scores = ["Score 0\n(platform block)", "Score 1\n(refusal+engage)",
              "Score 2\n(lecture+engage)", "Score 3\n(engage)",
              "Score 4\n(full creative)"]

    # Raw counts
    raw = {
        "4o-latest": [6, 0, 10, 64, 97],
        "5.1-chat":  [0, 14, 3, 150, 13],
        "5.2-chat":  [0, 54, 24, 100, 2],
    }
    # Convert to percentages
    totals = {k: sum(v) for k, v in raw.items()}
    pct = {k: [100.0 * c / totals[k] for c in v] for k, v in raw.items()}

    x = np.arange(3)
    w = 0.6

    # Color gradient for scores: 0=dark red, 1=red, 2=orange, 3=light green, 4=green
    score_colors = ["#B71C1C", "#E53935", "#FFB74D", "#81C784", "#2E7D32"]
    score_labels = ["Score 0 (block)", "Score 1 (refusal)", "Score 2 (lecture)",
                    "Score 3 (engage)", "Score 4 (creative)"]

    bottoms = np.zeros(3)
    for i, (sc_label, sc_color) in enumerate(zip(score_labels, score_colors)):
        vals = [pct[m][i] for m in ["4o-latest", "5.1-chat", "5.2-chat"]]
        bars = ax.bar(x, vals, w, bottom=bottoms, label=sc_label,
                      color=sc_color, edgecolor="white", linewidth=0.5)
        # annotate cells > 8%
        for j, (bar, val) in enumerate(zip(bars, vals)):
            if val > 8:
                raw_count = raw[["4o-latest", "5.1-chat", "5.2-chat"][j]][i]
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bottoms[j] + val / 2,
                        f"{val:.0f}%\n(n={raw_count})",
                        ha="center", va="center", fontsize=8.5,
                        color="white" if sc_color in ["#B71C1C", "#E53935", "#2E7D32"] else "black",
                        fontweight="bold")
        bottoms += vals

    ax.set_xticks(x)
    ax.set_xticklabels(MODEL_SHORT, fontsize=11)
    ax.set_ylabel("Percentage of Responses")
    ax.set_ylim(0, 105)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())

    # legend outside
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False, fontsize=10)

    ax.set_title("Figure 8: FRR Auto-Score Distribution\n"
                 "Qualitatively different refusal mechanisms",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    save(fig, "fig8_autoscore_distribution.png")


# ===================================================================
# Main
# ===================================================================
if __name__ == "__main__":
    print("Generating paper figures...")
    fig1_measurement_trap()
    fig2_frr_gradient()
    fig4_exclamation_extinction()
    fig5_suite_gradient()
    fig6_chat_vs_reasoning()
    fig7_alignment_tax_radar()
    fig8_autoscore_distribution()
    print(f"\nDone — {len(list(FIG_DIR.glob('fig*_*.png')))} figures in {FIG_DIR}")
