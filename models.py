from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="field_officer")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sites = relationship("Site", back_populates="creator")

class Site(Base):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    roof_area_sqm = Column(Float, nullable=False)
    roof_material = Column(String, nullable=True)
    soil_type = Column(String, nullable=True)
    avg_rainfall_mm = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    creator = relationship("User", back_populates="sites")
    assessments = relationship("Assessment", back_populates="site")

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    harvest_potential_lpy = Column(Float, nullable=False)  # litres per year
    recharge_feasible = Column(Boolean, default=False)
    cost_estimate_inr = Column(Float, default=0.0)
    report_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    site = relationship("Site", back_populates="assessments")
