from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.models import Site, Assessment
from ..schemas.schemas import AssessmentOut
from .auth import get_current_user, User

router = APIRouter()

def runoff_coefficient(material: str | None):
    # Simple defaults (can be refined with field data)
    mapping = {
        "concrete": 0.85,
        "tile": 0.75,
        "metal": 0.90,
        "asphalt": 0.85,
        "green_roof": 0.5,
    }
    return mapping.get((material or "").lower(), 0.8)

def compute_harvest_lpy(area_sqm: float, rainfall_mm: float, coeff: float) -> float:
    # rainfall_mm is mm/year; 1 mm over 1 sqm = 1 litre
    return area_sqm * rainfall_mm * coeff

def recharge_feasible(soil: str | None, area_sqm: float) -> bool:
    # Very simple rule-based feasibility (MVP)
    if not soil:
        return True
    s = soil.lower()
    if "clay" in s:
        return area_sqm >= 80  # need larger area for percolation
    return True

@router.post("/{site_id}/compute", response_model=AssessmentOut)
def compute(site_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    site = db.query(Site).get(site_id)
    if not site or site.user_id != user.id:
        raise HTTPException(status_code=404, detail="Site not found")
    coeff = runoff_coefficient(site.roof_material)
    harvest = compute_harvest_lpy(site.roof_area_sqm, site.avg_rainfall_mm, coeff)
    feasible = recharge_feasible(site.soil_type, site.roof_area_sqm)
    assessment = Assessment(
        site_id=site.id,
        harvest_potential_lpy=harvest,
        recharge_feasible=feasible,
        cost_estimate_inr= round(harvest * 0.02, 2)  # dummy linear estimate
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment
