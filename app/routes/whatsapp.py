from fastapi import APIRouter, HTTPException
from app.models.whatsapp import WhatsAppCVRequest
from app.services.cv_generator import parse_message

router = APIRouter()

@router.post("/")
async def generate_cv_from_whatsapp(request: WhatsAppCVRequest):
    try:
        # To parse the message
        parsed_data = parse_message(request.message)
        return {
            "parsed": parsed_data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))