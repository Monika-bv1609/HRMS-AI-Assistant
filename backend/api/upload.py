from fastapi import APIRouter, UploadFile, File

from services.upload_service import upload_pdf_to_rag

router = APIRouter()


@router.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):

    return upload_pdf_to_rag(file)