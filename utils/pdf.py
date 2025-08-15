import pdfkit
import tempfile
import os
from app.utils.templates import build_cv_html

# To generate a PDF file from the HTML content and return the file path
def create_pdf_file(name: str, email: str, content:str)-> str:
    html = build_cv_html(name, email, content)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")as tmp_file:
        pdfkit.from_string(html, tmp_file.name)
        return tmp_file.name
