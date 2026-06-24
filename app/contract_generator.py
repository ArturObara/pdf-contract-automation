import os
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

template_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def generate_upsell_pdf(client_data: dict) -> bytes:
    template = template_env.get_template("upsell_contract_template.html")
    rendered_html = template.render(**client_data)
    
    pdf_buffer = BytesIO()
    HTML(string=rendered_html).write_pdf(target=pdf_buffer, pdf_forms=True)
    
    return pdf_buffer.getvalue()