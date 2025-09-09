from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SiteCreate(BaseModel):
    latitude: float
    longitude: float
    roof_area_sqm: float = Field(gt=0)
    roof_material: Optional[str] = None
    soil_type: Optional[str] = None
    avg_rainfall_mm: float = Field(gt=0)

class SiteOut(SiteCreate):
    id: int
    class Config:
        from_attributes = True

class AssessmentOut(BaseModel):
    id: int
    site_id: int
    harvest_potential_lpy: float
    recharge_feasible: bool
    cost_estimate_inr: float
    report_url: Optional[str] = None
    class Config:
        from_attributes = True
