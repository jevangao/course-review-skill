#!/usr/bin/env python3
"""Extract PPTX slide and speaker-note text with visual-review flags."""

from __future__ import annotations

import argparse
import json
import posixpath
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile
import xml.etree.ElementTree as ET

A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
REL_ATTR = f"{{{R_NS}}}id"
VISUAL_TAGS = {
    f"{{{P_NS}}}pic": "picture",
    f"{{{P_NS}}}graphicFrame": "chart_or_table",
    f"{{{P_NS}}}cxnSp": "connector",
}


def find_pptx(inputs: list[str]) -> list[Path]:
    sources: set[Path] = set()
    for raw in inputs:
        candidate = Path(raw).expanduser().resolve()
        if candidate.is_dir():
            sources.update(
                path.resolve()
                for path in candidate.rglob("*")
                if path.is_file() and not path.name.startswith("~$") and path.suffix.lower() == ".pptx"
            )
        elif candidate.is_file() and not candidate.name.startswith("~$") and candidate.suffix.lower() == ".pptx":
            sources.add(candidate)
    return sorted(sources, key=lambda path: str(path).casefold())


def normalize_target(base_entry: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(base_entry), target))


def relationship_targets(archive: ZipFile, rels_entry: str, base_entry: str) -> dict[str, tuple[str, str]]:
    try:
        root = ET.fromstring(archive.read(rels_entry))
    except KeyError:
        return {}
    targets: dict[str, tuple[str, str]] = {}
    for rel in root.findall(f"{{{REL_NS}}}Relationship"):
        rel_id = rel.attrib.get("Id", "")
        target = normalize_target(base_entry, rel.attrib.get("Target", ""))
        targets[rel_id] = (target, rel.attrib.get("Type", ""))
    return targets


def ordered_slides(archive: ZipFile) -> list[str]:
    root = ET.fromstring(archive.read("ppt/presentation.xml"))
    rels = relationship_targets(archive, "ppt/_rels/presentation.xml.rels", "ppt/presentation.xml")
    entries: list[str] = []
    slide_list = root.find(f"{{{P_NS}}}sldIdLst")
    for slide_id in list(slide_list) if slide_list is not None else []:
        target = rels.get(slide_id.attrib.get(REL_ATTR, ""), ("", ""))[0]
        if target:
            entries.append(target)
    return entries


def extract_paragraphs(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    lines: list[str] = []
    for paragraph in root.findall(f".//{{{A_NS}}}p"):
        text = "".join(node.text or "" for node in paragraph.findall(f".//{{{A_NS}}}t"))
        text = " ".join(text.split()).strip()
        if text:
            lines.append(text)
    return lines


def extract_notes_body(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    lines: list[str] = []
    for shape in root.findall(f".//{{{P_NS}}}sp"):
        placeholders = shape.findall(f".//{{{P_NS}}}ph")
        if not any(placeholder.attrib.get("type") == "body" for placeholder in placeholders):
            continue
        for paragraph in shape.findall(f".//{{{A_NS}}}p"):
            text = "".join(node.text or "" for node in paragraph.findall(f".//{{{A_NS}}}t"))
            text = " ".join(text.split()).strip()
            if text:
                lines.append(text)
    return lines


def notes_for_slide(archive: ZipFile, slide_entry: str) -> list[str]:
    slide_path = PurePosixPath(slide_entry)
    rels_entry = str(slide_path.parent / "_rels" / f"{slide_path.name}.rels")
    for target, rel_type in relationship_targets(archive, rels_entry, slide_entry).values():
        if rel_type.endswith("/notesSlide"):
            try:
                return extract_notes_body(archive.read(target))
            except KeyError:
                return []
    return []


def visual_kinds(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    kinds = {label for tag, label in VISUAL_TAGS.items() if root.findall(f".//{tag}")}
    return sorted(kinds)


def extract_deck(path: Path) -> dict:
    with ZipFile(path) as archive:
        pages: list[dict] = []
        for index, entry in enumerate(ordered_slides(archive), start=1):
            xml_bytes = archive.read(entry)
            lines = extract_paragraphs(xml_bytes)
            notes = notes_for_slide(archive, entry)
            visuals = visual_kinds(xml_bytes)
            pages.append(
                {
                    "page": index,
                    "entry": entry,
                    "text": lines,
                    "notes": notes,
                    "visual_elements": visuals,
                    "needs_visual_review": bool(visuals) or not lines,
                }
            )
    return {
        "path": str(path),
        "name": path.name,
        "page_count": len(pages),
        "visual_review_pages": [page["page"] for page in pages if page["needs_visual_review"]],
        "notes_page_count": sum(bool(page["notes"]) for page in pages),
        "pages": pages,
    }


def write_markdown(corpus: dict, output: Path) -> None:
    lines = [
        "# PPTX Text Corpus",
        "",
        f"- Source decks: {corpus['deck_count']}",
        f"- Slides: {corpus['slide_count']}",
        f"- Slides flagged for visual review: {corpus['visual_review_slide_count']}",
        "- Extraction: OOXML presentation order, paragraph text, and speaker notes where present.",
        "",
    ]
    for deck in corpus["decks"]:
        lines.extend(
            [
                f"## {deck['name']}",
                "",
                f"- Slides: {deck['page_count']}",
                f"- Visual-review flags: {len(deck['visual_review_pages'])}",
                f"- Slides with notes: {deck['notes_page_count']}",
                "",
            ]
        )
        for page in deck["pages"]:
            flag = " | visual review" if page["needs_visual_review"] else ""
            lines.append(f"### Slide {page['page']}{flag}")
            lines.extend(page["text"] or ["_No extractable slide text; inspect rendered page._"])
            if page["notes"]:
                lines.append("")
                lines.append("**Speaker notes**")
                lines.extend(page["notes"])
            lines.append("")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for extracted evidence.")
    parser.add_argument("sources", nargs="+", help="PPTX source files or directories.")
    args = parser.parse_args()

    sources = find_pptx(args.sources)
    if not sources:
        parser.error("No .pptx sources were found.")
    decks: list[dict] = []
    errors: list[dict] = []
    for path in sources:
        try:
            decks.append(extract_deck(path))
        except (BadZipFile, KeyError, ET.ParseError, OSError) as error:
            errors.append({"path": str(path), "error": str(error)})
    corpus = {
        "deck_count": len(decks),
        "slide_count": sum(deck["page_count"] for deck in decks),
        "visual_review_slide_count": sum(len(deck["visual_review_pages"]) for deck in decks),
        "errors": errors,
        "decks": decks,
    }
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "pptx-corpus.json"
    md_path = output_dir / "pptx-corpus.md"
    json_path.write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(corpus, md_path)
    print(f"{json_path}|{corpus['deck_count']}|{corpus['slide_count']}|{len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
