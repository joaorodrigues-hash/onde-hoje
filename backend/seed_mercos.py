import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from security import gerar_hash_senha

db_path = os.path.join(BASE_DIR, "roles_novo.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Cria a tabela de administradores caso não exista
cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    sobrenome TEXT,
                    email TEXT UNIQUE,
                    senha TEXT,
                    cargo TEXT)''')

avaliadores = [
    ("João", "Rodrigues", "joao.rodrigues@mercos.com", "12345", "master"),
    ("Renan", "Avaliador", "renan@mercos.com", "12345", "master"),
    ("Níler", "Barcelos", "niler.barcelos@mercos.com", "12345", "master")
]

for nome, sobrenome, email, senha, cargo in avaliadores:
    hash_senha = gerar_hash_senha(senha)
    try:
        cursor.execute("INSERT INTO admin (nome, sobrenome, email, senha, cargo) VALUES (?, ?, ?, ?, ?)",
                       (nome, sobrenome, email, hash_senha, cargo))
    except sqlite3.IntegrityError:
        cursor.execute("UPDATE admin SET senha=? WHERE email=?", (hash_senha, email))

conn.commit()
conn.close()
print("✅ Avaliadores da Mercos cadastrados com sucesso para o Painel Admin!")