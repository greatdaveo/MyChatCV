import pdfkit
import tempfile
import os
from utils.templates import build_cv_html, build_simple_cv_html


# To generate a PDF file from HTML content and return the file path
def create_pdf_file(
    name: str,
    email: str,
    content: str,
    phone: str = "",
    location: str = "",
    linkedin: str = "",
) -> str:
    try:
        html = build_cv_html(name, email, content, phone, location, linkedin)
        print(f"HTML generated, length: {len(html)}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None
            }
            pdfkit.from_string(html, tmp_file.name, options=options)
            output_path = tmp_file.name

        if not (os.path.exists(output_path) and os.path.getsize(output_path) > 0):
            raise RuntimeError("wkhtmltopdf produced an empty file")

        return output_path

    except Exception as e:
        # Fallback to a simpler template if enhanced template or wkhtmltopdf fails
        print(f"PDF generation error (primary): {str(e)}")

        try:
            simple_html = build_simple_cv_html(name, email, content)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                options = {
                    'page-size': 'A4',
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': "UTF-8",
                    'no-outline': None,
                    'enable-local-file-access': None
                }
                pdfkit.from_string(simple_html, tmp_file.name, options=options)
                output_path = tmp_file.name

            if not (os.path.exists(output_path) and os.path.getsize(output_path) > 0):
                raise RuntimeError(
                    "wkhtmltopdf produced an empty file (fallback)")

            return output_path

        except Exception as e2:
            raise Exception(f"PDF generation failed: {str(e2)}")
