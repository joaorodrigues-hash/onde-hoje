import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "roles_novo.db")

def obter_conexao():
    """Retorna uma conexão ativa com o banco SQLite."""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome ou índice
    return conn

# Alias de compatibilidade caso alguma rota antiga use outro nome
get_db = obter_conexao
get_connection = obter_conexao

def iniciar_banco():
    """Cria as tabelas essenciais caso o banco ainda não exista."""
    conn = obter_conexao()
    cursor = conn.cursor()

    # 1. Tabela de Categorias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    """)

    # 2. Tabela de Parceiros / Produtores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parceiros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnpj TEXT UNIQUE NOT NULL,
            razao_social TEXT NOT NULL,
            nome_fantasia TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL
        )
    """)

    # 3. Tabela de Eventos / Rolês
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            venue TEXT NOT NULL,
            estado TEXT NOT NULL,
            cidade TEXT NOT NULL,
            price TEXT NOT NULL,
            category TEXT NOT NULL,
            image TEXT,
            tipo_imagem TEXT DEFAULT 'url',
            descricao TEXT,
            link_ingresso TEXT,
            observacao_interna TEXT,
            data_evento TEXT,
            likes INTEGER DEFAULT 0,
            clicks_share INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pendente',
            data_criacao TEXT,
            parceiro_id INTEGER DEFAULT 0
        )
    """)

    # 4. Tabela de Administradores / Equipe Mercos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            cargo TEXT DEFAULT 'moderador'
        )
    """)

    conn.commit()
    conn.close()