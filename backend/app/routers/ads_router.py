"""
Router REAL para APIs de Ads com Meta e Google Ads
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

from app.services.meta_ads_service import meta_ads_service
# from app.services.google_ads_service import google_ads_service  # Adicionaremos depois
from app.services.ad_creative_generator import generate_ad_creative  # Vamos criar

router = APIRouter(prefix="/api/ads", tags=["Ads"])

# Models Pydantic
class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    objective: str = Field(default="CONVERSIONS", pattern="^(CONVERSIONS|REACH|TRAFFIC|ENGAGEMENT)$")
    daily_budget: float = Field(default=50.0, gt=0)
    status: str = Field(default="PAUSED", pattern="^(PAUSED|ACTIVE)$")

class CreativeRequest(BaseModel):
    product: str
    target_audience: str
    tone: str = "profissional"
    platform: str = "meta"

class SegmentAnalysisRequest(BaseModel):
    demographics: Dict[str, Any]
    interests: List[str]
    budget_range: Dict[str, float]

# Meta Ads Endpoints
@router.get("/meta/campaigns")
async def get_meta_campaigns(limit: int = 10):
    """Lista campanhas reais do Meta Ads"""
    campaigns = meta_ads_service.get_campaigns(limit=limit)
    
    return {
        "platform": "meta",
        "count": len(campaigns),
        "campaigns": campaigns,
        "has_real_connection": meta_ads_service.initialized,
        "timestamp": datetime.now().isoformat()
    }

@router.post("/meta/campaigns")
async def create_meta_campaign(campaign: CampaignCreate):
    """Cria campanha REAL no Meta Ads"""
    result = meta_ads_service.create_campaign({
        "name": campaign.name,
        "objective": campaign.objective,
        "daily_budget": campaign.daily_budget,
        "status": campaign.status
    })
    
    return {
        "success": result["success"],
        "message": result["message"],
        "data": result.get("data", {}),
        "requires_config": not meta_ads_service.initialized,
        "config_instructions": result.get("next_steps", []) if not meta_ads_service.initialized else None
    }

@router.get("/meta/campaigns/{campaign_id}/insights")
async def get_campaign_insights(campaign_id: str, days: int = 7):
    """Busca insights de performance da campanha"""
    insights = meta_ads_service.get_campaign_insights(campaign_id, days)
    
    return {
        "campaign_id": campaign_id,
        "insights": insights,
        "period_days": days,
        "platform": "meta"
    }

# Gerador de Criativos com IA
@router.post("/generate-creative")
async def generate_creative(request: CreativeRequest):
    """Gera texto criativo para anúncios usando IA"""
    creative = generate_ad_creative(
        product=request.product,
        target_audience=request.target_audience,
        tone=request.tone,
        platform=request.platform
    )
    
    return {
        "platform": request.platform,
        "product": request.product,
        "audience": request.target_audience,
        "creative": creative,
        "generated_at": datetime.now().isoformat(),
        "tips": [
            "Use imagens de alta qualidade (1080x1080 para Instagram, 1200x628 para Facebook)",
            "Inclua call-to-action claro",
            "Teste múltiplas variações (A/B Testing)",
            "Otimize para mobile-first"
        ]
    }

# Análise de Segmento
@router.post("/analyze-segment")
async def analyze_segment(request: SegmentAnalysisRequest):
    """Analisa segmento e recomenda estratégia"""
    # Análise básica - depois implementamos ML
    audience_size = "MÉDIO" if len(request.interests) > 3 else "PEQUENO"
    
    recommended_budget = {
        "daily_min": request.budget_range.get("min", 20.0),
        "daily_max": request.budget_range.get("max", 100.0),
        "recommended": (request.budget_range.get("min", 20.0) + request.budget_range.get("max", 100.0)) / 2
    }
    
    platforms = []
    if "facebook" in str(request.interests).lower() or "instagram" in str(request.interests).lower():
        platforms.append("meta")
    if "google" in str(request.interests).lower() or "search" in str(request.interests).lower():
        platforms.append("google")
    if not platforms:
        platforms = ["meta", "google"]  # padrão
    
    return {
        "segment_score": 78,  # Score de 0-100
        "audience_size": audience_size,
        "recommended_platforms": platforms,
        "budget_recommendation": recommended_budget,
        "creative_strategy": {
            "primary_focus": request.interests[0] if request.interests else "benefícios do produto",
            "tone": "conversacional" if "young" in str(request.demographics).lower() else "profissional",
            "key_messages": [
                f"Solução para {request.demographics.get('age_group', 'seu público')}",
                f"Foco em: {', '.join(request.interests[:3])}" if request.interests else "Benefícios principais"
            ]
        },
        "optimization_tips": [
            "Comece com orçamento baixo e escale gradualmente",
            "Monitore performance diariamente nas primeiras 72h",
            "Teste pelo menos 3 imagens diferentes por campanha",
            "Use remarketing para quem interagiu"
        ]
    }

# Performance Dashboard
@router.get("/performance")
async def get_overall_performance(days: int = 30):
    """Retorna performance geral das campanhas"""
    # Aqui integraríamos com dados reais das APIs
    # Por enquanto, mock dados
    
    return {
        "period_days": days,
        "summary": {
            "total_campaigns": 8,
            "active_campaigns": 5,
            "total_spend": 3250.75,
            "total_conversions": 142,
            "average_cpa": 22.89,
            "average_roas": 3.2
        },
        "platform_breakdown": {
            "meta": {
                "spend": 2250.50,
                "conversions": 98,
                "cpa": 22.96,
                "top_performing_campaign": "Conversão E-commerce"
            },
            "google": {
                "spend": 1000.25,
                "conversions": 44,
                "cpa": 22.73,
                "top_performing_campaign": "Search Brand"
            }
        },
        "trends": {
            "spend_trend": "up",
            "conversion_trend": "up",
            "cpa_trend": "down"
        }
    }

@router.get("/health")
async def ads_health():
    """Health check das APIs de Ads"""
    return {
        "meta_ads": {
            "connected": meta_ads_service.initialized,
            "status": "operational" if meta_ads_service.initialized else "needs_config"
        },
        "google_ads": {
            "connected": False,
            "status": "not_implemented"
        },
        "timestamp": datetime.now().isoformat()
    }
