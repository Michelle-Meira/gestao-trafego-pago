import sys
sys.path.append('.')
from app.core.security import get_password_hash, verify_password

print("🧪 Testando SHA256...")

# Teste 1: Hash básico
pwd = "Admin123"
hash = get_password_hash(pwd)
print(f"✅ Hash gerado: {hash[:50]}...")

# Teste 2: Verificação
if verify_password(pwd, hash):
    print("✅ Verificação OK")
else:
    print("❌ Verificação falhou")

# Teste 3: Senha longa
long_pwd = "A" * 1000
try:
    hash_long = get_password_hash(long_pwd)
    print(f"✅ Senha longa (1000 chars) -> Hash gerado")
except Exception as e:
    print(f"❌ Erro: {e}")
