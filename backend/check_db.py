import sys
sys.path.append('.')
from app.database import SessionLocal
from app.schemas.campaign_db import CampaignDB

db = SessionLocal()
try:
    campaigns = db.query(CampaignDB).order_by(CampaignDB.id).all()
    print("📊 CAMPANHAS NO BANCO:")
    print("-" * 80)
    for c in campaigns:
        print(f"ID: {c.id} | Nome: {c.name[:30]:30} | Status: {c.status:10} | Plataforma: {c.platform:15} | Budget: R${c.budget_amount:.2f}")
    print(f"\nTotal: {len(campaigns)} campanhas")
finally:
    db.close()
