from pydantic import BaseModel
from typing import Optional
import datetime

class Task(BaseModel):
    TaskID: int 
    UserID: int
    UserName: str
    Titulo: str
    Descripcion: str
    Finalizado: Optional[int]
    CreadoEn: Optional[datetime.datetime]
    FinalizadoEn: Optional[datetime.datetime]