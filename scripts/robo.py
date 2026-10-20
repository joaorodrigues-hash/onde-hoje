import requests
import time

print("🤖 Robô Caçador de Rolês Iniciado...")

eventos_raspados = [
    {
        "title": "Tardezinha do Pagode", 
        "venue": "Clube de Campo", 
        "price": "Portaria", 
        "category": "Música ao Vivo", 
        "image": "https://images.unsplash.com/photo-1514525253344-f81bcc353c58?w=500",
        "descricao": "Tardezinha especial com muito pagode retrô e cerveja gelada."
    },
    {
        "title": "Eletrônica Underground", 
        "venue": "Galpão Abandonado", 
        "price": "Ingresso Antecipado", 
        "category": "Eletrônica", 
        "image": "https://images.unsplash.com/photo-1622909589989-746803dfa348?w=500",
        "descricao": "DJs internacionais comandando a pista até o amanhecer."
    },
    {
        "title": "Noite do Karaokê Anos 80", 
        "venue": "Bar Neon", 
        "price": "Entrada Free", 
        "category": "Festas", 
        "image": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=500",
        "descricao": "Venha soltar a voz com os maiores clássicos dos anos 80 e 90."
    }
]

URL_SUA_API = "http://127.0.0.1:8000/roles/sugerir"

print(f"📡 Encontrei {len(eventos_raspados)} eventos. Enviando para análise...")

for evento in eventos_raspados:
    payload = {
        "title": evento["title"],
        "venue": evento["venue"],
        "estado": "SP",
        "cidade": "São Paulo", 
        "price": evento["price"],
        "category": evento["category"],
        "image": evento["image"],
        "descricao": evento["descricao"],
        "link_ingresso": "https://sympla.com.br",
        "parceiro_id": 0
    }
    
    # Enviando via JSON body (compatível com FastAPI / Pydantic)
    resposta = requests.post(URL_SUA_API, json=payload)
    
    if resposta.status_code == 200:
        print(f"✅ Enviado com sucesso: {evento['title']}")
    else:
        print(f"❌ Erro ao enviar: {evento['title']} - Status: {resposta.status_code}")
    
    time.sleep(1)

print("🏁 Trabalho concluído! Eventos aguardando moderação no banco.")