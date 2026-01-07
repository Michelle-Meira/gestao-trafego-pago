"""
Serviço REAL para Meta Ads (Facebook/Instagram)
Necessita configuração no .env:
- META_APP_ID
- META_APP_SECRET  
- META_ACCESS_TOKEN
- META_AD_ACCOUNT_ID
"""
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.exceptions import FacebookRequestError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class RealMetaAdsService:
    """Serviço real para Meta Ads API"""
    
    def __init__(self):
        self.initialized = False
        self._init_facebook_api()
    
    def _init_facebook_api(self):
        """Inicializa a API do Facebook"""
        try:
            if all([
                settings.META_APP_ID,
                settings.META_APP_SECRET, 
                settings.META_ACCESS_TOKEN
            ]):
                FacebookAdsApi.init(
                    app_id=settings.META_APP_ID,
                    app_secret=settings.META_APP_SECRET,
                    access_token=settings.META_ACCESS_TOKEN,
                    api_version='v18.0'
                )
                self.initialized = True
                logger.info("✅ Meta Ads API inicializada com sucesso")
            else:
                logger.warning("⚠️ Meta Ads não configurado. Configure no .env")
                self.initialized = False
                
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Meta Ads: {e}")
            self.initialized = False
    
    def get_campaigns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Busca campanhas reais da conta de ads"""
        if not self.initialized:
            return self._get_mock_campaigns()
        
        try:
            account = AdAccount(settings.META_AD_ACCOUNT_ID)
            campaigns = account.get_campaigns(fields=[
                'id', 'name', 'status', 'objective', 
                'daily_budget', 'lifetime_budget',
                'created_time', 'start_time', 'stop_time',
                'effective_status', 'bid_strategy'
            ], limit=limit)
            
            result = []
            for camp in campaigns:
                camp_data = {
                    'id': camp.get('id'),
                    'name': camp.get('name'),
                    'status': camp.get('status'),
                    'objective': camp.get('objective'),
                    'daily_budget': camp.get('daily_budget'),
                    'created_time': camp.get('created_time'),
                    'effective_status': camp.get('effective_status'),
                    'platform': 'meta'
                }
                result.append(camp_data)
            
            return result
            
        except FacebookRequestError as e:
            logger.error(f"Erro Meta API: {e}")
            return self._get_mock_campaigns()
        except Exception as e:
            logger.error(f"Erro geral: {e}")
            return self._get_mock_campaigns()
    
    def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma campanha REAL no Meta Ads"""
        if not self.initialized:
            return self._mock_create_campaign(campaign_data)
        
        try:
            account = AdAccount(settings.META_AD_ACCOUNT_ID)
            
            campaign = account.create_campaign(
                fields=[],
                params={
                    'name': campaign_data['name'],
                    'objective': campaign_data.get('objective', 'CONVERSIONS'),
                    'status': campaign_data.get('status', 'PAUSED'),
                    'special_ad_categories': [],
                    'daily_budget': campaign_data.get('daily_budget', 5000),  # Em centavos
                }
            )
            
            return {
                'success': True,
                'campaign_id': campaign.get_id(),
                'message': 'Campanha criada com sucesso no Meta Ads',
                'data': {
                    'id': campaign.get_id(),
                    'name': campaign_data['name'],
                    'platform': 'meta'
                }
            }
            
        except FacebookRequestError as e:
            error_msg = f"Erro ao criar campanha: {e.api_error_message()}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'simulated': True
            }
    
    def get_campaign_insights(self, campaign_id: str, days: int = 7) -> Dict[str, Any]:
        """Busca insights de performance da campanha"""
        if not self.initialized:
            return self._mock_insights(campaign_id, days)
        
        try:
            campaign = Campaign(campaign_id)
            insights = campaign.get_insights(fields=[
                'impressions', 'clicks', 'spend', 'cpc', 'cpm',
                'ctr', 'conversions', 'cost_per_conversion',
                'frequency', 'reach'
            ], params={
                'time_range': {
                    'since': f'{days}_days_ago',
                    'until': 'today'
                }
            })
            
            if insights:
                insight_data = insights[0]
                return {
                    'campaign_id': campaign_id,
                    'period_days': days,
                    'impressions': int(insight_data.get('impressions', 0)),
                    'clicks': int(insight_data.get('clicks', 0)),
                    'spend': float(insight_data.get('spend', 0)),
                    'cpc': float(insight_data.get('cpc', 0)),
                    'ctr': float(insight_data.get('ctr', 0)),
                    'conversions': int(insight_data.get('conversions', 0)),
                    'platform': 'meta',
                    'real_data': True
                }
            
            return self._mock_insights(campaign_id, days)
            
        except Exception as e:
            logger.error(f"Erro ao buscar insights: {e}")
            return self._mock_insights(campaign_id, days)
    
    def _get_mock_campaigns(self) -> List[Dict[str, Any]]:
        """Dados mock para desenvolvimento"""
        return [
            {
                'id': 'mock_1',
                'name': 'Campanha de Conversão - E-commerce',
                'status': 'ACTIVE',
                'objective': 'CONVERSIONS',
                'daily_budget': 100.00,
                'created_time': '2024-01-01T10:00:00',
                'impressions': 12500,
                'clicks': 350,
                'spend': 245.50,
                'platform': 'meta',
                'simulated': True
            },
            {
                'id': 'mock_2',
                'name': 'Campanha de Branding - Alcance',
                'status': 'PAUSED',
                'objective': 'REACH',
                'daily_budget': 50.00,
                'created_time': '2024-01-03T14:30:00',
                'impressions': 8900,
                'clicks': 210,
                'spend': 178.00,
                'platform': 'meta',
                'simulated': True
            }
        ]
    
    def _mock_create_campaign(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock para criação de campanha"""
        return {
            'success': True,
            'campaign_id': f"mock_{datetime.now().timestamp()}",
            'message': 'Campanha criada (modo simulação)',
            'data': {
                'id': f"mock_{datetime.now().timestamp()}",
                'name': data['name'],
                'objective': data.get('objective', 'CONVERSIONS'),
                'status': 'PAUSED',
                'daily_budget': data.get('daily_budget', 50.0),
                'platform': 'meta',
                'simulated': True
            },
            'next_steps': [
                'Configure META_APP_ID, META_APP_SECRET e META_ACCESS_TOKEN no .env',
                'Adicione META_AD_ACCOUNT_ID da sua conta de anúncios'
            ]
        }
    
    def _mock_insights(self, campaign_id: str, days: int) -> Dict[str, Any]:
        """Mock para insights"""
        import random
        return {
            'campaign_id': campaign_id,
            'period_days': days,
            'impressions': random.randint(1000, 10000),
            'clicks': random.randint(50, 500),
            'spend': random.uniform(50.0, 500.0),
            'cpc': random.uniform(0.5, 2.5),
            'ctr': random.uniform(1.0, 5.0),
            'conversions': random.randint(5, 50),
            'platform': 'meta',
            'simulated': True
        }

# Instância global do serviço
meta_ads_service = RealMetaAdsService()
