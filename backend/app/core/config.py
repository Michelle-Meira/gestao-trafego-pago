from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Configurações básicas da aplicação
    APP_NAME: str = "Gestão de Tráfego Pago"
    DEBUG: bool = True
    
    # Banco de dados
    DATABASE_URL: str = "sqlite:///./gestao_trafego.db"
    
    # Segurança JWT
    SECRET_KEY: str = "sua-chave-secreta-aqui-minimo-32-caracteres-altere-isso-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Meta Ads (Facebook/Instagram) - Opcional
    META_APP_ID: Optional[str] = Field(default=None, description="App ID do Facebook Developers")
    META_APP_SECRET: Optional[str] = Field(default=None, description="App Secret do Facebook")
    META_ACCESS_TOKEN: Optional[str] = Field(default=None, description="Access Token de longa duração")
    META_AD_ACCOUNT_ID: Optional[str] = Field(default=None, description="ID da conta de anúncios (ex: act_123456789)")
    
    # Google Ads - Opcional
    GOOGLE_ADS_DEVELOPER_TOKEN: Optional[str] = None
    GOOGLE_ADS_CLIENT_ID: Optional[str] = None
    GOOGLE_ADS_CLIENT_SECRET: Optional[str] = None
    GOOGLE_ADS_REFRESH_TOKEN: Optional[str] = None
    GOOGLE_ADS_CUSTOMER_ID: Optional[str] = None
    
    # OpenAI para geração de textos - Opcional
    OPENAI_API_KEY: Optional[str] = None
    
    # Configurações de CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # ⚠️ IMPORTANTE: Ignora variáveis extras no .env

settings = Settings()

# Validação básica
if settings.DEBUG:
    print(f"⚙️ Configurações carregadas: {settings.APP_NAME}")
    if settings.META_APP_ID:
        print("✅ Meta Ads configurado")
    else:
        print("⚠️ Meta Ads não configurado (use .env)")
    
    if settings.OPENAI_API_KEY:
        print("✅ OpenAI configurado")
    else:
        print("⚠️ OpenAI não configurado (use .env para gerar textos com IA)")
