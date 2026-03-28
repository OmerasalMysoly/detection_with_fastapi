from pydantic import BaseModel, Field

class MAIL_VALIDATION(BaseModel):
    email: str = Field(..., example="0.0.0")