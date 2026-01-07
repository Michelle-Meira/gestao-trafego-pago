from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Text, JSON
from sqlalchemy.sql import func
from app.database import Base
import enum

class PlatformEnum(str, enum.Enum):
    GOOGLE_ADS = "google_ads"
    META_ADS = "meta_ads"
    TIKTOK_ADS = "tiktok_ads"
    LINKEDIN_ADS = "linkedin_ads"
    TWITTER_ADS = "twitter_ads"
    PINTEREST_ADS = "pinterest_ads"

class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"
    ARCHIVED = "archived"

class BudgetType(str, enum.Enum):
    DAILY = "daily"
    LIFETIME = "lifetime"

class CampaignDB(Base):
    __tablename__ = "campaigns"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    platform = Column(Enum(PlatformEnum), nullable=False)
    budget_type = Column(Enum(BudgetType), default=BudgetType.DAILY)
    budget_amount = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    target_audience = Column(Text, nullable=True)
    keywords = Column(JSON, default=list)
    bid_strategy = Column(String(50), nullable=True)
    creative_url = Column(String(500), nullable=True)
    
    # Métricas
    total_spent = Column(Float, default=0.0)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
