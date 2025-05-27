from fastapi import APIRouter, HTTPException
from app.models.whatsapp import WhatsAppCVRequest
from app.services.cv_generator import parse_message, generate_cv_content
from app.utils.pdf import create_pdf_file
from app.utils.generate_doc import create_docx_file
from app.utils.cloudinary_upload import upload_file_to_cloudinary

router = APIRouter()


@router.post("/")
async def generate_cv_from_whatsapp(request: WhatsAppCVRequest):
    try:
        # To parse the message
        parsed_data = parse_message(request.message)
        cv_content = await generate_cv_content(parsed_data)

        name = cv_content["name"]
        email = cv_content["email"]
        content = cv_content["content"]

        # Tp generate the PDF anf Docx files
        pdf_path = create_pdf_file(name, email, content)
        docx_path = create_docx_file(name, email, content)

        # To upload to cloudinary
        pdf_url = upload_file_to_cloudinary(pdf_path)
        docx_url = upload_file_to_cloudinary(docx_path)


        return {
            "status": "success",
            "data": {
             "name": name,
                "email": email,
                "pdf_url": pdf_url,
                "docx_url": docx_url
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))