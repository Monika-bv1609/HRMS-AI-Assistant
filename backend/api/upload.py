from typing import List

from fastapi import APIRouter, Form, UploadFile, File

from services.upload_service import upload_multiple_pdfs_to_rag

router = APIRouter()


@router.post("/upload-pdf")
def upload_pdf(
    files: List[UploadFile] = File(...),
    policy_type: str = Form(...)
):
    print("UPLOAD ROUTE HIT")
    print(f"ROUTE POLICY TYPE = {policy_type}")

    return upload_multiple_pdfs_to_rag(
        files,
        policy_type
    )