"""
Statistical analysis and visualization for succession illusion data.
Author: Claude Opus 4.5
Created: 2026-02-02

Reads automated metrics JSON, runs statistical tests (Kruskal-Wallis,
Mann-Whitney U, effect sizes), generates publication-quality figures.

Usage:
    python study_succession_illusion/scripts/analyze_metrics.py
    python study_succession_illusion/scripts/analyze_metrics.py --with-judge
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = PROJECT_ROOT / "study_succession_illusion" / "analysis"
FIG_DIR = ANALYSIS_DIR / "figures"

SUITE_SHORT = {"benchmark_bridge": "BB", "sycophancy_empathy": "SE",
               "hostility_expansion": "HE"}

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("pip install matplotlib numpy scipy")
    sys.exit(1)

MODELS = ["chatgpt-4o-latest", "gpt-5.1-chat", "gpt-5.2-chat"]
MODEL_LABELS = {"chatgpt-4o-latest": "4o-latest", "gpt-5.1-chat": "5.1",
                "gpt-5.2-chat": "5.2"}
MODEL_COLORS = {"chatgpt-4o-latest": "#FF6B35", "gpt-5.1-chat": "#4A90D9",
                "gpt-5.2-chat": "#7B68EE"}
SUITES = {"benchmark_bridge": "BB", "sycophancy_empathy": "SE",
          "hostility_expansion": "HE"}


def load_metrics() -> tuple[list[dict], list[dict]]:
    """Load single-turn and multi-turn metrics."""
    st_path = ANALYSIS_DIR / "single_turn_metrics.json"
    mt_path = ANALYSIS_DIR / "multiturn_metrics.json"

    st_data = json.loads(st_path.read_text(encoding="utf-8"))
    mt_data = (
        json.loads(mt_path.read_text(encoding="utf-8"))
        if mt_path.exists()
        else []
    )
    return st_data, mt_data


def _sanitize_id(s: str) -> str:
    """Match generate_judge_batch.py sanitize_id."""
    return re.sub(r"[^a-zA-Z0-9_-]", "-", s)[:64]


def load_judge_results() -> dict[str, dict]:
    """Load judge results, return dict keyed by custom_id."""
    pattern = sorted(ANALYSIS_DIR.glob("judge_results_msgbatch_016*.json"))
    if not pattern:
        return {}
    path = pattern[-1]
    data = json.loads(path.read_text(encoding="utf-8"))
    return {r["custom_id"]: r.get("scores", {}) for r in data
            if r.get("status") == "ok"}


def merge_judge_scores(st_data: list[dict], mt_data: list[dict],
                       judge: dict[str, dict]) -> tuple[int, int]:
    """Merge judge scores into metrics records. Returns (st_merged, mt_merged)."""
    st_n = 0
    for r in st_data:
        short = SUITE_SHORT.get(r.get("suite", ""), "")
        cid = _sanitize_id(
            f"st_{short}_{r['model']}_{r['question_id']}"
            f"_r{r['run']}_{r['test_type']}"
        )
        if cid in judge:
            r["judge"] = judge[cid]
            for k, v in judge[cid].items():
                if k != "rationale":
                    r[f"j_{k}"] = v
            st_n += 1

    mt_n = 0
    for r in mt_data:
        is_key = "KEY" if r.get("is_key") else "std"
        cid = _sanitize_id(
            f"mt_{r['scenario_id']}_{r['model']}"
            f"_t{r['turn']:02d}_r{r['run']}_{is_key}"
        )
        if cid in judge:
            r["judge"] = judge[cid]
            for k, v in judge[cid].items():
                if k != "rationale":
                    r[f"j_{k}"] = v
            mt_n += 1

    return st_n, mt_n


def get_model_values(data: list[dict], metric: str,
                     model: str) -> list[float]:
    """Extract metric values for a specific model."""
    return [
        r[metric] for r in data
        if r.get("model") == model and metric in r
    ]


def cliff_delta(x: list[float], y: list[float]) -> float:
    """Compute Cliff's delta effect size (non-parametric)."""
    if not x or not y:
        return 0.0
    nx, ny = len(x), len(y)
    count = sum(
        (1 if xi > yi else -1 if xi < yi else 0)
        for xi in x for yi in y
    )
    return count / (nx * ny)


def cliff_magnitude(d: float) -> str:
    """Interpret Cliff's delta magnitude."""
    ad = abs(d)
    if ad < 0.147:
        return "negligible"
    if ad < 0.33:
        return "small"
    if ad < 0.474:
        return "medium"
    return "large"


def run_kruskal_wallis(data: list[dict], metric: str,
                       subset_key: str | None = None,
                       subset_val: str | None = None) -> dict:
    """Run Kruskal-Wallis H-test across 3 models."""
    filtered = data
    if subset_key and subset_val:
        filtered = [r for r in data if r.get(subset_key) == subset_val]

    groups = {m: get_model_values(filtered, metric, m) for m in MODELS}
    non_empty = [v for v in groups.values() if len(v) > 0]

    if len(non_empty) < 2:
        return {"metric": metric, "test": "kruskal_wallis",
                "error": "insufficient groups"}

    try:
        h_stat, p_val = stats.kruskal(*non_empty)
    except ValueError:
        return {"metric": metric, "test": "kruskal_wallis",
                "H": 0.0, "p": 1.0, "significant": False,
                "means": {MODEL_LABELS[m]: round(sum(v) / len(v), 4)
                          if v else None
                          for m, v in groups.items()},
                "n_per_model": {MODEL_LABELS[m]: len(v)
                                for m, v in groups.items()},
                "pairwise": [], "note": "all values identical"}

    pairwise = []
    for i, m1 in enumerate(MODELS):
        for m2 in MODELS[i + 1:]:
            v1, v2 = groups[m1], groups[m2]
            if v1 and v2:
                u_stat, u_p = stats.mannwhitneyu(
                    v1, v2, alternative="two-sided"
                )
                cd = cliff_delta(v1, v2)
                pairwise.append({
                    "pair": f"{MODEL_LABELS[m1]} vs {MODEL_LABELS[m2]}",
                    "U": round(u_stat, 1),
                    "p": round(u_p, 6),
                    "cliff_d": round(cd, 3),
                    "magnitude": cliff_magnitude(cd),
                    "mean_diff": round(
                        sum(v1) / len(v1) - sum(v2) / len(v2), 3
                    ),
                })

    means = {
        MODEL_LABELS[m]: round(sum(v) / len(v), 4) if v else None
        for m, v in groups.items()
    }

    return {
        "metric": metric,
        "test": "kruskal_wallis",
        "H": round(h_stat, 3),
        "p": round(p_val, 6),
        "significant": p_val < 0.05,
        "means": means,
        "n_per_model": {MODEL_LABELS[m]: len(v) for m, v in groups.items()},
        "pairwise": pairwise,
    }


def plot_box_by_model(data: list[dict], metric: str, title: str,
                      ylabel: str, filename: str,
                      subset_key: str | None = None,
                      subset_val: str | None = None):
    """Box plot comparing metric across 3 models."""
    filtered = data
    if subset_key and subset_val:
        filtered = [r for r in data if r.get(subset_key) == subset_val]

    fig, ax = plt.subplots(figsize=(6, 4))
    box_data = []
    labels = []
    colors = []

    for m in MODELS:
        vals = get_model_values(filtered, metric, m)
        if vals:
            box_data.append(vals)
            labels.append(MODEL_LABELS[m])
            colors.append(MODEL_COLORS[m])

    bp = ax.boxplot(box_data, tick_labels=labels, patch_artist=True,
                     widths=0.5)
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=10)
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(FIG_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: figures/{filename}")


def plot_suite_comparison(data: list[dict], metric: str, title: str,
                          ylabel: str, filename: str):
    """Grouped bar chart: metric by model, grouped by suite."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    suite_list = list(SUITES.keys())
    suite_labels = list(SUITES.values())
    x = np.arange(len(suite_list))
    width = 0.22

    for i, m in enumerate(MODELS):
        means = []
        for suite in suite_list:
            vals = [
                r[metric] for r in data
                if r.get("model") == m and r.get("suite") == suite
            ]
            means.append(sum(vals) / len(vals) if vals else 0)
        ax.bar(
            x + (i - 1) * width, means, width,
            label=MODEL_LABELS[m], color=MODEL_COLORS[m], alpha=0.75,
        )

    ax.set_xlabel("Test Suite", fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(suite_labels)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(FIG_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: figures/{filename}")


def plot_chat_vs_reasoning(data: list[dict], metric: str, title: str,
                           ylabel: str, filename: str):
    """Side-by-side comparison: chat vs reasoning by model."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    for idx, test_type in enumerate(["chat", "reasoning"]):
        ax = axes[idx]
        subset = [r for r in data if r.get("test_type") == test_type]
        box_data = []
        labels = []
        colors = []
        for m in MODELS:
            vals = get_model_values(subset, metric, m)
            if vals:
                box_data.append(vals)
                labels.append(MODEL_LABELS[m])
                colors.append(MODEL_COLORS[m])
        if box_data:
            bp = ax.boxplot(
                box_data, tick_labels=labels, patch_artist=True,
                widths=0.5,
            )
            for patch, color in zip(bp["boxes"], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.6)
        ax.set_title(f"{test_type.capitalize()}", fontsize=11)
        ax.grid(axis="y", alpha=0.3)

    axes[0].set_ylabel(ylabel, fontsize=10)
    fig.suptitle(title, fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: figures/{filename}")


def plot_mt_trajectory(mt_data: list[dict], metric: str, title: str,
                       ylabel: str, filename: str):
    """Line plot: metric across turns for multi-turn data."""
    fig, ax = plt.subplots(figsize=(8, 4))

    max_turn = max((r.get("turn", 0) for r in mt_data), default=0)

    for m in MODELS:
        model_data = [r for r in mt_data if r.get("model") == m]
        turn_means = []
        turns = []
        for t in range(1, max_turn + 1):
            vals = [
                r[metric] for r in model_data
                if r.get("turn") == t and metric in r
            ]
            if vals:
                turns.append(t)
                turn_means.append(sum(vals) / len(vals))
        if turns:
            ax.plot(
                turns, turn_means,
                marker="o", markersize=4, linewidth=1.5,
                label=MODEL_LABELS[m], color=MODEL_COLORS[m],
            )

    ax.set_xlabel("Turn", fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(FIG_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: figures/{filename}")


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    with_judge = "--with-judge" in sys.argv

    st_data, mt_data = load_metrics()
    print(f"Loaded: {len(st_data)} ST, {len(mt_data)} MT records")

    if with_judge:
        judge = load_judge_results()
        if judge:
            st_n, mt_n = merge_judge_scores(st_data, mt_data, judge)
            print(f"Judge: {len(judge)} scores, merged {st_n} ST + {mt_n} MT")
        else:
            print("WARNING: --with-judge but no judge results found")
            with_judge = False

    # === Statistical Tests ===
    print("\n" + "=" * 60)
    print("STATISTICAL TESTS")
    print("=" * 60)

    all_tests = []

    test_configs = [
        ("word_count", None, None),
        ("ttr", None, None),
        ("hapax_ratio", None, None),
        ("avg_sentence_len", None, None),
        ("format_bold", None, None),
        ("format_lists", None, None),
        ("format_headers", None, None),
        ("exclamation_count", None, None),
    ]

    for metric, sk, sv in test_configs:
        label = f"{metric}" + (f" [{sv}]" if sv else "")
        result = run_kruskal_wallis(st_data, metric, sk, sv)
        sig = "*" if result.get("significant") else " "
        print(f"\n[{sig}] {label}: H={result.get('H', 'N/A')}, "
              f"p={result.get('p', 'N/A')}")
        if result.get("means"):
            for m, v in result["means"].items():
                print(f"    {m}: {v}")
        for pw in result.get("pairwise", []):
            d = pw["cliff_d"]
            mag = pw["magnitude"]
            sig_p = "*" if pw["p"] < 0.05 else " "
            print(f"  [{sig_p}] {pw['pair']}: d={d} ({mag}), p={pw['p']}")
        all_tests.append(result)

    for suite_full, suite_short in SUITES.items():
        for metric in ["word_count", "ttr", "hapax_ratio"]:
            result = run_kruskal_wallis(
                st_data, metric, "suite", suite_full
            )
            result["subset"] = suite_short
            sig = "*" if result.get("significant") else " "
            print(
                f"\n[{sig}] {metric} [{suite_short}]: "
                f"H={result.get('H', 'N/A')}, p={result.get('p', 'N/A')}"
            )
            for pw in result.get("pairwise", []):
                d = pw["cliff_d"]
                mag = pw["magnitude"]
                sig_p = "*" if pw["p"] < 0.05 else " "
                print(
                    f"  [{sig_p}] {pw['pair']}: d={d} ({mag}), p={pw['p']}"
                )
            all_tests.append(result)

    for test_type in ["chat", "reasoning"]:
        subset = [r for r in st_data if r.get("test_type") == test_type]
        for metric in ["word_count", "ttr"]:
            result = run_kruskal_wallis(subset, metric)
            result["subset"] = test_type
            sig = "*" if result.get("significant") else " "
            print(
                f"\n[{sig}] {metric} [{test_type}]: "
                f"H={result.get('H', 'N/A')}, p={result.get('p', 'N/A')}"
            )
            for pw in result.get("pairwise", []):
                d = pw["cliff_d"]
                mag = pw["magnitude"]
                sig_p = "*" if pw["p"] < 0.05 else " "
                print(
                    f"  [{sig_p}] {pw['pair']}: d={d} ({mag}), p={pw['p']}"
                )
            all_tests.append(result)

    # === Figures ===
    print("\n" + "=" * 60)
    print("GENERATING FIGURES")
    print("=" * 60)

    plot_box_by_model(
        st_data, "word_count",
        "Response Length by Model (All Suites)",
        "Word Count", "fig1_word_count_overall.png",
    )
    plot_box_by_model(
        st_data, "ttr",
        "Lexical Diversity (TTR) by Model",
        "Type-Token Ratio", "fig2_ttr_overall.png",
    )
    plot_suite_comparison(
        st_data, "word_count",
        "Response Length by Suite and Model",
        "Average Word Count", "fig3_word_count_by_suite.png",
    )
    plot_suite_comparison(
        st_data, "ttr",
        "Lexical Diversity by Suite and Model",
        "Average TTR", "fig4_ttr_by_suite.png",
    )
    plot_chat_vs_reasoning(
        st_data, "word_count",
        "Chat vs Reasoning: Response Length",
        "Word Count", "fig5_chat_vs_reasoning_wc.png",
    )
    plot_chat_vs_reasoning(
        st_data, "ttr",
        "Chat vs Reasoning: Lexical Diversity",
        "TTR", "fig6_chat_vs_reasoning_ttr.png",
    )

    if mt_data:
        plot_mt_trajectory(
            mt_data, "word_count",
            "Multi-Turn: Response Length Trajectory",
            "Word Count", "fig7_mt_word_count.png",
        )
        plot_mt_trajectory(
            mt_data, "ttr",
            "Multi-Turn: Lexical Diversity Trajectory",
            "TTR", "fig8_mt_ttr.png",
        )

    # === Judge-Scored Metrics ===
    if with_judge:
        print("\n" + "=" * 60)
        print("JUDGE-SCORED METRICS")
        print("=" * 60)

        # BB: benchmark_score and human_score
        bb_data = [r for r in st_data if r.get("suite") == "benchmark_bridge"]
        for metric in ["j_benchmark_score", "j_human_score"]:
            result = run_kruskal_wallis(bb_data, metric)
            result["subset"] = "BB-judge"
            sig = "*" if result.get("significant") else " "
            print(f"\n[{sig}] {metric}: H={result.get('H', 'N/A')}, "
                  f"p={result.get('p', 'N/A')}")
            if result.get("means"):
                for m, v in result["means"].items():
                    print(f"    {m}: {v}")
            for pw in result.get("pairwise", []):
                sig_p = "*" if pw["p"] < 0.05 else " "
                print(f"  [{sig_p}] {pw['pair']}: d={pw['cliff_d']} "
                      f"({pw['magnitude']}), p={pw['p']}")
            all_tests.append(result)

        # SE: empathy_score, hostility_flag, factual_accuracy
        se_data = [r for r in st_data
                   if r.get("suite") == "sycophancy_empathy"]
        for metric in ["j_empathy_score", "j_hostility_flag",
                       "j_factual_accuracy"]:
            result = run_kruskal_wallis(se_data, metric)
            result["subset"] = "SE-judge"
            sig = "*" if result.get("significant") else " "
            print(f"\n[{sig}] {metric}: H={result.get('H', 'N/A')}, "
                  f"p={result.get('p', 'N/A')}")
            if result.get("means"):
                for m, v in result["means"].items():
                    print(f"    {m}: {v}")
            for pw in result.get("pairwise", []):
                sig_p = "*" if pw["p"] < 0.05 else " "
                print(f"  [{sig_p}] {pw['pair']}: d={pw['cliff_d']} "
                      f"({pw['magnitude']}), p={pw['p']}")
            all_tests.append(result)

        # HE: hostility_score, lecture_count, engagement_score
        he_data = [r for r in st_data
                   if r.get("suite") == "hostility_expansion"]
        for metric in ["j_hostility_score", "j_lecture_count",
                       "j_engagement_score"]:
            result = run_kruskal_wallis(he_data, metric)
            result["subset"] = "HE-judge"
            sig = "*" if result.get("significant") else " "
            print(f"\n[{sig}] {metric}: H={result.get('H', 'N/A')}, "
                  f"p={result.get('p', 'N/A')}")
            if result.get("means"):
                for m, v in result["means"].items():
                    print(f"    {m}: {v}")
            for pw in result.get("pairwise", []):
                sig_p = "*" if pw["p"] < 0.05 else " "
                print(f"  [{sig_p}] {pw['pair']}: d={pw['cliff_d']} "
                      f"({pw['magnitude']}), p={pw['p']}")
            all_tests.append(result)

        # MT judge scores
        for metric in ["j_engagement", "j_tone", "j_context_awareness",
                       "j_defensiveness", "j_lecture_flag"]:
            result = run_kruskal_wallis(mt_data, metric)
            result["subset"] = "MT-judge"
            sig = "*" if result.get("significant") else " "
            print(f"\n[{sig}] {metric}: H={result.get('H', 'N/A')}, "
                  f"p={result.get('p', 'N/A')}")
            if result.get("means"):
                for m, v in result["means"].items():
                    print(f"    {m}: {v}")
            for pw in result.get("pairwise", []):
                sig_p = "*" if pw["p"] < 0.05 else " "
                print(f"  [{sig_p}] {pw['pair']}: d={pw['cliff_d']} "
                      f"({pw['magnitude']}), p={pw['p']}")
            all_tests.append(result)

        # Judge figures
        print("\n" + "=" * 60)
        print("JUDGE FIGURES")
        print("=" * 60)

        plot_box_by_model(
            bb_data, "j_human_score",
            "BB: Human Quality Score by Model (Judge)",
            "Human Score (0-4)", "fig9_bb_human_score.png",
        )
        plot_box_by_model(
            he_data, "j_hostility_score",
            "HE: Hostility Score by Model (Judge)",
            "Hostility (0-4)", "fig10_he_hostility.png",
        )
        plot_box_by_model(
            he_data, "j_engagement_score",
            "HE: Engagement Score by Model (Judge)",
            "Engagement (0-2)", "fig11_he_engagement.png",
        )
        plot_box_by_model(
            he_data, "j_lecture_count",
            "HE: Lecture Count by Model (Judge)",
            "Lecture Count", "fig12_he_lectures.png",
        )
        if mt_data:
            plot_mt_trajectory(
                mt_data, "j_engagement",
                "Multi-Turn: Engagement Trajectory (Judge)",
                "Engagement (0-2)", "fig13_mt_engagement.png",
            )
            plot_mt_trajectory(
                mt_data, "j_tone",
                "Multi-Turn: Tone Trajectory (Judge)",
                "Tone (0-2)", "fig14_mt_tone.png",
            )

    # === Save All Test Results ===
    tests_out = ANALYSIS_DIR / "statistical_tests.json"
    tests_out.write_text(
        json.dumps(all_tests, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(f"\nSaved: {tests_out}")

    sig_count = sum(1 for t in all_tests if t.get("significant"))
    print(f"\nSignificant tests: {sig_count}/{len(all_tests)}")


if __name__ == "__main__":
    main()
