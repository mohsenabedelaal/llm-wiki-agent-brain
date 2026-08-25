# pypdf — Extract Text and PdfReader

Canonical: https://pypdf.readthedocs.io/en/stable/user/extract-text.html

`pypdf` is a pure-python PDF library capable of extracting text and metadata, splitting, merging, cropping, and transforming PDF files.

## Text Extraction

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
page = reader.pages[0]
text = page.extract_text()
```

### Extraction Modes and Options

```python
# Extract in fixed-width layout adhering to rendered layout
text_layout = page.extract_text(extraction_mode="layout")

# Preserve horizontal positioning without excess vertical whitespace
text_clean = page.extract_text(
    extraction_mode="layout",
    layout_mode_space_vertically=False,
)

# Extract oriented text (e.g. upward or turned)
text_oriented = page.extract_text((0, 90))
```

### Using Visitor Functions

Visitor functions allow custom filtering of text fragments (e.g., ignoring headers and footers):

```python
parts = []

def visitor_body(text, cm, tm, font_dict, font_size):
    y = tm[5]
    if 50 < y < 720 or y == 0:
        parts.append(text)

page.extract_text(visitor_text=visitor_body)
body_text = "".join(parts)
```

## Practical Considerations

- **Scanned Documents**: `extract_text()` returns empty or minimal text on image-only/scanned PDFs. OCR software is needed for image-based PDFs.
- **Memory Usage**: Extracting text parses full content streams; check stream sizes if processing large or uncompressed PDFs.
- **Safety & Robustness**: Bound iteration over `reader.pages` (`len(reader.pages)`) and only read from allowlisted repository directories.
