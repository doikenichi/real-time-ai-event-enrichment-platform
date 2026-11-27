# PDF to HTML converter

`pdf_to_html.py` recursively finds PDF files below a directory and creates a
reflowable, ebook-style HTML file beside each PDF. The source PDF is never
changed or removed.

## Setup

Python 3.11 or newer is required.

```powershell
python -m pip install -r requirements.txt
```

PyMuPDF is licensed under AGPL-3.0 (with a commercial licensing option). Check
that this license is suitable before incorporating the converter into a
proprietary application.

## Usage

Scan the current directory and all of its subdirectories:

```powershell
python pdf_to_html.py
```

Scan a particular directory:

```powershell
python pdf_to_html.py "C:\path\to\pdfs"
```

Existing HTML files are skipped by default. Replace them only when explicitly
requested:

```powershell
python pdf_to_html.py "C:\path\to\pdfs" --overwrite
```

The command prints converted, skipped, and failed counts. It returns exit code
`0` when every conversion succeeds, `1` when one or more PDFs fail, and `2` for
an invalid root directory. A failure in one PDF does not prevent the remaining
PDFs from being processed.

Each output document contains:

- one continuous semantic article instead of fixed-position PDF page replicas
- a clickable table of contents when the PDF has an outline
- navigation links and anchors for every source page
- embedded images that resize with the reader window
- safe web, email, and internal-page references from the PDF
- responsive light and dark ebook styling

PDFs do not inherently contain ebook-quality structure, so the reading order is
only as good as the source document's text layer. Image-only scanned PDFs
require a separate OCR step to produce searchable text.

## Tests

The tests use only Python's standard library:

```powershell
python -m unittest discover -s tests -v
```
