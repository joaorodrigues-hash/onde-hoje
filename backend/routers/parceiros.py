from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import sqlite3
from database import get_db
from security import gerar_hash_senha, verificar_senha

router = APIRouter(prefix="/parceiros", tags=["Parceiros"])

class LoginParceiroSchema(BaseModel):
    email: str
    senha: str

class ParceiroSchema(BaseModel):
    cnpj: str
    razao_social: str
    nome_fantasia: str
    email: str
    senha: str
    cidade: str
    estado: str
    nome: str
    sobrenome: str

class AtualizarPerfilSchema(BaseModel):
    razao_social: str
    nome_fantasia: str
    cidade: str
    estado: str
    nome: str
    sobrenome: str
    email: str
    senha_antiga: str = ""
    senha_nova: str = ""

@router.post("/login")
def login_parceiro(dados: LoginParceiroSchema, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, email, senha, nome_fantasia FROM parceiros WHERE email = ?", (dados.email,))
    parceiro = cursor.fetchone()
    
    if parceiro and verificar_senha(dados.senha, parceiro["senha"]):
        return {
            "id": parceiro["id"],
            "email": parceiro["email"],
            "nome_fantasia": parceiro["nome_fantasia"]
        }
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@router.post("/cadastrar")
def cadastrar(dados: ParceiroSchema, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    try:
        senha_hash = gerar_hash_senha(dados.senha)
        cursor.execute("""
            INSERT INTO parceiros (cnpj, razao_social, nome_fantasia, email, senha, cidade, estado, nome, sobrenome)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (dados.cnpj, dados.razao_social, dados.nome_fantasia, dados.email, senha_hash, dados.cidade, dados.estado, dados.nome, dados.sobrenome))
        db.commit()
        return {"status": "ok"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="CNPJ ou E-mail já cadastrados")

@router.get("/perfil/{parceiro_id}")
def obter_perfil_parceiro(parceiro_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, cnpj, razao_social, nome_fantasia, email, cidade, estado, nome, sobrenome 
        FROM parceiros WHERE id = ?
    """, (parceiro_id,))
    parceiro = cursor.fetchone()
    if not parceiro:
        raise HTTPException(status_code=404, detail="Parceiro não encontrado")
    return dict(parceiro)

@router.post("/perfil/{parceiro_id}")
def atualizar_perfil_parceiro(parceiro_id: int, dados: AtualizarPerfilSchema, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, senha FROM parceiros WHERE id = ?", (parceiro_id,))
    parceiro = cursor.fetchone()
    if not parceiro:
        raise HTTPException(status_code=404, detail="Parceiro não encontrado")

    if dados.senha_nova.strip():
        if not verificar_senha(dados.senha_antiga, parceiro["senha"]):
            raise HTTPException(status_code=400, detail="A senha atual informada está incorreta.")
        nova_hash = gerar_hash_senha(dados.senha_nova)
        cursor.execute("""
            UPDATE parceiros 
            SET razao_social=?, nome_fantasia=?, cidade=?, estado=?, nome=?, sobrenome=?, email=?, senha=?
            WHERE id=?
        """, (dados.razao_social, dados.nome_fantasia, dados.cidade, dados.estado, dados.nome, dados.sobrenome, dados.email, nova_hash, parceiro_id))
    else:
        cursor.execute("""
            UPDATE parceiros 
            SET razao_social=?, nome_fantasia=?, cidade=?, estado=?, nome=?, sobrenome=?, email=?
            WHERE id=?
        """, (dados.razao_social, dados.nome_fantasia, dados.cidade, dados.estado, dados.nome, dados.sobrenome, dados.email, parceiro_id))

    db.commit()
    return {"status": "ok", "mensagem": "Dados atualizados com sucesso."}

@router.get("/stats/{parceiro_id}")
def stats_parceiro(parceiro_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM roles WHERE parceiro_id = ? AND status = 'aprovado'", (parceiro_id,))
    publicados = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM roles WHERE parceiro_id = ? AND status = 'pendente'", (parceiro_id,))
    pendentes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COALESCE(SUM(likes), 0) FROM roles WHERE parceiro_id = ?", (parceiro_id,))
    likes = cursor.fetchone()[0]
    
    graficos = {
        "semanal": {"labels": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"], "dados": [1, 0, 2, 1, 4, 7, 3]},
        "mensal": {"labels": ["Semana 1", "Semana 2", "Semana 3", "Semana 4"], "dados": [5, 8, 4, publicados]},
        "semestral": {"labels": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"], "dados": [12, 15, 10, 22, 30, publicados]},
        "anual": {"labels": ["2023", "2024", "2025", "2026"], "dados": [10, 45, 80, publicados]}
    }

    return {
        "publicados": publicados,
        "pendentes": pendentes,
        "likes": likes,
        "graficos": graficos
    }

@router.get("/eventos/{parceiro_id}")
def listar_eventos_parceiro(parceiro_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, title, category, status, data_evento, image FROM roles WHERE parceiro_id = ? ORDER BY id DESC", (parceiro_id,))
    roles = cursor.fetchall()
    return [dict(r) for r in roles]

@router.get("/lista")
def lista_parceiros(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, nome_fantasia as nome, cnpj, cidade, estado, email FROM parceiros ORDER BY id DESC")
    parceiros = cursor.fetchall()
    return [
        {
            "id": p["id"],
            "nome": p["nome"],
            "cnpj": p["cnpj"],
            "cidade": p["cidade"],
            "estado": p["estado"],
            "email": p["email"],
            "senha": "Oculta por segurança"
        } for p in parceiros
    ]