from pydantic import BaseModel, Field, validator, ConfigDict
from datetime import datetime, date
from typing import Optional, List
from enum import Enum
from decimal import Decimal


class Platform(str, Enum):
    GOOGLE_ADS = "google_ads"
    META_ADS = "meta_ads"
    TIKTOK_ADS = "tiktok_ads"
    LINKEDIN_ADS = "linkedin_ads"
    TWITTER_ADS = "twitter_ads"
    PINTEREST_ADS = "pinterest_ads"


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"
    ARCHIVED = "archived"


class BudgetType(str, Enum):
    DAILY = "daily"
    LIFETIME = "lifetime"


class CampaignBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nome da campanha")
    platform: Platform = Field(..., description="Plataforma de anúncio")
    budget_type: BudgetType = Field(default=BudgetType.DAILY, description="Tipo de orçamento")
    budget_amount: float = Field(..., gt=0, description="Valor do orçamento")
    start_date: datetime = Field(..., description="Data de início")
    end_date: Optional[datetime] = Field(None, description="Data de término (opcional)")
    status: CampaignStatus = Field(default=CampaignStatus.DRAFT, description="Status da campanha")
    target_audience: Optional[str] = Field(None, description="Público-alvo")
    keywords: List[str] = Field(default_factory=list, description="Palavras-chave")
    bid_strategy: Optional[str] = Field(None, description="Estratégia de lance")
    creative_url: Optional[str] = Field(None, description="URL do criativo")
    
    @validator('end_date')
    def validate_dates(cls, end_date, values):
        if 'start_date' in values and end_date:
            if end_date < values['start_date']:
                raise ValueError('end_date deve ser após start_date')
        return end_date
    
    @validator('budget_amount')
    def validate_budget(cls, budget_amount, values):
        if budget_amount <= 0:
            raise ValueError('Orçamento deve ser maior que zero')
        return round(budget_amount, 2)


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    budget_amount: Optional[float] = Field(None, gt=0)
    status: Optional[CampaignStatus] = None
    end_date: Optional[date] = None
    target_audience: Optional[str] = None


class Campaign(CampaignBase):
    id: int
    created_at: datetime
    updated_at: datetime
    total_spent: float = Field(default=0.0, description="Total gasto até o momento")
    impressions: int = Field(default=0, description="Número de impressões")
    clicks: int = Field(default=0, description="Número de cliques")
    conversions: int = Field(default=0, description="Número de conversões")
    
    model_config = ConfigDict(from_attributes=True)
