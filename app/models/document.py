from pydantic import BaseModel
from typing import Optional

class Document(BaseModel):
    user_id: str
    filename: str
    status: Optional[str] = "Pending"  
    file_data: bytes 