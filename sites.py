from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.models import Site
from ..schemas.schemas import SiteCreate, SiteOut
from .auth import get_current_user, User

router = APIRouter()

@router.post("/", response_model=SiteOut)
def create_site(payload: SiteCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    site = Site(
        user_id=user.id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        roof_area_sqm=payload.roof_area_sqm,
        roof_material=payload.roof_material,
        soil_type=payload.soil_type,
        avg_rainfall_mm=payload.avg_rainfall_mm,
    )
    db.add(site)
    db.commit()
    db.refresh(site)
    return site

@router.get("/{site_id}", response_model=SiteOut)
def get_site(site_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    site = db.query(Site).get(site_id)
    if not site or site.user_id != user.id:
        raise HTTPException(status_code=404, detail="Site not found")
    return site
