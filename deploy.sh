#!/bin/bash
echo "🚀 Deploy do Sistema de Gestão de Tráfego"
echo "========================================"

# Verificar status
echo "📊 Status do Git:"
git status

# Adicionar alterações
echo "📦 Adicionando alterações..."
git add .

# Commit
read -p "✏️  Mensagem do commit: " commit_msg
git commit -m "$commit_msg"

# Push
echo "📤 Enviando para GitHub..."
git push origin main

echo "✅ Deploy concluído!"
echo "🌐 Acesse: https://github.com/michelle-meira/gestao-trafego-pago"
