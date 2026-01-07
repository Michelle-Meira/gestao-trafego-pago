from fastapi import APIRouter, HTTPException, Query, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
import statistics

from app.database import get_db
from app.schemas.campaign_db import CampaignDB, PlatformEnum, CampaignStatus, BudgetType
from app.models.campaign import (
    Campaign, CampaignCreate, CampaignUpdate
)

router = APIRouter(
    prefix="/campaigns",
    tags=["campaigns"],
    responses={404: {"description": "Não encontrado"}}
)

# --- CRUD Operations com Banco de Dados ---

@router.get("/", response_model=List[Campaign])
async def list_campaigns(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[CampaignStatus] = None,
    platform: Optional[PlatformEnum] = None,
    start_date_from: Optional[date] = None,
    start_date_to: Optional[date] = None
):
    """Lista campanhas com filtros opcionais"""
    query = db.query(CampaignDB)
    
    if status:
        query = query.filter(CampaignDB.status == status)
    if platform:
        query = query.filter(CampaignDB.platform == platform)
    if start_date_from:
        query = query.filter(CampaignDB.start_date >= start_date_from)
    if start_date_to:
        query = query.filter(CampaignDB.start_date <= start_date_to)
    
    campaigns = query.offset(skip).limit(limit).all()
    return campaigns


@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Busca uma campanha específica pelo ID"""
    campaign = db.query(CampaignDB).filter(CampaignDB.id == campaign_id).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campanha {campaign_id} não encontrada"
        )
    
    return campaign


@router.post("/", response_model=Campaign, status_code=status.HTTP_201_CREATED)
async def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    """Cria uma nova campanha"""
    
    # Converte date para datetime para o banco
    start_datetime = datetime.combine(campaign.start_date, datetime.min.time())
    end_datetime = datetime.combine(campaign.end_date, datetime.min.time()) if campaign.end_date else None
    
    db_campaign = CampaignDB(
        name=campaign.name,
        platform=campaign.platform,
        budget_type=campaign.budget_type,
        budget_amount=campaign.budget_amount,
        start_date=start_datetime,
        end_date=end_datetime,
        status=campaign.status,
        target_audience=campaign.target_audience,
        keywords=campaign.keywords,
        bid_strategy=campaign.bid_strategy,
        creative_url=campaign.creative_url,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    return db_campaign


@router.put("/{campaign_id}", response_model=Campaign)
async def update_campaign(
    campaign_id: int, 
    campaign_update: CampaignUpdate, 
    db: Session = Depends(get_db)
):
    """Atualiza uma campanha existente"""
    db_campaign = db.query(CampaignDB).filter(CampaignDB.id == campaign_id).first()
    
    if not db_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campanha {campaign_id} não encontrada"
        )
    
    update_data = campaign_update.dict(exclude_unset=True)
    
    # Converte date para datetime se end_date for atualizado
    if 'end_date' in update_data and update_data['end_date']:
        update_data['end_date'] = datetime.combine(update_data['end_date'], datetime.min.time())
    
    # Atualiza campos
    for key, value in update_data.items():
        setattr(db_campaign, key, value)
    
    db_campaign.updated_at = datetime.now()
    db.commit()
    db.refresh(db_campaign)
    
    return db_campaign


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Remove uma campanha"""
    db_campaign = db.query(CampaignDB).filter(CampaignDB.id == campaign_id).first()
    
    if not db_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campanha {campaign_id} não encontrada"
        )
    
    db.delete(db_campaign)
    db.commit()
    
    return None


@router.post("/{campaign_id}/pause", response_model=Campaign)
async def pause_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Pausa uma campanha"""
    db_campaign = db.query(CampaignDB).filter(CampaignDB.id == campaign_id).first()
    
    if not db_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campanha {campaign_id} não encontrada"
        )
    
    db_campaign.status = CampaignStatus.PAUSED
    db_campaign.updated_at = datetime.now()
    db.commit()
    db.refresh(db_campaign)
    
    return db_campaign


@router.post("/{campaign_id}/activate", response_model=Campaign)
async def activate_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Ativa uma campanha"""
    db_campaign = db.query(CampaignDB).filter(CampaignDB.id == campaign_id).first()
    
    if not db_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campanha {campaign_id} não encontrada"
        )
    
    db_campaign.status = CampaignStatus.ACTIVE
    db_campaign.updated_at = datetime.now()
    db.commit()
    db.refresh(db_campaign)
    
    return db_campaign


# --- Analytics & Reports ---

@router.get("/{campaign_id}/metrics")
async def get_campaign_metrics(campaign_id: int, db: Session = Depends(get_db)):
    """Retorna métricas detalhadas de uma campanha"""
    campaign = db.query(CampaignDB).filter(CampaignDB.id == campaign_id).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campanha {campaign_id} não encontrada"
        )
    
    # Cálculos
    ctr = (campaign.clicks / campaign.impressions * 100) if campaign.impressions > 0 else 0
    cpc = (campaign.total_spent / campaign.clicks) if campaign.clicks > 0 else 0
    conversion_rate = (campaign.conversions / campaign.clicks * 100) if campaign.clicks > 0 else 0
    
    return {
        "campaign_id": campaign_id,
        "campaign_name": campaign.name,
        "metrics": {
            "total_spent": round(campaign.total_spent, 2),
            "impressions": campaign.impressions,
            "clicks": campaign.clicks,
            "conversions": campaign.conversions,
            "ctr": round(ctr, 2),
            "cpc": round(cpc, 2),
            "conversion_rate": round(conversion_rate, 2),
            "budget_remaining": round(campaign.budget_amount - campaign.total_spent, 2),
            "budget_utilization": round((campaign.total_spent / campaign.budget_amount * 100), 2) if campaign.budget_amount > 0 else 0
        },
        "status": campaign.status,
        "platform": campaign.platform
    }


@router.get("/platform/{platform}/summary")
async def get_platform_summary(platform: PlatformEnum, db: Session = Depends(get_db)):
    """Resumo de todas as campanhas de uma plataforma"""
    platform_campaigns = db.query(CampaignDB).filter(CampaignDB.platform == platform).all()
    
    if not platform_campaigns:
        return {
            "platform": platform,
            "total_campaigns": 0,
            "message": f"Nenhuma campanha encontrada para {platform}"
        }
    
    total_spent = sum(c.total_spent for c in platform_campaigns)
    total_budget = sum(c.budget_amount for c in platform_campaigns)
    active_campaigns = len([c for c in platform_campaigns if c.status == CampaignStatus.ACTIVE])
    
    # Calcula CTR médio
    ctr_list = [
        (c.clicks / c.impressions * 100) if c.impressions > 0 else 0 
        for c in platform_campaigns
    ]
    avg_ctr = statistics.mean(ctr_list) if ctr_list else 0
    
    return {
        "platform": platform,
        "total_campaigns": len(platform_campaigns),
        "active_campaigns": active_campaigns,
        "total_spent": round(total_spent, 2),
        "total_budget": round(total_budget, 2),
        "budget_utilization": round((total_spent / total_budget * 100), 2) if total_budget > 0 else 0,
        "average_ctr": round(avg_ctr, 2)
    }


# --- Data Population (para testes) ---

@router.post("/populate-sample", response_model=List[Campaign])
async def populate_sample_data(db: Session = Depends(get_db)):
    """Popula com dados de exemplo para testes"""
    
    # Limpa tabela primeiro
    db.query(CampaignDB).delete()
    db.commit()
    
    sample_campaigns = [
        CampaignDB(
            name="Campanha Black Friday",
            platform=PlatformEnum.GOOGLE_ADS,
            budget_type=BudgetType.DAILY,
            budget_amount=500.00,
            start_date=datetime(2024, 11, 1, 10, 0, 0),
            end_date=datetime(2024, 11, 30, 23, 59, 59),
            status=CampaignStatus.ACTIVE,
            target_audience="25-45 anos, interessados em eletrônicos",
            keywords=["black friday", "ofertas", "desconto", "eletrônicos"],
            bid_strategy="maximize_conversions",
            creative_url="https://exemplo.com/banner.jpg",
            total_spent=2450.75,
            impressions=125000,
            clicks=3125,
            conversions=156,
            created_at=datetime(2024, 10, 15, 10, 30, 0),
            updated_at=datetime(2024, 10, 20, 14, 45, 0)
        ),
        CampaignDB(
            name="Lançamento App Mobile",
            platform=PlatformEnum.META_ADS,
            budget_type=BudgetType.LIFETIME,
            budget_amount=3000.00,
            start_date=datetime(2024, 10, 1, 9, 0, 0),
            status=CampaignStatus.ACTIVE,
            target_audience="18-35 anos, mobile users",
            keywords=["app", "mobile", "download", "lançamento"],
            bid_strategy="lowest_cost",
            total_spent=1875.50,
            impressions=89000,
            clicks=4450,
            conversions=89,
            created_at=datetime(2024, 9, 28, 9, 15, 0),
            updated_at=datetime(2024, 10, 10, 11, 20, 0)
        )
    ]
    
    db.add_all(sample_campaigns)
    db.commit()
    
    # Retorna as campanhas criadas
    for campaign in sample_campaigns:
        db.refresh(campaign)
    
    return sample_campaigns
