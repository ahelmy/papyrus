import uuid

from jinja2 import Template
from pathlib import Path
from docxtpl import DocxTemplate
from openpyxl import Workbook
from xhtml2pdf import pisa
import pypandoc

TEMPLATES_DIR = Path("app/templates")
OUTPUT_DIR = Path("app/outputs")


def render_template(template_id: str, data: dict, format: str) -> str:
    template_path = TEMPLATES_DIR / template_id
    output_file = OUTPUT_DIR / f"{uuid.uuid4()}.{format}"

    if not template_path.exists():
        raise FileNotFoundError("Template not found")

    template_extension = template_path.suffix[1:]
    conversion_key = f'{template_extension}_{format}'
    # Render based on format
    if conversion_key in CONVERSION_MATRIX:
        return CONVERSION_MATRIX[conversion_key](template_path, data, output_file)
    else:
        raise ValueError("Unsupported format")


def html_to_html(template_path, data, output_file=None):
    with open(template_path, 'r') as file:
        template = Template(file.read())
    rendered_content = template.render(**data)
    if output_file:
        with open(output_file, 'w') as file:
            file.write(rendered_content)
    return rendered_content


def docx_to_docx(template_path, data, output_file):
    doc = DocxTemplate(template_path)
    doc.render(data)
    doc.save(output_file)
    return str(output_file)


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
    return str(output_file)


def docx_to_pdf(template_path, data, output_file: Path):
    filename = output_file.with_suffix('')
    docx_path = filename.with_suffix('.docx')
    docx_to_docx(template_path, data, docx_path)
    pypandoc.convert_file(docx_path, 'latex', outputfile=output_file)
    return str(output_file)


def html_to_pdf(template_path, data, output_file):
    html_content = html_to_html(template_path, data, None)
    with open(output_file, 'w+b') as file:
        pisa.CreatePDF(html_content, dest=file)
    return str(output_file)


CONVERSION_MATRIX = {
    'docx_pdf': docx_to_pdf,
    'docx_docx': docx_to_docx,

    'html_pdf': html_to_pdf,
    'html_html': html_to_html,
}
