# Output Modes And Subject Adaptation

## Contents

- Default deliverables
- Output mode selection
- Recommended structure
- Subject adaptations
- Writing and attribution rules

## Default Deliverables

For a substantial slide collection, default to:

1. A detailed study guide in the user's language.
2. A short coverage and verification note listing sources, page counts, visual review scope, and limitations.

Offer additional products only when useful to the learning goal:

- rapid-review sheet for examination preparation;
- formulas, vocabulary, or key-case sheet;
- self-test questions or flashcard prompts;
- worked example workbook;
- teaching outline or lesson plan.

## Output Mode Selection

| User goal | Primary output | Useful additions |
| --- | --- | --- |
| Learn an unfamiliar course | Explanatory study guide ordered by prerequisites | Glossary, concept map, self-check |
| Prepare for an exam | Compressed review guide emphasizing tested operations | Formula sheet, common errors, practice checklist |
| Review a workshop/training | Action-oriented handbook | Process checklist, terminology table |
| Teach from supplied slides | Instructor outline | Learning objectives, example prompts, discussion questions |
| Build a question bank | Topic and objective map first | Questions tagged by source module and difficulty |

## Recommended Structure

Use this structure for a detailed Markdown guide, adapting labels to the language and subject:

```markdown
# <Course or Topic> Study Guide

## Sources And Coverage
## How To Use This Guide
## Course Map
## Core Modules
## Procedures, Formulas, Or Frameworks
## Comparison And Selection Tables
## Slide Conventions, Caveats, And Likely Errors
## Self-Test Or Practice Checklist
## Coverage Index
```

Use a shorter structure for rapid review:

```markdown
# <Course or Topic> Rapid Review

## Must-Know Concepts
## Formulas / Rules / Procedures
## Common Confusions
## Last-Minute Checklist
```

## Subject Adaptations

| Subject type | Extract and reorganize around | Verify visually |
| --- | --- | --- |
| Algorithms and computing | invariants, pseudocode, states, complexity, boundary cases | traces, diagrams, code snippets, tables |
| Mathematics and statistics | definitions, assumptions, theorems, proof ideas, example patterns | equations, plotted data, geometric figures |
| Science and engineering | models, units, experimental setups, causal relations, calculations | schematics, charts, apparatus, annotated formulas |
| Medicine and health education | terminology, pathways, diagnostic or clinical criteria as taught | anatomical figures, workflows, dosage tables; do not add medical advice |
| Law, policy, and management | distinctions, rule frameworks, cases, decision criteria | timelines, matrices, quoted provisions |
| Language and humanities | vocabulary, themes, grammar or rhetorical patterns, textual examples | annotated excerpts, maps, chronology |
| Product or professional training | workflows, responsibilities, tools, scenarios, compliance points | UI screenshots, process maps, dashboards |

## Writing And Attribution Rules

- Synthesize around learner needs rather than paraphrasing every slide.
- Treat repeated content and explicit review/objective pages as emphasis signals.
- Cite a source module or page when recording a disputed convention, possible typo, or especially consequential claim.
- Keep `slide convention`, `general enrichment`, and `needs verification` visually distinct.
- Do not introduce outside facts silently. Label outside knowledge as additional context.
- Avoid long verbatim copying; summarize and preserve only short labels, definitions, or formulas needed for learning.
