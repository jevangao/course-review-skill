---
name: course-slide-study-guide
description: Create verified study guides, review notes, summaries, cheat sheets, question banks, and learning materials from course, lecture, workshop, or training slide collections. Use when Codex needs to read one or many PPTX, PPT, PDF, or slide-export files; synthesize lessons into Markdown; extract formulas, terminology, algorithms, examples, or exam points; compare slide-specific claims with general knowledge; or preserve evidence for review.
---

# Course Slide Study Guide

Build learning material from slide sources with traceable evidence. Treat slides as authored course material: extract their claims faithfully, inspect visual pages before interpreting them, and distinguish source wording from outside corrections or enrichment.

## Operating Contract

1. Follow the user's language, learning goal, output depth, and requested format.
2. Preserve source files unless the user explicitly requests edits.
3. Keep an evidence workspace containing an inventory, extractable text, quality report, and visual review artifacts when the task involves more than a small deck.
4. State the number and types of sources covered in final study material.
5. Label statements distinctly when they differ:
   - `Slide convention`: wording, symbols, definitions, or constraints as taught.
   - `General note`: broader standard knowledge useful for learners.
   - `Needs verification`: likely typo, ambiguous diagram, unsupported visual, or conflict requiring caution.
6. Do not infer essential meaning from an image-heavy, diagram-heavy, animation-stage, table, chart, or formula page without visually inspecting it or declaring the limitation.

## Source Routing

| Source | Required acquisition route | Required visual route |
| --- | --- | --- |
| `.pptx` | Run `scripts/inventory_slides.py` and `scripts/extract_pptx_corpus.py` | Use an available presentation rendering workflow to render pages and contact sheets |
| `.pdf` slide export | Inventory it; use the PDF extraction workflow when available | Render pages/contact sheets using the PDF workflow |
| legacy `.ppt` | Inventory it and convert through an available presentation application, or request converted input if unavailable | Inspect converted rendering |
| online/slides link | Export or fetch a stable local copy when authorized, recording provenance | Render or inspect the stable copy |

For mixed collections, create one coverage index across every source type, even when only PPTX sources can use the bundled extractor directly.

## Evidence Workspace

Place artifacts under an output folder near the requested output or in a temporary workspace for read-only review:

```text
<output-root>/
├── evidence/
│   ├── source-inventory.json
│   ├── source-inventory.md
│   ├── pptx-corpus.json
│   ├── pptx-corpus.md
│   ├── coverage-report.md
│   └── visuals/<source>/contact-sheet.png
└── <requested learning outputs>.md
```

Keep evidence by default for substantial synthesis tasks. Remove it only when the user asks.

## Workflow

### 1. Clarify Output Without Stalling

Infer sensible defaults when the request is clear:

- Default language: the user's language.
- Default product: detailed Markdown study guide plus a short evidence/coverage note.
- Default audience: the learner reviewing the supplied slides.
- Default depth: organized synthesis, not slide-by-slide transcription.

Ask only when output purpose materially changes the result, or when authorization is needed to retrieve remote files.

### 2. Inventory All Sources

Run:

```bash
python3 scripts/inventory_slides.py --output-dir <evidence-dir> <source-path> [<source-path> ...]
```

Use counts and file types to determine processing routes. Inspect ordering rather than assuming filesystem order matches teaching order; infer chronology from filenames and titles where appropriate, and document uncertainty.

### 3. Extract Searchable PPTX Evidence

Run:

```bash
python3 scripts/extract_pptx_corpus.py --output-dir <evidence-dir> <pptx-or-directory> [<pptx-or-directory> ...]
```

The script resolves presentation slide order from OOXML relationships, reads text and speaker notes where present, flags visual pages, and writes Markdown plus JSON corpora. Use the corpus for reading and searching; never treat extraction alone as proof of diagram meaning.

For PDFs, use available PDF text extraction while retaining page numbers. For unconvertible `.ppt`, report it as uncovered evidence rather than silently skipping it.

### 4. Render And Review Visual Evidence

Render each relevant source or create equivalent page previews. Generate contact sheets for long collections. Prioritize detailed review of:

- pages flagged by the extractor as needing visual review;
- diagrams, algorithms, timelines, maps, charts, tables, formulas, code traces, and worked examples;
- slides with little text, unsupported embedded objects, or contradictory text;
- summary, learning objective, assignment, quiz, and review pages.

Read [references/visual-review.md](references/visual-review.md) for review strategy and failure handling.

### 5. Build A Knowledge Model

Before drafting, record:

- source sequence and topic map;
- learning objectives and repeated emphasis;
- definitions, conventions, formulas, procedures, examples, and assessment signals;
- source-specific terminology or notation;
- discrepancies, suspected errors, and pages requiring caution.

Do not merely concatenate slide bullets. Reorganize material around learning tasks and dependencies.

### 6. Produce Learning Outputs

Read [references/output-modes.md](references/output-modes.md) when selecting outputs or adapting to a subject. Produce only outputs that serve the request, commonly:

- detailed Markdown study guide;
- rapid-review sheet;
- concept/term glossary and formula sheet;
- worked-method or algorithm cards;
- self-test questions, flashcard prompts, or practice checklist;
- source coverage and verification note.

Every substantial guide should include navigation, module-by-module explanation, important conventions or uncertainties, a review checklist, and coverage information.

### 7. Verify Coverage And Accuracy

For PPTX sources, run:

```bash
python3 scripts/check_coverage.py \
  --inventory <evidence-dir>/source-inventory.json \
  --corpus <evidence-dir>/pptx-corpus.json \
  --output <evidence-dir>/coverage-report.md
```

Also verify manually:

- all intended sources are included or explicitly listed as unsupported/unavailable;
- claims involving visuals were inspected;
- formulas, numerical examples, notation, and conditions reflect source material;
- corrections and enrichment are not presented as if they appeared on slides;
- output paths, headings, links, and Markdown rendering are usable.

## Bundled Resources

- `scripts/inventory_slides.py`: recursively inventory `.pptx`, `.ppt`, and `.pdf` sources and count PPTX pages.
- `scripts/extract_pptx_corpus.py`: create page-level Markdown/JSON corpus from PPTX text and notes in presentation order, with visual-review flags.
- `scripts/check_coverage.py`: compare inventory with extracted PPTX evidence and produce a compact quality report.
- `references/output-modes.md`: output templates and subject-adaptive guidance.
- `references/visual-review.md`: visual inspection priorities, rendering expectations, and limitation reporting.
