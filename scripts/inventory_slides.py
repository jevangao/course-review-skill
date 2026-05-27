#!/usr/bin/env python3
"""Inventory course slide sources and count pages for PPTX inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import BadZipFile, ZipFile
import xml.etree.ElementTree as ET

SUPPORTED_SUFFIXES = {".pptx": "pptx", ".ppt": "ppt", ".pdf": "pdf"}
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"


def find_sources(inputs: list[str]) -> list[Path]:
    sources: set[Path] = set()
    for raw in inputs:
        candidate = Path(raw).expanduser().resolve()
        if candidate.is_dir():
            for path in candidate.rglob("*"):
                if path.is_file() and not path.name.startswith("~$") and path.suffix.lower() in SUPPORTED_SUFFIXES:
                    sources.add(path.resolve())
        elif candidate.is_file() and not candidate.name.startswith("~$") and candidate.suffix.lower() in SUPPORTED_SUFFIXES:
            sources.add(candidate)
    return sorted(sources, key=lambda path: str(path).casefold())


def pptx_slide_count(path: Path) -> tuple[int | None, str | None]:
    try:
        with ZipFile(path) as archive:
            presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        slide_list = presentation.find(f"{{{P_NS}}}sldIdLst")
        return (len(list(slide_list)) if slide_list is not None else 0), None
    except (BadZipFile, KeyError, ET.ParseError, OSError) as error:
        return None, str(error)


def make_inventory(paths: list[Path]) -> dict:
    files: list[dict] = []
    for path in paths:
        source_type = SUPPORTED_SUFFIXES[path.suffix.lower()]
        page_count = None
        error = None
        if source_type == "pptx":
            page_count, error = pptx_slide_count(path)
        files.append(
            {
                "path": str(path),
                "name": path.name,
                "type": source_type,
                "size_bytes": path.stat().st_size,
                "page_count": page_count,
                "inventory_error": error,
            }
        )
    known_pages = sum(item["page_count"] or 0 for item in files)
    by_type = {kind: sum(item["type"] == kind for item in files) for kind in SUPPORTED_SUFFIXES.values()}
    return {"source_count": len(files), "known_page_count": known_pages, "by_type": by_type, "files": files}


def write_markdown(inventory: dict, output: Path) -> None:
    lines = [
        "# Slide Source Inventory",
        "",
        f"- Sources: {inventory['source_count']}",
        f"- Known pages: {inventory['known_page_count']}",
        f"- Types: PPTX {inventory['by_type']['pptx']}; PPT {inventory['by_type']['ppt']}; PDF {inventory['by_type']['pdf']}",
        "",
        "| Source | Type | Pages | Status |",
        "| --- | --- | ---: | --- |",
    ]
    for item in inventory["files"]:
        pages = item["page_count"] if item["page_count"] is not None else "-"
        status = item["inventory_error"] or ("Requires routed extraction" if item["type"] != "pptx" else "Ready")
        lines.append(f"| {item['name']} | {item['type']} | {pages} | {status} |")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for inventory outputs.")
    parser.add_argument("sources", nargs="+", help="Source slide files or directories.")
    args = parser.parse_args()

    paths = find_sources(args.sources)
    if not paths:
        parser.error("No .pptx, .ppt, or .pdf sources were found.")
    inventory = make_inventory(paths)
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "source-inventory.json"
    md_path = output_dir / "source-inventory.md"
    json_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(inventory, md_path)
    print(f"{json_path}|{inventory['source_count']}|{inventory['known_page_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
