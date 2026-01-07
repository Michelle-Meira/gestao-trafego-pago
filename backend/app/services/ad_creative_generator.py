"""
Gerador de textos criativos para anúncios usando IA
"""
import os
from typing import Dict, Any
import openai
from app.core.config import settings

# Configurar OpenAI se disponível
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY
    OPENAI_AVAILABLE = True
else:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI não configurado. Usando templates padrão.")

def generate_ad_creative(
    product: str,
    target_audience: str,
    tone: str = "profissional",
    platform: str = "meta"
) -> Dict[str, Any]:
    """
    Gera textos criativos para anúncios
    """
    
    if OPENAI_AVAILABLE:
        return _generate_with_openai(product, target_audience, tone, platform)
    else:
        return _generate_with_templates(product, target_audience, tone, platform)

def _generate_with_openai(product: str, audience: str, tone: str, platform: str) -> Dict[str, Any]:
    """Usa OpenAI para gerar textos"""
    try:
        prompt = f"""
        Gere um anúncio para {platform.upper()} com as seguintes características:
        
        Produto/Serviço: {product}
        Público-alvo: {audience}
        Tom: {tone}
        
        Forneça:
        1. Um HEADLINE impactante (máx 40 caracteres)
        2. Uma DESCRIÇÃO persuasiva (máx 125 caracteres)
        3. Um CALL-TO-ACTION claro
        4. 3 HASHTAGS relevantes
        5. Um texto para o campo "Texto Principal" (máx 200 caracteres)
        
        Formato em português do Brasil.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um copywriter especialista em marketing digital."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        # Parse simples da resposta
        lines = content.split('\n')
        result = {
            "headline": lines[1].replace("1. ", "").replace("HEADLINE: ", "") if len(lines) > 1 else f"Descubra {product}",
            "description": lines[2].replace("2. ", "").replace("DESCRIÇÃO: ", "") if len(lines) > 2 else f"Perfecto para {audience}",
            "cta": lines[3].replace("3. ", "").replace("CALL-TO-ACTION: ", "") if len(lines) > 3 else "Saiba Mais",
            "hashtags": lines[4].replace("4. ", "").split(", ") if len(lines) > 4 else [f"#{product.replace(' ', '')}"],
            "primary_text": lines[5].replace("5. ", "") if len(lines) > 5 else "",
            "generated_by": "openai_gpt"
        }
        
        return result
        
    except Exception as e:
        print(f"Erro ao usar OpenAI: {e}")
        return _generate_with_templates(product, audience, tone, platform)

def _generate_with_templates(product: str, audience: str, tone: str, platform: str) -> Dict[str, Any]:
    """Usa templates quando OpenAI não está disponível"""
    
    templates = {
        "profissional": {
            "headlines": [
                f"Solução Profissional para {product}",
                f"Eficiência em {product} para {audience}",
                f"Resultados Comprovados com {product}"
            ],
            "descriptions": [
                f"Maximize seus resultados com nossa solução em {product}. Ideal para {audience}.",
                f"Tecnologia avançada para {product}. Desenvolvido para {audience}.",
                f"Transforme sua abordagem com {product}. Solução completa para {audience}."
            ],
            "ctas": ["Solicitar Demonstração", "Agendar Consulta", "Baixar Material"]
        },
        "conversacional": {
            "headlines": [
                f"Descubra como {product} pode mudar seu dia a dia!",
                f"Você já conhece {product}? Perfeito para {audience}!",
                f"A revolução do {product} chegou!"
            ],
            "descriptions": [
                f"Junte-se a milhares de {audience} satisfeitos. Experimente {product} hoje mesmo!",
                f"Não espere mais para descobrir os benefícios do {product}. Feito para {audience} como você!",
                f"O que você está esperando? {product} é a solução que faltava para {audience}."
            ],
            "ctas": ["Experimente Grátis", "Começar Agora", "Quero Saber Mais"]
        }
    }
    
    import random
    template = templates.get(tone, templates["profissional"])
    
    return {
        "headline": random.choice(template["headlines"]),
        "description": random.choice(template["descriptions"]),
        "cta": random.choice(template["ctas"]),
        "hashtags": [f"#{product.replace(' ', '')}", f"#{audience.replace(' ', '')}", "#MarketingDigital"],
        "primary_text": f"{product} oferece a melhor solução para {audience}. Resultados comprovados e suporte especializado. Não perca esta oportunidade!",
        "generated_by": "template_system"
    }
