from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.database import db
from app.models.document import Document
from app.utils.auth import get_current_user  

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
    dependencies=[Depends(get_current_user)]  
)

@router.post("/doc")
async def upload_doc(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    user = await db.users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    existing_doc = await db.documents.find_one({
        "user_id": user_id,
        "filename": file.filename
    })

    if existing_doc:
        return {
            "message": "File already exists for this user",
            "user_id": user_id,
            "filename": file.filename,
            "status": existing_doc["status"]
        }

    pdf_content = await file.read()

    doc = Document(
        user_id=user_id,
        filename=file.filename,
        status="Submitted",
        file_data=pdf_content
    )
    await db.documents.insert_one(doc.model_dump())

    return {
        "message": "PDF uploaded and saved in MongoDB",
        "user_id": user_id,
        "filename": file.filename,
        "status": doc.status
    }

# ⬇️ Retrieve PDF
@router.get("/doc/{user_id}")
async def get_user_pdf(user_id: str):
    doc = await db.documents.find_one({"user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="No PDF found for this user")

    return StreamingResponse(
        BytesIO(doc["file_data"]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={doc['filename']}"}
    )
