from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.report import ReportGenerateRequest
from app.services.report_service import generate_report_data, build_pdf_report
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/generate")
def generate_report(
    req: ReportGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        report_data = generate_report_data(db, req)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    if req.export_format.lower() == "pdf":
        pdf_buffer = build_pdf_report(report_data)
        filename = f"{report_data.get('report_id', 'report')}.pdf"
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    return report_data

@router.get("/download-pdf/{project_id}")
def download_project_report_pdf(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    req = ReportGenerateRequest(report_type="PROJECT_RISK", project_id=project_id, export_format="pdf")
    try:
        report_data = generate_report_data(db, req)
        pdf_buffer = build_pdf_report(report_data)
        filename = f"Project_Risk_Report_PRJ_{project_id}.pdf"
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
