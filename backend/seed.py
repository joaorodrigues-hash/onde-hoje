import sqlite3
import os
import random
from datetime import datetime, timedelta

# Garante a importação correta de security.py independente de onde o script for executado
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from security import gerar_hash_senha

DATABASE_URL = os.path.join(BASE_DIR, "roles_novo.db")

def popular_banco():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    print("→ Iniciando carga de dados no banco...")

    # 1. Garantir Categorias
    categorias = [
        "Festas", "Sertanejo", "Música ao Vivo", "Eletrônica", 
        "Rock", "Samba", "Pagode", "Stand-up", "Jazz", "Hip-hop"
    ]
    for cat in categorias:
        cursor.execute("INSERT OR IGNORE INTO categorias (nome) VALUES (?)", (cat,))

    # 2. Cadastro de Parceiros Realistas
    parceiros_base = [
        ("11.222.333/0001-01", "Vila Madalena Entretenimento LTDA", "Vila Country Lounge", "contato@vilacountry.com.br", "São Paulo", "SP", "Marcos", "Silveira"),
        ("22.333.444/0001-02", "Lapa Boemia & Música Bar ME", "Beco do Samba Lapa", "contato@becodosamba.com.br", "Rio de Janeiro", "RJ", "Camila", "Ferreira"),
        ("33.444.555/0001-03", "Batel Nightlife & Eventos LTDA", "Ópera Rock House", "eventos@operarock.com.br", "Curitiba", "PR", "Rodrigo", "Albuquerque"),
        ("44.555.666/0001-04", "Savassi Pubs e Gastronomia EIRELI", "Savassi Jazz Club", "contato@savassijazz.com.br", "Belo Horizonte", "MG", "Larissa", "Mendes"),
        ("55.666.777/0001-05", "Lagoa Sunset Entretenimento LTDA", "Sunset Beach Garden", "contato@sunsetgarden.com.br", "Florianópolis", "SC", "Lucas", "Santoro"),
        ("66.777.888/0001-06", "Pelô Cultural Eventos ME", "Casa do Axé & Roda", "contato@pelocultural.com.br", "Salvador", "BA", "Tatiane", "Ribeiro"),
        ("77.888.999/0001-07", "Moinhos Shows e Baladas LTDA", "Moinhos Live Stage", "contato@moinhoslive.com.br", "Porto Alegre", "RS", "Guilherme", "Castro"),
        ("88.999.000/0001-08", "Setor Marista Lounge Bar ME", "Goiano Modão Bar", "contato@goianomodao.com.br", "Goiânia", "GO", "Felipe", "Barros"),
        ("99.000.111/0001-09", "Asa Sul Shows e Eventos EIRELI", "Brasília Beat Club", "contato@bsbbeat.com.br", "Brasília", "DF", "Renata", "Vasconcelos"),
        ("10.111.222/0001-10", "Campinas Night Entertainment LTDA", "Campinas Rooftop Pub", "contato@campinasrooftop.com.br", "Campinas", "SP", "Thiago", "Nunes"),
        ("20.222.333/0001-11", "BC Nightlife Group LTDA", "Ocean Club BC", "contato@oceanclub.com.br", "Balneário Camboriú", "SC", "Fernanda", "Lima"),
        ("30.333.444/0001-12", "Santos Beira Mar Entretenimento LTDA", "Santos Beach Lounge", "contato@santosbeach.com.br", "Santos", "SP", "André", "Martins")
    ]

    parceiros_ids = []
    senha_padrao_hash = gerar_hash_senha("parceiro123")

    for cnpj, razao, fantasia, email, cid, uf, nome, sobrenome in parceiros_base:
        cursor.execute("SELECT id FROM parceiros WHERE cnpj = ?", (cnpj,))
        row = cursor.fetchone()
        if row:
            parceiros_ids.append(row[0])
        else:
            cursor.execute("""
                INSERT INTO parceiros (cnpj, razao_social, nome_fantasia, email, senha, cidade, estado, nome, sobrenome)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (cnpj, razao, fantasia, email, senha_padrao_hash, cid, uf, nome, sobrenome))
            parceiros_ids.append(cursor.lastrowid)

    print(f"✓ {len(parceiros_ids)} parceiros cadastrados/validados.")

    # 3. Bancos de Imagens por Categoria
    imagens_cat = {
        "Festas": [
            "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800",
            "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800",
            "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=800"
        ],
        "Sertanejo": [
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800",
            "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=800"
        ],
        "Música ao Vivo": [
            "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800",
            "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=800"
        ],
        "Eletrônica": [
            "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800",
            "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=800",
            "https://images.unsplash.com/photo-1516873240891-4bf014598ab4?w=800"
        ],
        "Rock": [
            "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?w=800",
            "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=800"
        ],
        "Samba": [
            "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800",
            "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800"
        ],
        "Pagode": [
            "https://images.unsplash.com/photo-1520523839898-507125cd53c1?w=800"
        ],
        "Stand-up": [
            "https://images.unsplash.com/photo-1585699324551-f6c309eedeca?w=800"
        ],
        "Jazz": [
            "https://images.unsplash.com/photo-1511192336575-5a79af67a629?w=800"
        ],
        "Hip-hop": [
            "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800"
        ]
    }

    # Cidades e Locais Realistas por UF
    locais_brasil = [
        ("SP", "São Paulo", ["Vila Madalena", "Audio Club", "Espaço Unimed", "Cine Joia", "Beco do Batman"]),
        ("SP", "Campinas", ["Galleria Hall", "Sousas Lounge", "Campinas Hall"]),
        ("SP", "Santos", ["Praia do Gonzaga", "Mendes Convention Center", "Arena Santos"]),
        ("RJ", "Rio de Janeiro", ["Circo Voador", "Fundição Progresso", "Beco das Garrafas", "Marina da Glória"]),
        ("RJ", "Niterói", ["Reserva Cultural Niterói", "Charitas Deck Lounge"]),
        ("PR", "Curitiba", ["Pedreira Paulo Leminski", "Ópera de Arame", "Crossroads", "Largo da Ordem"]),
        ("PR", "Londrina", ["Igapó Stage", "Parque Ney Braga"]),
        ("SC", "Florianópolis", ["P12 Jurerê", "Stage Music Park", "Lagoa da Conceição"]),
        ("SC", "Balneário Camboriú", ["Green Valley Club", "Barra Sul Rooftop"]),
        ("MG", "Belo Horizonte", ["Parque das Mangabeiras", "Distrital Cruzeiro", "Savassi Pub"]),
        ("RS", "Porto Alegre", ["Opinião", "Auditório Araújo Vianna", "Cais Embarcadero"]),
        ("BA", "Salvador", ["Pelourinho Histórico", "Concha Acústica", "Rio Vermelho Deck"]),
        ("GO", "Goiânia", ["Arena Goiânia", "Parque Vaca Brava Lounge", "Setor Marista"]),
        ("DF", "Brasília", ["Pontão do Lago Sul", "Arena BRB", "Bier Fass"])
    ]

    nomes_eventos_base = {
        "Festas": ["Noite Open Bar & DJ Set", "Festa Sunset Neon", "Baile do Encontro", "White Party Exclusive", "After Hours Club"],
        "Sertanejo": ["Sexta Sertaneja Universitária", "Modão de Viola & Costela", "Violada dos Amigos", "Noite de Boteco & Modão"],
        "Música ao Vivo": ["Voz e Violão no Deck", "Sessão Acústica Especial", "Noite Autoral & Covers", "Quinta Acústica"],
        "Eletrônica": ["Underground Techno Night", "Sunset House Sessions", "Deep Vibes Festival", "Bass & Synth Experience"],
        "Rock": ["Noite dos Clássicos do Rock", "Tributo Rock Anos 90", "Festival Indie & Grunge", "Heavy Riff Night"],
        "Samba": ["Roda de Samba Tradicional", "Feijoada com Samba de Raiz", "Batucada no Quintal", "Samba de Primeira"],
        "Pagode": ["Tardezinha do Pagode", "Pagode de Domingo", "Encontro das Tribos Pagodeiras", "Cerveja Gelada & Pagodinho"],
        "Stand-up": ["Noite da Comédia Ao Vivo", "Show de Stand-up com Convidados", "Palco Aberto & Risadas"],
        "Jazz": ["Noite do Jazz & Blues", "Jam Session Jam & Soul", "Jazz sob as Estrelas"],
        "Hip-hop": ["Batalha de MCs & Boom Bap", "Trap & Hip-hop Nation", "Cypher no Beco"]
    }

    hoje = datetime.now()
    eventos_gerados = []

    # 4. Gerar 75 Eventos Futuros (Próximos dias e meses de 2026)
    for i in range(75):
        uf, cidade, venues = random.choice(locais_brasil)
        categoria = random.choice(categorias)
        titulo_base = random.choice(nomes_eventos_base[categoria])
        titulo = f"{titulo_base} #{i+1}"
        venue = random.choice(venues)
        
        dias_a_frente = random.randint(1, 90)
        data_evento = (hoje + timedelta(days=dias_a_frente)).strftime("%Y-%m-%d")
        
        preco = random.choice(["Gratuito", "R$ 20,00", "R$ 35,00", "R$ 50,00", "R$ 70,00", "R$ 100,00", "R$ 150,00"])
        imagem = random.choice(imagens_cat[categoria])
        descricao = f"Venha participar de {titulo} em {cidade}! O melhor da cena de {categoria} reunido em um único local com estrutura de alta qualidade."
        link_ingresso = "https://sympla.com.br" if preco != "Gratuito" else ""
        likes = random.randint(15, 650)
        clicks_share = int(likes * random.uniform(0.15, 0.45))
        parceiro_id = random.choice(parceiros_ids)

        eventos_gerados.append((
            titulo, venue, uf, cidade, preco, categoria, imagem, "url",
            descricao, link_ingresso, "", data_evento, likes, clicks_share, "aprovado",
            (hoje - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"), parceiro_id
        ))

    # 5. Gerar 30 Eventos Passados (Arquivo Histórico)
    for i in range(30):
        uf, cidade, venues = random.choice(locais_brasil)
        categoria = random.choice(categorias)
        titulo = f"Edição Histórica: {random.choice(nomes_eventos_base[categoria])}"
        venue = random.choice(venues)
        
        dias_atras = random.randint(10, 400)
        data_evento = (hoje - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
        
        preco = random.choice(["Gratuito", "R$ 30,00", "R$ 40,00", "R$ 60,00"])
        imagem = random.choice(imagens_cat[categoria])
        descricao = f"Evento já encerrado realizado em {cidade}. Uma grande noite de celebração para o público de {categoria}."
        likes = random.randint(100, 1200)
        clicks_share = int(likes * random.uniform(0.2, 0.5))
        parceiro_id = random.choice(parceiros_ids)

        eventos_gerados.append((
            titulo, venue, uf, cidade, preco, categoria, imagem, "url",
            descricao, "", "", data_evento, likes, clicks_share, "aprovado",
            (hoje - timedelta(days=dias_atras + 5)).strftime("%Y-%m-%d"), parceiro_id
        ))

    # 6. Gerar 10 Eventos Pendentes com Notas ao Moderador
    notas_moderacao = [
        "Verificar se o valor do ingresso já é o lote 2.",
        "Cartaz promocional enviado diretamente pela assessoria da banda.",
        "Favor checar a idade mínima da entrada (18+).",
        "Produtor confirmou horário de abertura dos portões às 19h.",
        "Evento solidário com doação de 1kg de alimento na portaria."
    ]

    for i in range(10):
        uf, cidade, venues = random.choice(locais_brasil)
        categoria = random.choice(categorias)
        titulo = f"Proposta Nova: {random.choice(nomes_eventos_base[categoria])}"
        venue = random.choice(venues)
        data_evento = (hoje + timedelta(days=random.randint(5, 45))).strftime("%Y-%m-%d")
        preco = random.choice(["Gratuito", "R$ 25,00", "R$ 45,00"])
        imagem = random.choice(imagens_cat[categoria])
        obs = random.choice(notas_moderacao)

        eventos_gerados.append((
            titulo, venue, uf, cidade, preco, categoria, imagem, "url",
            "Evento submetido para moderação antes da publicação oficial.",
            "https://sympla.com.br", obs, data_evento, 0, 0, "pendente",
            hoje.strftime("%Y-%m-%d"), 0
        ))

    # 7. Inserção em Massa no Banco
    cursor.executemany("""
        INSERT INTO roles (
            title, venue, estado, cidade, price, category, image, tipo_imagem,
            descricao, link_ingresso, observacao_interna, data_evento,
            likes, clicks_share, status, data_criacao, parceiro_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, eventos_gerados)

    conn.commit()
    conn.close()

    print(f"✓ {len(eventos_gerados)} eventos inseridos com sucesso!")
    print(f"  - {75} Eventos Futuros (feed principal)")
    print(f"  - {30} Eventos Passados (arquivo histórico)")
    print(f"  - {10} Eventos Pendentes (fila de moderação)")
    print("✓ Povoamento concluído com êxito!")

if __name__ == "__main__":
    popular_banco()