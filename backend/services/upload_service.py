from urllib import response

import requests

from utils.config import PDF_AGENT_URL
from langsmith import traceable

@traceable(name="upload_multiple_pdfs_to_rag")
def upload_multiple_pdfs_to_rag(files,policy_type):

    uploaded_files = []

    for file in files:

        file_data = [
            (
                "files",
                (
                    file.filename,
                    file.file,
                    file.content_type
                )
            )
        ]
        print(
            f"[UPLOAD] {file.filename} -> policy_type={policy_type}"
        )
        response = requests.post(
            f"{PDF_AGENT_URL}/read-pdf",
            files=file_data,
            data={
                "policy_type": policy_type
            }

        )
        print(f"{PDF_AGENT_URL}/read-pdf")
        print("STATUS:", response.status_code)
        print("BODY:", response.text)


        uploaded_files.append({
            "filename": file.filename,
            "response": response.json()
        })

    return {
        "message": "All PDFs processed successfully",
        "uploaded_files": uploaded_files
    }