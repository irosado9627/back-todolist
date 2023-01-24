from pydantic import BaseModel

class genericResponse(BaseModel):
    msg: str
    data: dict