import requests

from utils.config import PDF_AGENT_URL


def upload_multiple_pdfs_to_rag(files):

    uploaded_files = []

    for file in files:

        file_data = {
            "file": (
                file.filename,
                file.file,
                file.content_type
            )
        }

        response = requests.post(
            f"{PDF_AGENT_URL}/read-pdf",
            files=file_data
        )

        uploaded_files.append({
            "filename": file.filename,
            "response": response.json()
        })

    return {
        "message": "All PDFs processed successfully",
        "uploaded_files": uploaded_files
    }