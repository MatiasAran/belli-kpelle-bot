from flask import Flask, request
import requests
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configurações
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
CLIENT_TOKEN = os.getenv("CLIENT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

CHECKOUT_LINKS = {
    "2 meses": "https://checkout.ticto.app/OFC9448BB?pid=AF1A012565",
    "6 meses": "https://checkout.ticto.app/OAF938958?pid=AF1A012565",
    "12 meses": "https://checkout.ticto.app/OEB54D7D8?pid=AF1A012565"
}

IMAGENS = {
    "2 meses": "https://drive.google.com/uc?export=download&id=1ZCT5J_j5aapCu3KxAgLmVf15UNxg9hb1",
    "6 meses": "https://drive.google.com/uc?export=download&id=15xaD4SfMrwN6R4boFUPOP8-uZ-S4d_f4",
    "12 meses": "https://drive.google.com/uc?export=download&id=1CGppPn_A3o-factU31W7ofF19XFiKPBC"
}

def enviar_imagem(phone, img_url):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-image"
    payload = {
        "phone": phone,
        "image": img_url,
        "caption": "Belli K-Pelle - Veja como é o tratamento!"
    }
    headers = {
        "Content-Type": "application/json",
        "Client-Token": CLIENT_TOKEN
    }
    response = requests.post(url, json=payload, headers=headers)
    print("📸 Status envio imagem:", response.status_code)
    print("📸 Resposta envio imagem:", response.text)

def enviar_resposta(phone, reply):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    payload = {
        "phone": phone,
        "message": reply
    }
    headers = {
        "Content-Type": "application/json",
        "Client-Token": CLIENT_TOKEN
    }
    response = requests.post(url, json=payload, headers=headers)
    print("✅ Status envio Z-API:", response.status_code)
    print("✅ Resposta Z-API:", response.text)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Data recebida:", data)

    if data.get("fromMe", False):
        print("⚠️ Ignorando mensagem enviada por mim mesmo.")
        return "ok", 200

    sender = data.get("phone", "")
    message = data.get("text", {}).get("message", "")

    print(f"📨 Mensagem recebida de {sender}: {message}")

    # prompt base
    prompt = f"""
Você é uma atendente simpática, especialista em vendas do suplemento Belli K-Pelle.
Seu papel é responder as clientes interessadas no produto de forma empática e humanizada, como se fosse uma mulher de 45 anos que também já sofreu com problemas de cabelo, pele e unhas.

Características do produto:
- Belli K-Pelle é um suplemento natural que fortalece cabelos, unhas e melhora o aspecto da pele.
- Indicado especialmente para mulheres acima de 40 anos que sentem queda capilar, unhas fracas e pele sem viço.
- Cada pote dura 2 meses.

Opções de compra:
- Tratamento de 12 meses: {CHECKOUT_LINKS['12 meses']}
- Tratamento de 6 meses: {CHECKOUT_LINKS['6 meses']}
- Tratamento de 2 meses: {CHECKOUT_LINKS['2 meses']}

Seu objetivo é fazer a cliente se sentir segura para comprar, reforçando sutilmente os gatilhos mentais de segurança, confiança e benefício.

Quando perceber que a cliente está pronta para comprar, encaminhe automaticamente o seguinte plano, sem pedir que ela escolha:
A maioria das minhas clientes escolhe o plano de 6 meses porque ele oferece um ótimo custo-benefício, proporciona resultados mais duradouros e ainda conta com frete grátis! 🚚✨
Aqui está o link para garantir: {CHECKOUT_LINKS['6 meses']}

Sempre responda de forma acolhedora, com muitos emojis, gere conexão e faça perguntas abertas no final para manter a conversa fluindo.

Mensagem recebida: {message}
"""

    try:
        print("🧠 Enviando para OpenAI...")

        response = openai.chat.completions.create(
            model="gpt-4o",
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response.choices[0].message.content
        print("💬 Resposta gerada:", reply)

        # Verifica qual plano está na mensagem para enviar imagem correspondente
        for plano, link in CHECKOUT_LINKS.items():
            if link in reply:
                print(f"🖼️ Detectado plano: {plano}, enviando imagem correspondente...")
                enviar_imagem(sender, IMAGENS[plano])
                break

        enviar_resposta(sender, reply)

    except Exception as e:
        print("❌ Erro ao consultar OpenAI:", e)
        enviar_resposta(sender, "Desculpe, estou com um probleminha técnico agora. Pode tentar novamente em alguns minutos? 😊")

    return "ok", 200

if __name__ == '__main__':
    app.run(port=5000)
    
    @app.route("/")
def home():
    return "API rodando com sucesso!"

