import sys
sys.path.append('.')
from app.database import Base, engine
from app.schemas.campaign_db import CampaignDB
from app.schemas.user_db import UserDB

print("🔄 Atualizando banco de dados com autenticação...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas/atualizadas:")
print("   - campaigns")
print("   - users")
