from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.models import Assessment, Site, User
from ..core.config import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path
import os

router = APIRouter()

REPORTS_DIR = Path(__file__).resolve().parent.parent / 'reports'
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def create_pdf_report(assessment: Assessment, site: Site, filepath: Path):
    c = canvas.Canvas(str(filepath), pagesize=A4)
    width, height = A4
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-60, 'Rooftop Rainwater Harvesting Assessment Report')
    c.setFont('Helvetica', 11)
    c.drawString(40, height-100, f'Site ID: {site.id}')
    c.drawString(40, height-120, f'Latitude, Longitude: {site.latitude}, {site.longitude}')
    c.drawString(40, height-140, f'Roof Area (sqm): {site.roof_area_sqm}')
    c.drawString(40, height-160, f'Roof Material: {site.roof_material or "N/A"}')
    c.drawString(40, height-180, f'Soil Type: {site.soil_type or "N/A"}')
    c.drawString(40, height-200, f'Avg Rainfall (mm/yr): {site.avg_rainfall_mm}')
    c.drawString(40, height-230, f'Harvest Potential (L/yr): {assessment.harvest_potential_lpy:.2f}')
    c.drawString(40, height-250, f'Recharge Feasible: {assessment.recharge_feasible}')
    c.drawString(40, height-270, f'Estimated Cost (INR): {assessment.cost_estimate_inr:.2f}')
    c.showPage()
    c.save()

@router.post('/assessments/{assessment_id}/report')
def generate_report(assessment_id: int, db: Session = Depends(get_db)):
    assessment = db.query(Assessment).get(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail='Assessment not found')
    site = db.query(Site).get(assessment.site_id)
    if not site:
        raise HTTPException(status_code=404, detail='Site not found')
    filename = f'assessment_{assessment_id}.pdf'
    filepath = REPORTS_DIR / filename
    create_pdf_report(assessment, site, filepath)
    # save path to assessment.report_url (relative)
    assessment.report_url = str(filepath.name)
    db.add(assessment)
    db.commit()
    return {'report': f'/reports/{filename}', 'filename': filename}
