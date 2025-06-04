from fastapi import APIRouter, Form, Request
from fastapi.responses import PlainTextResponse
from app.services.cv_generator import parse_message, generate_cv_content
from app.utils.cloudinary_upload import upload_file_to_cloudinary
from app.utils.pdf import  create_pdf_file
from app.utils.generate_doc import create_docx_file

router = APIRouter()

# To receive form-encoded data from Twilio WhatsApp Webhook
@router.post("/twilio/webhook")
async def twilio_webhook(
        body: str = Form(..., alias="Body"), # The user's message
        from_number: str = Form(..., alias="From") # The sender's WhatsApp Number
):
    try:
        print(f"Received CV request from: {from_number}")

        # To parse the WhatsApp text and generate content
        parsed_data = parse_message(body)
        cv = await generate_cv_content(parsed_data)
        name, email, content = cv["name"], cv["email"], cv["content"]

        # To generate the files and upload to Cloudinary
        pdf_path = create_pdf_file(name, email, content)
        docx_path = create_docx_file(name, email, content)

        pdf_url = upload_file_to_cloudinary(pdf_path)
        docx_url = upload_file_to_cloudinary(docx_path)

        # To set up the WhatsApp response to be sent to the user
        response_text = (
            f"Hi {name}, your CV has been generated!\n\n"
            f"📄 PDF: {pdf_url}\n"
            f"📝 Word: {docx_url}\n\n"
            f"Thank you for using MyChatCV!"
        )

        return PlainTextResponse(content=response_text)

    except Exception as e:
        return PlainTextResponse(content=f"Sorry, something went wrong: {str(e)}")