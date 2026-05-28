#!/usr/bin/env python3
"""Check PPTX extraction coverage against a slide-source inventory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--corpus", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    inventory = load_json(args.inventory)
    corpus = load_json(args.corpus)
    expected = {item["path"]: item for item in inventory["files"] if item["type"] == "pptx"}
    extracted = {deck["path"]: deck for deck in corpus["decks"]}
    missing = sorted(set(expected) - set(extracted))
    unexpected = sorted(set(extracted) - set(expected))
    page_mismatch: list[str] = []
    for path in sorted(set(expected) & set(extracted)):
        if expected[path]["page_count"] != extracted[path]["page_count"]:
            page_mismatch.append(
                f"{Path(path).name}: inventory {expected[path]['page_count']}, corpus {extracted[path]['page_count']}"
            )
    extraction_errors = corpus.get("errors", [])
    passed = not missing and not unexpected and not page_mismatch and not extraction_errors
    non_pptx = [item for item in inventory["files"] if item["type"] != "pptx"]
    lines = [
        "# Slide Evidence Coverage Report",
        "",
        f"- Status: {'PASS' if passed else 'REVIEW REQUIRED'}",
        f"- Inventoried sources: {inventory['source_count']}",
        f"- Inventoried PPTX decks: {len(expected)}",
        f"- Extracted PPTX decks: {corpus['deck_count']}",
        f"- Extracted PPTX slides: {corpus['slide_count']}",
        f"- Pages flagged for visual review: {corpus['visual_review_slide_count']}",
        f"- Other sources requiring routed processing: {len(non_pptx)}",
        "",
        "## Exceptions",
        "",
    ]
    exceptions: list[str] = []
    exceptions.extend(f"- Missing extraction: `{path}`" for path in missing)
    exceptions.extend(f"- Not present in inventory: `{path}`" for path in unexpected)
    exceptions.extend(f"- Page mismatch: {message}" for message in page_mismatch)
    exceptions.extend(f"- Extraction error: `{item['path']}`: {item['error']}" for item in extraction_errors)
    if non_pptx:
        exceptions.extend(f"- Route separately as {item['type'].upper()}: `{item['path']}`" for item in non_pptx)
    lines.extend(exceptions or ["- None for PPTX extraction."])
    lines.extend(
        [
            "",
            "## Required Manual Checks",
            "",
            "- Render or otherwise inspect pages flagged for visual review before interpreting diagrams, charts, formulas, or staged examples.",
            "- Confirm any non-PPTX sources listed above are processed through their required route.",
            "- Separate slide-specific conventions, external enrichment, and unresolved ambiguities in final learning material.",
            "",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"{args.output.resolve()}|{'PASS' if passed else 'REVIEW REQUIRED'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
