"""One-off generator for the placeholder files under
app/static/sample_documents/ that the Project Details "Recent Files"
preview serves. Project documents (seeded and fallback-pool alike, see
DOCUMENT_POOL in app/routes/project_routes.py) only ever use a small,
fixed set of file names — this script builds one real, valid file per
name (not just a name+size record) so clicking one actually shows real
content instead of nothing.

Run with: python generate_sample_documents.py
"""

import os
import zipfile

OUT_DIR = os.path.join(os.path.dirname(__file__), "app", "static", "sample_documents")

PDF_TITLES = {
    "project_proposal.pdf": "Project Proposal",
    "progress_report.pdf": "Progress Report",
    "mou_agreement.pdf": "MOU Agreement",
    "q2_impact_report.pdf": "Q2 Impact Report",
}

XLSX_TITLES = {
    "budget_estimate.xlsx": "Budget Estimate",
    "budget_breakdown.xlsx": "Budget Breakdown",
}


def build_pdf(title):
    """A minimal, spec-valid single-page PDF with the title as body text."""
    body_lines = [
        "This is a sample document generated for demo/preview purposes.",
        "No real file was uploaded for this record.",
    ]

    content_lines = [f"BT /F1 24 Tf 72 700 Td ({title}) Tj ET"]
    y = 660
    for line in body_lines:
        content_lines.append(f"BT /F1 12 Tf 72 {y} Td ({line}) Tj ET")
        y -= 20
    content_stream = "\n".join(content_lines).encode("latin-1")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length %d >>\nstream\n" % len(content_stream) + content_stream + b"\nendstream",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode("latin-1") + obj + b"\nendobj\n"

    xref_offset = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode("latin-1")
    out += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        out += f"{off:010d} 00000 n \n".encode("latin-1")
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF"
    ).encode("latin-1")

    return bytes(out)


def build_xlsx(title):
    """A minimal, spec-valid single-sheet XLSX with the title in cell A1."""
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>'
        "</workbook>"
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )
    escaped_title = title.replace("&", "&amp;").replace("<", "&lt;")
    sheet = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        "<sheetData>"
        '<row r="1"><c r="A1" t="inlineStr"><is><t>%s</t></is></c></row>'
        '<row r="2"><c r="A2" t="inlineStr"><is><t>Sample document generated for demo/preview purposes.</t></is></c></row>'
        "</sheetData>"
        "</worksheet>"
    ) % escaped_title

    from io import BytesIO

    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/worksheets/sheet1.xml", sheet)
    return buf.getvalue()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for filename, title in PDF_TITLES.items():
        path = os.path.join(OUT_DIR, filename)
        with open(path, "wb") as f:
            f.write(build_pdf(title))
        print(f"wrote {path}")

    for filename, title in XLSX_TITLES.items():
        path = os.path.join(OUT_DIR, filename)
        with open(path, "wb") as f:
            f.write(build_xlsx(title))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
