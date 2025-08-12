from pydantic import BaseModel

class WhatsAppCVRequest(BaseModel):
    message: str