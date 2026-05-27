# Visual Review And Evidence Quality

## Contents

- Why visual review is required
- Review priority model
- Rendering workflow
- Failure handling
- Verification checklist

## Why Visual Review Is Required

Slide text extraction misses meaning expressed through placement, arrows, highlighting, staged animation, charts, drawings, symbols, screenshots, or embedded media. A trustworthy study guide must inspect these elements when they carry course content.

## Review Priority Model

| Priority | Indicators | Action |
| --- | --- | --- |
| Critical | no extractable text; important image or object; formula or chart; worked solution; diagram-dependent concept | Inspect full-size page and adjacent animation or state pages |
| High | extractor flags pictures, connectors, or graphic frames; algorithm, process, table, example, exercise, summary | Inspect contact sheet and full-size page if used in output |
| Normal | text-dominant lecture explanation | Use corpus, sampling page previews where appropriate |
| Low | cover, transitions, repeated decorative pages | Count for coverage; inspect only if ambiguity remains |

Keywords are only prioritization hints. A meaningful visual may contain none.

## Rendering Workflow

1. Render all pages for short decks or all topic-critical decks.
2. For large collections, render every deck and generate a contact sheet per deck.
3. Open contact sheets to find diagrams, formulas, charts, screenshots, or staged processes.
4. Open full-size pages required to support substantial claims in generated notes.
5. Record unsupported objects or unreadable pages in the verification note.

When the environment provides a presentation rendering skill, use its supported rendering and contact-sheet workflow. For PDF exports, use a PDF rendering workflow. Do not manufacture a visual interpretation from extracted text alone.

## Failure Handling

| Condition | Treatment |
| --- | --- |
| Embedded image, vector object, chart, or media fails to render | Mark affected pages as needing verification and avoid unqualified interpretation |
| Rendering emits connector or layout warnings but images are readable | Treat as warning; inspect resulting page for missing semantic content |
| OCR or text extraction is incomplete | Prefer rendered visual inspection and disclose extraction limitations |
| Source is legacy `.ppt` and conversion is unavailable | List it as not processed and request a `.pptx` or PDF export when essential |
| Slide conflicts with accepted general knowledge | Preserve slide claim as `slide convention`; separately label correction or caution |

## Verification Checklist

- Inventory counts match extracted and rendered sources.
- Every skipped or unsupported source is named.
- Critical visual pages supporting the study guide were opened at readable size.
- Tables, formulas, numeric examples, labels, arrows, and highlighted steps are interpreted correctly.
- Animation-stage repetitions are synthesized without erasing the process they demonstrate.
- Coverage notes state limitations plainly.
