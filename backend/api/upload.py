from typing import List

from fastapi import APIRouter, UploadFile, File

from services.upload_service import upload_multiple_pdfs_to_rag

router = APIRouter()


@router.post("/upload-pdf")
def upload_pdf(files: List[UploadFile] = File(...)):

    return upload_multiple_pdfs_to_rag(files)