import sys
sys.path.append('.')
from app.core.security import get_password_hash

print("🧪 Testando hash de senhas...")

# Senha curta (OK)
try:
    hash1 = get_password_hash("Admin123")
    print("✅ 'Admin123' -> Hash gerado")
except Exception as e:
    print(f"❌ Erro: {e}")

# Senha muito longa (deve truncar)
try:
    long_pwd = "A" * 100  # 100 caracteres
    hash2 = get_password_hash(long_pwd)
    print(f"✅ Senha longa ({len(long_pwd)} chars) -> Hash gerado (truncado automaticamente)")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
