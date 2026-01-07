from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from app.services.meta_ads import meta_simulator
from app.services.google_ads import google_simulator  # Criaremos depois
import json

router = APIRouter(prefix="/api/ads", tags=["ads"])

# Meta Ads Endpoints
@router.get("/meta/campaigns")
async def get_meta_campaigns():
    """Lista campanhas do Meta Ads"""
    campaigns = meta_simulator.get_campaigns()
    return {
        "platform": "meta",
        "count": len(campaigns),
        "campaigns": campaigns,
        "simulated": True  # Indica que são dados de simulação
    }

@router.post("/meta/campaigns")
async def create_meta_campaign(campaign_data: Dict[str, Any]):
    """Cria nova campanha no Meta Ads"""
    required = ["name", "objective"]
    for field in required:
        if field not in campaign_data:
            raise HTTPException(400, f"Campo obrigatório: {field}")
    
    result = meta_simulator.create_campaign(
        name=campaign_data["name"],
        objective=campaign_data.get("objective", "CONVERSIONS"),
        daily_budget=campaign_data.get("daily_budget", 50.0)
    )
    
    return {
        "message": "Campanha criada com sucesso (simulação)",
        "data": result,
        "next_steps": [
            "Configure o token real do Meta Ads no .env",
            "Use META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN"
        ]
    }

@router.post("/meta/generate-creative")
async def generate_meta_creative(prompt: Dict[str, Any]):
    """Gera criativo para Meta Ads"""
    product = prompt.get("product", "produto")
    audience = prompt.get("audience", "empreendedores")
    
    creative = meta_simulator.generate_creative(product, audience)
    
    return {
        "platform": "meta",
        "prompt": prompt,
        "creative": creative,
        "tips": [
            "Use imagens de alta qualidade",
            "Inclua call-to-action claro",
            "Teste múltiplas variações"
        ]
    }

# Google Ads Endpoints (simulação)
@router.get("/google/campaigns")
async def get_google_campaigns():
    """Lista campanhas do Google Ads (simulado)"""
    return {
        "platform": "google",
        "count": 2,
        "campaigns": [
            {
                "id": "g1",
                "name": "Campanha Search - Palavras-chave",
                "type": "SEARCH",
                "status": "ENABLED",
                "budget": 75.00,
                "clicks": 420,
                "impressions": 8500,
                "ctr": 4.94
            },
            {
                "id": "g2",
                "name": "Campanha Display - Remarketing",
                "type": "DISPLAY",
                "status": "PAUSED", 
                "budget": 100.00,
                "clicks": 890,
                "impressions": 25000,
                "ctr": 3.56
            }
        ],
        "simulated": True
    }

@router.post("/analyze-segment")
async def analyze_segment(segment_data: Dict[str, Any]):
    """Analisa segmento para campanha"""
    demographics = segment_data.get("demographics", {})
    interests = segment_data.get("interests", [])
    
    analysis = {
        "segment_score": 85,
        "recommended_platforms": ["meta", "google"],
        "budget_recommendation": {
            "daily": 50.0,
            "monthly": 1500.0
        },
        "creative_tips": [
            f"Foco em: {', '.join(interests[:3]) if interests else 'audiência geral'}",
            "Use linguagem direta e benefícios claros",
            "Teste diferentes horários de publicação"
        ],
        "best_performing_formats": ["carousel", "video", "single_image"]
    }
    
    return {
        "analysis": analysis,
        "input_data": segment_data,
        "timestamp": "2024-01-06T23:00:00"
    }

@router.get("/performance")
async def get_performance(days: int = 7):
    """Retorna performance das campanhas"""
    return {
        "period_days": days,
        "total_impressions": 45000,
        "total_clicks": 2100,
        "total_spend": 1250.75,
        "avg_cpc": 0.60,
        "avg_ctr": 4.67,
        "conversions": 89,
        "cpa": 14.05,
        "platform_breakdown": {
            "meta": {"spend": 850.25, "conversions": 62},
            "google": {"spend": 400.50, "conversions": 27}
        }
    }
