from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

class GoogleAdsSimulator:
    """Simulador de Google Ads para desenvolvimento"""
    
    def __init__(self):
        self.keywords = [
            "gestão de tráfego pago",
            "facebook ads curso",
            "google ads profissional",
            "marketing digital",
            "anúncios online"
        ]
    
    def get_keyword_suggestions(self, product: str) -> List[Dict[str, Any]]:
        """Sugere palavras-chave para campanha"""
        base_keywords = [f"{product} {mod}" for mod in [
            "preço", "como usar", "melhor", "curso", "tutorial", 
            "funciona", "vale a pena", "2024", "grátis"
        ]]
        
        suggestions = []
        for kw in base_keywords[:5] + random.sample(self.keywords, 3):
            suggestions.append({
                "keyword": kw,
                "monthly_searches": random.randint(1000, 10000),
                "competition": random.choice(["LOW", "MEDIUM", "HIGH"]),
                "cpc_range": f"R$ {random.uniform(0.5, 5.0):.2f} - R$ {random.uniform(5.0, 15.0):.2f}"
            })
        
        return suggestions
    
    def estimate_performance(self, budget: float, keywords: List[str]) -> Dict[str, Any]:
        """Estima performance da campanha"""
        estimated = {
            "daily_budget": budget,
            "estimated_impressions": int(budget * 80),
            "estimated_clicks": int(budget * 4),
            "estimated_ctr": random.uniform(3.0, 7.0),
            "estimated_cpc": budget / (budget * 4) if budget > 0 else 0,
            "keywords_analyzed": len(keywords),
            "recommended_max_cpc": budget * 0.8 / (budget * 4) if budget > 0 else 0.5
        }
        
        return estimated

google_simulator = GoogleAdsSimulator()
