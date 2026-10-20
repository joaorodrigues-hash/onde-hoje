from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from database import get_db

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

@router.get("/")
def listar_categorias(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, nome FROM categorias ORDER BY nome")
    cats = [{"id": r["id"], "nome": r["nome"]} for r in cursor.fetchall()]
    return cats

@router.post("/add")
def adicionar_categoria(data: dict, db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (data["nome"],))
        db.commit()
        return {"status": "ok"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Categoria já existe.")

@router.post("/delete/{id}")
def deletar_categoria(id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM categorias WHERE id = ?", (id,))
    db.commit()
    return {"status": "ok"}