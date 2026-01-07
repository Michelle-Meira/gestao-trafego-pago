import sys
sys.path.append('.')
from app.core.security import get_password_hash

# Teste senhas
test_passwords = [
    "short",
    "Admin123",  # OK
    "a" * 100,   # Muito longa
]

for pwd in test_passwords:
    try:
        hash = get_password_hash(pwd)
        print(f"✅ '{pwd[:10]}...' -> Hash gerado")
    except Exception as e:
        print(f"❌ '{pwd[:10]}...' -> Erro: {e}")
