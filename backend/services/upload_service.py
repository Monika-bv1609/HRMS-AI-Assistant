import requests

from utils.config import PDF_AGENT_URL


def upload_pdf_to_rag(file):


# multipart/form-data upload
    files = {
        "file": (file.filename, file.file, file.content_type)
    }

    response = requests.post(
        f"{PDF_AGENT_URL}/read-pdf",
        files=files
    )

    return response.json()