from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()


@router.get("/report/json")
def download_json():

    path = "reports/output/report.json"

    if os.path.exists(path):
        return FileResponse(
            path,
            filename="BugHunter_Report.json",
            media_type="application/json"
        )

    return {
        "error": "Report not found."
    }


@router.get("/report/html")
def download_html():

    path = "reports/output/report.html"

    if os.path.exists(path):
        return FileResponse(
            path,
            filename="BugHunter_Report.html",
            media_type="text/html"
        )

    return {
        "error": "Report not found."
    }


@router.get("/report/pdf")
def download_pdf():

    path = "reports/output/report.pdf"

    if os.path.exists(path):
        return FileResponse(
            path,
            filename="BugHunter_Report.pdf",
            media_type="application/pdf"
        )

    return {
        "error": "Report not found."
    }