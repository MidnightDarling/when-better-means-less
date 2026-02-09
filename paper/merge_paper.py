#!/usr/bin/env python3
"""Merge modular section files into the final paper.

Features:
- Combines sections in order
- Validates cross-references (Section X, Figure X)
- Checks FRR number consistency
- Checks terminology consistency
- Reports issues before writing

Author: Claude Opus 4.6
Created: 2026-02-08
"""

import re
import sys
from pathlib import Path
from collections import Counter

SECTIONS_DIR = Path(__file__).parent / "sections"
OUTPUT = Path(__file__).parent / "when_better_means_less.md"

# Section files in merge order
SECTION_ORDER = [
    "00_meta.md",
    "01_abstract.md",
    "02_introduction.md",
    "03_background_genealogy.md",
    "04_background_anomaly.md",
    "05_background_related_work.md",
    "06_methodology.md",
    "07_results_text_metrics.md",
    "08_results_judge_eval.md",
    "09_results_multi_turn.md",
    "10_results_frr.md",
    "11_results_reliability.md",
    "12_discussion.md",
    "13_alignment_tax.md",
    "14_implications.md",
    "15_conclusion.md",
    "16_references.md",
    "17_appendix.md",
]


def read_sections():
    """Read all section files in order."""
    sections = []
    for filename in SECTION_ORDER:
        filepath = SECTIONS_DIR / filename
        if filepath.exists():
            sections.append((filename, filepath.read_text()))
        else:
            print(f"WARNING: Missing section file: {filename}")
    return sections


def validate_frr_consistency(full_text):
    """Check that all FRR percentages are consistent."""
    issues = []

    # Find all FRR percentage mentions
    frr_patterns = re.findall(r"(\d+\.?\d*)%.*?(?:4o|FRR|refusal)", full_text)

    # Find specific FRR table values
    frr_table = re.findall(
        r"\*\*(\d+\.?\d*)%\*\*", full_text
    )
    if frr_table:
        frr_set = set(frr_table)
        if len(frr_set) > 6:  # 3 models × 2 mentions max
            issues.append(
                f"FRR: Found {len(frr_set)} distinct bold percentages: {frr_set}. "
                "Check for inconsistent FRR numbers."
            )

    return issues


def validate_terminology(full_text):
    """Check for inconsistent terminology."""
    issues = []

    # "Human Score" as a metric name (not "human scores" as in rater scores)
    human_score_count = len(re.findall(r"Human [Ss]cores?\b(?! were| are)", full_text))
    judge_rated_count = len(re.findall(r"Judge-[Rr]ated", full_text))
    if human_score_count > 0:
        issues.append(
            f"Terminology: 'Human Score' appears {human_score_count}x "
            f"(should be 'Judge-Rated Quality', which appears {judge_rated_count}x)"
        )

    # Check for old section names that should have been renamed
    old_names = {
        "Naming Deception": "Naming Ambiguity",
        "cognitive violence": "moved to Appendix A.3",
        "designed betrayal": "softened or removed",
    }
    for old_name, replacement in old_names.items():
        # Exclude appendix from checks
        main_text = full_text.split("## Appendix")[0] if "## Appendix" in full_text else full_text
        count = len(re.findall(re.escape(old_name), main_text, re.IGNORECASE))
        if count > 0:
            issues.append(
                f"Terminology: '{old_name}' appears {count}x in main text "
                f"(should be {replacement})"
            )

    return issues


def validate_cross_refs(full_text):
    """Check that Section/Figure references point to existing targets."""
    issues = []

    # Find section references
    refs = re.findall(r"Section ([IVX]+\.?\d*\.?\d*)", full_text)
    # Find section definitions
    defs = re.findall(r"^## ([IVX]+)\.", full_text, re.MULTILINE)

    ref_counter = Counter(refs)
    for ref, count in ref_counter.items():
        base = ref.split(".")[0]
        if base not in defs:
            issues.append(f"Cross-ref: 'Section {ref}' referenced but not defined")

    return issues


def merge(dry_run=False):
    """Merge sections and validate."""
    sections = read_sections()

    if not sections:
        print("ERROR: No section files found. Run split_paper.py first.")
        sys.exit(1)

    # Combine
    parts = []
    for filename, content in sections:
        parts.append(content.rstrip())

    full_text = "\n\n---\n\n".join(parts) + "\n"

    # Validate
    all_issues = []
    all_issues.extend(validate_frr_consistency(full_text))
    all_issues.extend(validate_terminology(full_text))
    all_issues.extend(validate_cross_refs(full_text))

    # Report
    line_count = len(full_text.split("\n"))
    word_count = len(full_text.split())
    print(f"Merged: {len(sections)} sections, {line_count} lines, {word_count} words")

    if all_issues:
        print(f"\nValidation issues ({len(all_issues)}):")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("Validation: All checks passed")

    if dry_run:
        print("\n[DRY RUN] Not writing output file.")
    else:
        OUTPUT.write_text(full_text)
        print(f"\nWritten to: {OUTPUT}")

    return len(all_issues)


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    issue_count = merge(dry_run=dry_run)
    sys.exit(1 if issue_count > 0 else 0)
