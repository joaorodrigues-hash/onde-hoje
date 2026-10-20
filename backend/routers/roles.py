from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import sqlite3
from database import get_db

router = APIRouter(prefix="/roles", tags=["Rolês"])

class RoleSchema(BaseModel):
    title: str
    venue: str
    estado: str
    cidade: str
    price: str
    category: str
    image: str = ""
    tipo_imagem: str = "url"
    descricao: str = ""
    link_ingresso: str = ""
    observacao_interna: str = ""
    data_evento: Optional[str] = None
    parceiro_id: int = 0

@router.get("/explorar")
def explorar_roles(
    estado: Optional[str] = Query(None),
    cidade: Optional[str] = Query(None),
    categoria: Optional[str] = Query(None),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    query = """
        SELECT * FROM roles 
        WHERE status = 'aprovado' 
          AND (data_evento >= date('now') OR data_evento IS NULL OR data_evento = '')
    """
    params = []

    if estado and estado.strip():
        query += " AND UPPER(estado) = UPPER(?)"
        params.append(estado.strip())

    if cidade and cidade.strip():
        query += " AND LOWER(cidade) LIKE LOWER(?)"
        params.append(f"%{cidade.strip()}%")

    if categoria and categoria.strip():
        query += " AND category = ?"
        params.append(categoria.strip())

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    roles = cursor.fetchall()

    return [dict(r) for r in roles]

@router.get("/passados")
def listar_roles_passados(
    estado: Optional[str] = Query(None),
    cidade: Optional[str] = Query(None),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    query = """
        SELECT * FROM roles 
        WHERE status = 'aprovado' 
          AND data_evento < date('now') 
          AND data_evento IS NOT NULL 
          AND data_evento != ''
    """
    params = []

    if estado and estado.strip():
        query += " AND UPPER(estado) = UPPER(?)"
        params.append(estado.strip())

    if cidade and cidade.strip():
        query += " AND LOWER(cidade) LIKE LOWER(?)"
        params.append(f"%{cidade.strip()}%")

    query += " ORDER BY data_evento DESC"
    cursor.execute(query, params)
    roles = cursor.fetchall()

    return [dict(r) for r in roles]

@router.post("/sugerir")
def sugerir_role(role: RoleSchema, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    imagem_final = role.image
    if role.tipo_imagem == "sem_foto" or not imagem_final:
        imagem_final = "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800"

    cursor.execute("""
        INSERT INTO roles (
            title, venue, estado, cidade, price, category, image, tipo_imagem,
            descricao, link_ingresso, observacao_interna, data_evento, status, parceiro_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pendente', ?)
    """, (
        role.title, role.venue, role.estado, role.cidade, role.price, role.category,
        imagem_final, role.tipo_imagem, role.descricao, role.link_ingresso,
        role.observacao_interna, role.data_evento, role.parceiro_id
    ))
    db.commit()
    return {"status": "ok", "mensagem": "Sugestão enviada com sucesso para análise da moderação."}

@router.get("/pendentes")
def listar_pendentes(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM roles WHERE status = 'pendente' ORDER BY id DESC")
    roles = cursor.fetchall()
    return [dict(r) for r in roles]

@router.post("/aprovar/{id}")
def aprovar(id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE roles SET status = 'aprovado' WHERE id = ?", (id,))
    db.commit()
    return {"status": "aprovado"}

@router.post("/rejeitar/{id}")
def rejeitar(id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE roles SET status = 'rejeitado' WHERE id = ?", (id,))
    db.commit()
    return {"status": "rejeitado"}

@router.get("/gerenciar")
def gerenciar_roles(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM roles WHERE status IN ('aprovado', 'oculto') ORDER BY id DESC")
    roles = cursor.fetchall()
    return [dict(r) for r in roles]

@router.post("/status/{id}")
def alterar_status(id: int, dados: dict, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    novo_status = dados.get("status")
    if novo_status == "excluir":
        cursor.execute("DELETE FROM roles WHERE id = ?", (id,))
    else:
        cursor.execute("UPDATE roles SET status = ? WHERE id = ?", (novo_status, id))
    db.commit()
    return {"status": "ok"}