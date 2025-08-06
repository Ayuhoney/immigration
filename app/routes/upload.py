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
    email: str = Form(...),
    status: str = Form(...),
    visa_type: str = Form(...),
    file: UploadFile = File(...)
):
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    existing_doc = await db.documents.find_one({
        "email": email,
        "filename": file.filename
    })

    if existing_doc:
        return {
            "message": "File already exists for this user",
            "email": email,
            "filename": file.filename,
            "status": existing_doc["status"]
        }

    pdf_content = await file.read()

    doc = Document(
        email=email,
        filename=file.filename,
        status=status,          # ✅ saving status
        visa_type=visa_type,    # ✅ saving visa_type
        file_data=pdf_content
    )

    await db.documents.insert_one(doc.model_dump()) 

    return {
        "message": "PDF uploaded and saved in MongoDB",
        "email": email,
        "filename": file.filename,
        "status": doc.status,
        "visa_type": doc.visa_type
    }



@router.get("/doc/{email}")
async def get_user_pdf(email: str):
    doc = await db.documents.find_one({"email": email})
    if not doc:
        raise HTTPException(status_code=404, detail="No PDF found for this user")

    pdf_stream = BytesIO(doc["file_data"])

    headers = {
        "Content-Disposition": f'inline; filename="{doc["filename"]}"',
        "Content-Type": "application/pdf",
        "Content-Length": str(len(doc["file_data"])),
        "Cache-Control": "no-cache",
        "X-Filename": doc["filename"],         # ✅ custom header
        "X-Visa-Type": doc["visa_type"],       # ✅ custom header
        "X-Status": doc["status"]              # ✅ custom header
    }

    return StreamingResponse(pdf_stream, media_type="application/pdf", headers=headers)
