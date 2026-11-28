from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import ClassVar, Self
from unittest.mock import patch

from pdf_to_html import convert_tree, discover_pdfs, render_pdf_to_html


class FakePage:
    def __init__(
        self, number: int, content: str, links: list[dict[str, object]]
    ) -> None:
        self.number = number
        self.content = content
        self.links = links
        self.requested_formats: list[str] = []

    def get_text(self, output_format: str) -> str:
        self.requested_formats.append(output_format)
        if output_format == "html":
            return '<div style="position:relative"><p style="position:absolute">fixed</p></div>'
        return f'<div id="page{self.number}"><p>{self.content}</p></div>'

    def get_links(self) -> list[dict[str, object]]:
        return self.links


class FakeDocument:
    metadata: ClassVar[dict[str, str]] = {"title": "Native & Ebook"}

    def __init__(self, pages: list[FakePage]) -> None:
        self.pages = pages

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def __iter__(self):  # type: ignore[no-untyped-def]
        return iter(self.pages)

    def get_toc(self) -> list[list[object]]:
        return [[1, "Introduction", 1], [2, "Details", 2]]


class DiscoverPdfsTests(unittest.TestCase):
    def test_pdfs_in_nested_directories_are_discovered_case_insensitively(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first.pdf"
            second = root / "nested" / "second.PDF"
            second.parent.mkdir()
            first.touch()
            second.touch()
            (root / "ignore.txt").touch()

            discovered = discover_pdfs(root)

            self.assertEqual(discovered, [first, second])

    def test_missing_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"

            with self.assertRaisesRegex(ValueError, "does not exist"):
                discover_pdfs(missing)

    def test_file_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            file_root = Path(directory) / "not-a-directory"
            file_root.touch()

            with self.assertRaisesRegex(ValueError, "not a directory"):
                discover_pdfs(file_root)


class ConvertTreeTests(unittest.TestCase):
    def test_pdf_is_converted_beside_source_without_modifying_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "nested" / "guide.pdf"
            source.parent.mkdir()
            source.write_bytes(b"original-pdf")

            summary = convert_tree(root, renderer=lambda path: f"<p>{path.name}</p>")

            self.assertEqual(source.read_bytes(), b"original-pdf")
            self.assertEqual(
                source.with_suffix(".html").read_text(encoding="utf-8"),
                "<p>guide.pdf</p>",
            )
            self.assertEqual(summary.converted, 1)
            self.assertEqual(summary.skipped, 0)
            self.assertEqual(summary.failed, ())

    def test_existing_html_is_skipped_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "guide.pdf"
            output = root / "guide.html"
            source.touch()
            output.write_text("keep me", encoding="utf-8")

            summary = convert_tree(root, renderer=lambda _: "replacement")

            self.assertEqual(output.read_text(encoding="utf-8"), "keep me")
            self.assertEqual(summary.converted, 0)
            self.assertEqual(summary.skipped, 1)

    def test_existing_html_is_replaced_only_when_overwrite_is_true(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "guide.pdf"
            output = root / "guide.html"
            source.touch()
            output.write_text("old", encoding="utf-8")

            summary = convert_tree(root, overwrite=True, renderer=lambda _: "new")

            self.assertEqual(output.read_text(encoding="utf-8"), "new")
            self.assertEqual(summary.converted, 1)
            self.assertEqual(summary.skipped, 0)

    def test_one_conversion_failure_does_not_stop_other_pdfs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bad = root / "bad.pdf"
            good = root / "good.pdf"
            bad.touch()
            good.touch()

            def renderer(path: Path) -> str:
                if path == bad:
                    raise RuntimeError("damaged PDF")
                return "converted"

            summary = convert_tree(root, renderer=renderer)

            self.assertFalse(bad.with_suffix(".html").exists())
            self.assertEqual(
                good.with_suffix(".html").read_text(encoding="utf-8"), "converted"
            )
            self.assertEqual(summary.converted, 1)
            self.assertEqual(summary.failed, ((bad, "damaged PDF"),))


class EbookRenderingTests(unittest.TestCase):
    def test_pdf_becomes_a_reflowable_article_with_toc_and_page_navigation(
        self,
    ) -> None:
        pages = [
            FakePage(0, "Introduction text", []),
            FakePage(1, "Details text", []),
        ]
        document = FakeDocument(pages)
        fake_pymupdf = SimpleNamespace(open=lambda _: document, LINK_URI=2, LINK_GOTO=1)

        with patch.dict(sys.modules, {"pymupdf": fake_pymupdf}):
            output = render_pdf_to_html(Path("sample.pdf"))

        self.assertEqual(pages[0].requested_formats, ["xhtml"])
        self.assertNotIn("position:absolute", output)
        self.assertIn('<article class="ebook-content">', output)
        self.assertIn('<a href="#page-1">Introduction</a>', output)
        self.assertIn('<a href="#page-2">Page 2</a>', output)
        self.assertIn('id="page-1"', output)
        self.assertIn("Introduction text", output)
        self.assertIn("Details text", output)

    def test_safe_pdf_links_are_preserved_and_unsafe_uris_are_omitted(self) -> None:
        page = FakePage(
            0,
            "References",
            [
                {"kind": 2, "uri": "https://example.com/?a=1&b=2"},
                {"kind": 2, "uri": "mailto:reader@example.com"},
                {"kind": 2, "uri": "javascript:alert(1)"},
                {"kind": 1, "page": 1},
            ],
        )
        document = FakeDocument([page, FakePage(1, "Target", [])])
        fake_pymupdf = SimpleNamespace(open=lambda _: document, LINK_URI=2, LINK_GOTO=1)

        with patch.dict(sys.modules, {"pymupdf": fake_pymupdf}):
            output = render_pdf_to_html(Path("sample.pdf"))

        self.assertIn('href="https://example.com/?a=1&amp;b=2"', output)
        self.assertIn('href="mailto:reader@example.com"', output)
        self.assertIn('href="#page-2"', output)
        self.assertNotIn("javascript:", output)


if __name__ == "__main__":
    unittest.main()
