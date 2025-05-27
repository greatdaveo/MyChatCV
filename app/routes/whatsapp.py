from fastapi import APIRouter, HTTPException
from app.models.whatsapp import WhatsAppCVRequest
from app.services.cv_generator import parse_message, generate_cv_content

router = APIRouter()

@router.post("/")
async def generate_cv_from_whatsapp(request: WhatsAppCVRequest):
    try:
        # To parse the message
        parsed_data = parse_message(request.message)
        cv_content = await generate_cv_content(parsed_data)
        return {
            "cv": cv_content,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))