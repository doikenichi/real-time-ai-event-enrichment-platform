"""Recursively convert PDF files to adjacent HTML files."""

from __future__ import annotations

import argparse
import html
import os
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from xml.etree import ElementTree


HtmlRenderer = Callable[[Path], str]


@dataclass(frozen=True)
class ConversionSummary:
    """Outcome counts for one directory-tree conversion."""

    converted: int
    skipped: int
    failed: tuple[tuple[Path, str], ...]


def discover_pdfs(root: Path) -> list[Path]:
    """Return PDFs below *root* in deterministic order."""
    if not root.exists():
        raise ValueError(f"root does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"root is not a directory: {root}")

    pdfs = (
        path
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink() and path.suffix.lower() == ".pdf"
    )
    return sorted(pdfs, key=lambda path: path.relative_to(root).as_posix().casefold())


def _xhtml_body(fragment: str) -> str:
    """Remove PyMuPDF's per-page wrapper while retaining semantic children."""
    try:
        wrapper = ElementTree.fromstring(fragment)
    except ElementTree.ParseError:
        return fragment

    leading_text = html.escape(wrapper.text) if wrapper.text else ""
    children = "".join(
        ElementTree.tostring(child, encoding="unicode", method="html")
        for child in wrapper
    )
    return leading_text + children


def _toc_html(entries: list[list[Any]], page_count: int) -> str:
    items: list[str] = []
    for entry in entries:
        if len(entry) < 3:
            continue
        level, label, page_number = entry[:3]
        if not isinstance(page_number, int) or not 1 <= page_number <= page_count:
            continue
        safe_label = html.escape(str(label))
        safe_level = max(1, min(int(level), 6)) if isinstance(level, int) else 1
        items.append(
            f'<li class="toc-level-{safe_level}">'
            f'<a href="#page-{page_number}">{safe_label}</a></li>'
        )
    if not items:
        return ""
    return (
        '<nav class="toc" aria-labelledby="toc-heading">'
        '<h2 id="toc-heading">Contents</h2><ol>'
        + "".join(items)
        + "</ol></nav>"
    )


def _page_navigation_html(page_count: int) -> str:
    links = "".join(
        f'<li><a href="#page-{number}">Page {number}</a></li>'
        for number in range(1, page_count + 1)
    )
    return (
        '<nav class="page-navigation" aria-labelledby="pages-heading">'
        '<h2 id="pages-heading">Pages</h2><ol>'
        f"{links}</ol></nav>"
    )


def _safe_uri(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    candidate = value.strip()
    try:
        scheme = urlsplit(candidate).scheme.lower()
    except ValueError:
        return None
    return candidate if scheme in {"http", "https", "mailto"} else None


def _link_references_html(
    pages: list[Any], *, page_count: int, pymupdf_module: Any
) -> str:
    references: list[str] = []
    seen: set[tuple[int, str]] = set()

    for source_index, page in enumerate(pages, start=1):
        for link in page.get_links():
            target: str | None = None
            label: str | None = None
            if link.get("kind") == pymupdf_module.LINK_URI:
                uri = _safe_uri(link.get("uri"))
                if uri is not None:
                    target = uri
                    label = uri
            elif link.get("kind") == pymupdf_module.LINK_GOTO:
                destination = link.get("page")
                if isinstance(destination, int) and 0 <= destination < page_count:
                    target = f"#page-{destination + 1}"
                    label = f"Page {destination + 1}"

            if target is None or label is None or (source_index, target) in seen:
                continue
            seen.add((source_index, target))
            references.append(
                f'<li><span>Page {source_index}:</span> '
                f'<a href="{html.escape(target, quote=True)}">'
                f"{html.escape(label)}</a></li>"
            )

    if not references:
        return ""
    return (
        '<section class="link-references" aria-labelledby="links-heading">'
        '<h2 id="links-heading">Referenced links</h2><ol>'
        + "".join(references)
        + "</ol></section>"
    )


def render_pdf_to_html(pdf_path: Path) -> str:
    """Render one PDF as a reflowable, navigable ebook-style HTML document."""
    try:
        import pymupdf
    except ImportError as error:
        raise RuntimeError(
            "PyMuPDF is required for conversion; install dependencies with "
            "'python -m pip install -r requirements.txt'"
        ) from error

    with pymupdf.open(pdf_path) as document:
        pages = list(document)
        page_count = len(pages)
        metadata = document.metadata or {}
        raw_title = metadata.get("title") or pdf_path.stem
        toc = _toc_html(document.get_toc(), page_count)
        page_navigation = _page_navigation_html(page_count)
        article_parts = []
        for number, page in enumerate(pages, start=1):
            article_parts.append(
                f'<a id="page-{number}" class="page-anchor" '
                f'aria-label="Source page {number}"></a>'
                f'<span class="page-marker" aria-hidden="true">{number}</span>'
                + _xhtml_body(page.get_text("xhtml"))
            )
        references = _link_references_html(
            pages, page_count=page_count, pymupdf_module=pymupdf
        )

    title = html.escape(str(raw_title))
    article = "\n".join(article_parts)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{ color-scheme: light dark; font-family: Georgia, serif; line-height: 1.65; }}
    body {{ margin: 0; background: #f4f0e8; color: #28231d; }}
    .ebook {{ max-width: 72rem; margin: auto; padding: clamp(1rem, 4vw, 3rem); }}
    .ebook-header, nav, .link-references {{ font-family: system-ui, sans-serif; }}
    .ebook-header {{ border-bottom: 1px solid #a89f91; margin-bottom: 2rem; }}
    .reader-navigation {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); gap: 2rem; }}
    nav ol {{ padding-left: 1.5rem; }}
    .toc-level-2 {{ margin-left: 1rem; }}
    .toc-level-3 {{ margin-left: 2rem; }}
    a {{ color: #85551f; }}
    .ebook-content {{ max-width: 46rem; margin: 3rem auto; }}
    .ebook-content img {{ display: block; max-width: 100%; height: auto; margin: 1.5rem auto; }}
    .ebook-content p {{ margin: 0 0 1em; }}
    .page-anchor {{ scroll-margin-top: 1rem; }}
    .page-marker {{ display: block; margin: 2.5rem 0 1rem; color: #756b60; font: 0.75rem system-ui, sans-serif; }}
    .page-marker::before {{ content: "Source page "; }}
    @media (prefers-color-scheme: dark) {{
      body {{ background: #181614; color: #eee7dc; }}
      a {{ color: #e7b878; }}
    }}
  </style>
</head>
<body><main class="ebook">
  <header class="ebook-header"><h1>{title}</h1></header>
  <section class="reader-navigation">{toc}{page_navigation}</section>
  <article class="ebook-content">
{article}
  </article>
  {references}
</main></body>
</html>
"""


def _write_html_atomically(output: Path, content: str, *, overwrite: bool) -> None:
    """Commit complete HTML without exposing a partially written destination."""
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=output.parent,
            prefix=f".{output.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_file.write(content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
            temporary_path = Path(temporary_file.name)

        if overwrite:
            temporary_path.replace(output)
        else:
            os.link(temporary_path, output)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def convert_tree(
    root: Path,
    *,
    overwrite: bool = False,
    renderer: HtmlRenderer | None = None,
) -> ConversionSummary:
    """Convert PDFs below *root* and return a summary."""
    selected_renderer = renderer or render_pdf_to_html
    converted = 0
    skipped = 0
    failures: list[tuple[Path, str]] = []

    for pdf_path in discover_pdfs(root):
        output_path = pdf_path.with_suffix(".html")
        if output_path.exists() and not overwrite:
            skipped += 1
            continue

        try:
            content = selected_renderer(pdf_path)
            _write_html_atomically(output_path, content, overwrite=overwrite)
            converted += 1
        except FileExistsError:
            # Another process created the output after the existence check.
            skipped += 1
        except Exception as error:  # Keep converting independent documents.
            failures.append((pdf_path, str(error)))

    return ConversionSummary(converted=converted, skipped=skipped, failed=tuple(failures))


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Recursively convert PDFs to adjacent HTML files."
    )
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace HTML files that already exist",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface and return its process exit code."""
    arguments = build_parser().parse_args(argv)
    try:
        summary = convert_tree(arguments.root, overwrite=arguments.overwrite)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    for source, message in summary.failed:
        print(f"error: {source}: {message}", file=sys.stderr)
    print(
        f"Converted: {summary.converted}; skipped: {summary.skipped}; "
        f"failed: {len(summary.failed)}"
    )
    return 1 if summary.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

