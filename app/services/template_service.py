from __future__ import annotations

import subprocess
import uuid

from jinja2 import Template
from pathlib import Path
from docxtpl import DocxTemplate
from openpyxl import Workbook

TEMPLATES_DIR = Path("app/templates")
OUTPUT_DIR = Path("app/outputs")


def render_template(template_id: str, data: dict, format: str) -> Path:
    template_path = TEMPLATES_DIR / template_id
    output_file = OUTPUT_DIR / f"{uuid.uuid4()}.{format}"

    if not template_path.exists():
        raise FileNotFoundError("Template not found")

    template_extension = template_path.suffix[1:]
    conversion_key = f'{template_extension}_{format}'
    # Render based on format
    if conversion_key in CONVERSION_MATRIX:
        CONVERSION_MATRIX[conversion_key](template_path, data, output_file)
        return output_file
    else:
        raise ValueError("Unsupported format")


def html_to_html(template_path, data, output_file):
    with open(template_path, 'r') as file:
        template = Template(file.read())
    rendered_content = template.render(**data)
    if output_file:
        with open(output_file, 'w') as file:
            file.write(rendered_content)


def docx_to_docx(template_path, data, output_file):
    doc = DocxTemplate(template_path)
    doc.render(data)
    doc.save(output_file)


def render_xlsx(template_path, data, output_file):
    wb = Workbook(template_path)
    ws = wb.active
    # Process the XLSX using openpyxl
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str):
                for key, value in data.items():
                    if f'{{{{{key}}}}}' in cell.value:
                        cell.value = cell.value.replace(f'{{{{{key}}}}}', str(value))
    wb.save(output_file)


def docx_to_pdf(template_path, data, output_file: Path):
    filename = output_file.with_suffix('')
    docx_path = filename.with_suffix('.docx')
    docx_to_docx(template_path, data, docx_path)
    infilters = [
        '--infilter="Microsoft Word 2007/2010/2013 XML"',
        '--infilter="Microsoft Word 2007-2013 XML"',
        '--infilter="Microsoft Word 2007-2013 XML Template"',
        '--infilter="Microsoft Word 95 Template"',
        '--infilter="MS Word 95 Vorlage"',
        '--infilter="Microsoft Word 97/2000/XP Template"',
        '--infilter="MS Word 97 Vorlage"',
        '--infilter="Microsoft Word 2003 XML"',
        '--infilter="MS Word 2003 XML"',
        '--infilter="Microsoft Word 2007 XML Template"',
        '--infilter="MS Word 2007 XML Template"',
        '--infilter="Microsoft Word 6.0"',
        '--infilter="MS WinWord 6.0"',
        '--infilter="Microsoft Word 95"',
        '--infilter="MS Word 95"',
        '--infilter="Microsoft Word 97/2000/XP"',
        '--infilter="MS Word 97"',
        '--infilter="Microsoft Word 2007 XML"',
        '--infilter="MS Word 2007 XML"',
        '--infilter="Microsoft WinWord 5"',
        '--infilter="MS WinWord 5"'
    ]

    err = convert_to_pdf_by_libreoffice(infilters, docx_path)
    if err:
        raise ValueError(err)


def html_to_pdf(template_path, data, output_file):
    html_path = output_file.with_suffix('.html')
    html_to_html(template_path, data, html_path)

    err = convert_to_pdf_by_libreoffice(['--infilter="HTML Document"', '--infilter="MediaWiki"'], html_path)
    if err:
        raise ValueError(err)


def convert_to_pdf_by_libreoffice(infilters, source_path) -> str | None:
    cmd = ['soffice', '--headless']
    cmd.extend(infilters)
    cmd.extend(['--convert-to', 'pdf:writer_pdf_Export', '--outdir', OUTPUT_DIR, source_path])
    result = subprocess.run(cmd)
    if result.returncode != 0:
        return "Failed to convert to PDF"
    return None


CONVERSION_MATRIX = {
    'docx_pdf': docx_to_pdf,
    'docx_docx': docx_to_docx,

    'html_pdf': html_to_pdf,
    'html_html': html_to_html,
}
