from pydantic import BaseModel
from typing import Optional

class Document(BaseModel):
    email: str
    filename: str
    status: Optional[str] = "Pending"  
    file_data: bytes 