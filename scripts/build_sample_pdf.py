"""Build a tiny text PDF with extractable content (no reportlab dependency)."""

from __future__ import annotations

from pathlib import Path


def make_text_pdf(lines: list[str]) -> bytes:
    """Return a minimal PDF-1.4 document whose text pypdf can extract."""
    content_parts = ["BT", "/F1 11 Tf", "50 750 Td"]
    for i, line in enumerate(lines):
        safe = (
            line.replace("\\", "\\\\")
            .replace("(", "\\(")
            .replace(")", "\\)")
        )
        if i == 0:
            content_parts.append(f"({safe}) Tj")
        else:
            content_parts.append("0 -16 Td")
            content_parts.append(f"({safe}) Tj")
    content_parts.append("ET")
    stream = "\n".join(content_parts).encode("latin-1", errors="replace")

    objects: list[bytes] = []
    objects.append(b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n")
    objects.append(b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n")
    objects.append(
        b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources<< /Font<< /F1 5 0 R >> >> >>endobj\n"
    )
    objects.append(
        f"4 0 obj<< /Length {len(stream)} >>stream\n".encode("ascii")
        + stream
        + b"\nendstream\nendobj\n"
    )
    objects.append(
        b"5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n"
    )

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(out))
        out.extend(obj)

    xref_pos = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    out.extend(
        f"trailer<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )
    return bytes(out)


def write_sample_manual(path: Path) -> Path:
    lines = [
        "DAEP Building Sample AHU O&M Excerpt synthetic PDF fixture",
        "Equipment: AHU-3 Floor 3 Trane CSAA-40",
        "Design supply airflow: 14000 CFM",
        "Fan motor: 30 HP",
        "Design fan power baseline: 16.5 kW at 75 F OA",
        "Design SAT: 55 F",
        "Cooling coil: 52 tons",
        "Filter MERV 14 replace when DP greater than 1.5 in w.g.",
        "Minimum OA: 2800 CFM",
        "Exception: power more than 20 percent above baseline for over 30 minutes",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(make_text_pdf(lines))
    return path


if __name__ == "__main__":
    repo = Path(__file__).resolve().parents[1]
    out = write_sample_manual(repo / "raw" / "manuals" / "sample-ahu-om-excerpt.pdf")
    print(f"Wrote {out}")
