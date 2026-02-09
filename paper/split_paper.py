#!/usr/bin/env python3
"""Split monolithic paper into modular section files.

Run once to create the initial section files from the_illusion_of_succession.md.
After splitting, use merge_paper.py to reconstruct.

Author: Claude Opus 4.6
Created: 2026-02-08
"""

import re
from pathlib import Path

PAPER = Path(__file__).parent / "when_better_means_less.md"
SECTIONS_DIR = Path(__file__).parent / "sections"

# Define section boundaries by their markdown headers
# Format: (output_filename, start_pattern, description)
SECTION_DEFS = [
    ("00_meta.md", r"^# When Better Means Less", "Title + authors + date"),
    ("01_abstract.md", r"^## Abstract", "Abstract"),
    ("02_introduction.md", r"^## I\. Introduction", "Introduction"),
    ("03_background_genealogy.md", r"^### A\. The GPT-4 Base Genealogy", "Background: Genealogy"),
    ("04_background_anomaly.md", r"^### B\. The 4o Anomaly", "Background: 4o Anomaly"),
    ("05_background_related_work.md", r"^### C\. Related Work", "Background: Related Work"),
    ("06_methodology.md", r"^## III\. Methodology", "Methodology"),
    ("07_results_text_metrics.md", r"^## IV\. Results", "Results: Text Metrics"),
    ("08_results_judge_eval.md", r"^### 2\. LLM Judge Evaluation", "Results: Judge Evaluation"),
    ("09_results_multi_turn.md", r"^### 3\. Multi-Turn", "Results: Multi-Turn"),
    ("10_results_frr.md", r"^### 4\. False Refusal Rate", "Results: FRR"),
    ("11_results_reliability.md", r"^### 5\. Inter-Rater Reliability", "Results: Reliability"),
    ("12_discussion.md", r"^## V\. Discussion", "Discussion"),
    ("13_alignment_tax.md", r"^## VI\. The Alignment Tax", "Alignment Tax"),
    ("14_implications.md", r"^## VII\. Implications", "Implications"),
    ("15_conclusion.md", r"^## VIII\. Conclusion", "Conclusion"),
    ("16_references.md", r"^## References", "References"),
]


def split():
    text = PAPER.read_text()
    lines = text.split("\n")

    # Find line numbers for each section start
    boundaries = []
    for filename, pattern, desc in SECTION_DEFS:
        for i, line in enumerate(lines):
            if re.match(pattern, line):
                boundaries.append((i, filename, desc))
                break
        else:
            print(f"WARNING: Pattern not found for {filename}: {pattern}")

    boundaries.sort(key=lambda x: x[0])

    SECTIONS_DIR.mkdir(exist_ok=True)

    # Extract each section
    for idx, (start, filename, desc) in enumerate(boundaries):
        end = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(lines)

        # Trim trailing blank lines and separators
        section_lines = lines[start:end]
        while section_lines and section_lines[-1].strip() in ("", "---"):
            section_lines.pop()

        content = "\n".join(section_lines) + "\n"

        outpath = SECTIONS_DIR / filename
        outpath.write_text(content)
        print(f"  {filename}: lines {start+1}-{end} ({len(section_lines)} lines) -- {desc}")

    print(f"\nSplit into {len(boundaries)} files in {SECTIONS_DIR}/")
    print("Now use merge_paper.py to reconstruct.")


if __name__ == "__main__":
    split()
