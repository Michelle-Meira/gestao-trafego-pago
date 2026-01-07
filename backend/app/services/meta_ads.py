from typing import Dict, Any, List, Optional
from datetime import datetime
import json

class MetaAdsSimulator:
    """Simulador seguro de Meta Ads para desenvolvimento"""
    
    def __init__(self):
        self.campaigns = []
        self.adsets = []
        self.ads = []
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Carrega dados de exemplo"""
        self.campaigns = [
            {
                "id": "1",
                "name": "Campanha Inicial - Conversões",
                "objective": "CONVERSIONS",
                "status": "ACTIVE",
                "daily_budget": 50.00,
                "created_time": "2024-01-05T10:00:00",
                "impressions": 12500,
                "clicks": 350,
                "spend": 245.50
            },
            {
                "id": "2", 
                "name": "Campanha Branding - Alcance",
                "objective": "REACH",
                "status": "PAUSED",
                "daily_budget": 30.00,
                "created_time": "2024-01-03T14:30:00",
                "impressions": 8900,
                "clicks": 210,
                "spend": 178.00
            }
        ]
    
    def get_campaigns(self) -> List[Dict[str, Any]]:
        """Lista campanhas (simulado)"""
        return self.campaigns
    
    def create_campaign(self, name: str, objective: str = "CONVERSIONS", 
                       daily_budget: float = 50.0) -> Dict[str, Any]:
        """Cria nova campanha (simulado)"""
        campaign = {
            "id": str(len(self.campaigns) + 1),
            "name": name,
            "objective": objective,
            "status": "PAUSED",  # Começa pausada
            "daily_budget": daily_budget,
            "created_time": datetime.now().isoformat(),
            "impressions": 0,
            "clicks": 0,
            "spend": 0.0
        }
        self.campaigns.append(campaign)
        return {"success": True, "campaign": campaign}
    
    def generate_creative(self, product: str, audience: str) -> Dict[str, Any]:
        """Gera texto criativo para anúncios"""
        creatives = {
            "headlines": [
                f"Descubra como {product} pode transformar seu negócio!",
                f"{audience}: A solução definitiva para {product}",
                f"Pare de perder tempo com {product} ineficientes",
                f"Revolucione sua abordagem com {product}"
            ],
            "descriptions": [
                f"Especialmente desenvolvido para {audience}. Resultados comprovados em 30 dias.",
                f"Junte-se a milhares de {audience} satisfeitos. Método testado e aprovado.",
                f"Não espere mais para otimizar seus resultados. Solução completa para {audience}."
            ],
            "ctas": ["Saiba Mais", "Comece Agora", "Teste Grátis", "Solicitar Demonstração"]
        }
        
        import random
        return {
            "headline": random.choice(creatives["headlines"]),
            "description": random.choice(creativas["descriptions"]),
            "cta": random.choice(creatives["ctas"]),
            "platform": "meta",
            "generated_at": datetime.now().isoformat()
        }

meta_simulator = MetaAdsSimulator()
