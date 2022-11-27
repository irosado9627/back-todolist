from pydantic import BaseModel
from typing import Optional
import datetime

class User(BaseModel):
    UserID: int
    UserName: str
    Password: Optional[str]
    Estatus: Optional[str]
    FechaAlta: Optional[datetime.date]
    AudFecha: Optional[datetime.datetime]
    FechaBaja: Optional[datetime.date]
    FechaBloq: Optional[datetime.date]

class UserCreated(BaseModel):
    msg: str
    UserName: str