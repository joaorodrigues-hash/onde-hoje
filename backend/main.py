import os
import jwt
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, FileResponse
import uvicorn

from routers import categorias, roles, parceiros, admin, upload
from database import iniciar_banco

SECRET_KEY = "mercos_chave_mestra_secreta"

@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_banco()
    yield

app = FastAPI(title="Onde Hoje API", lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. MIDDLEWARE: Proteção JWT nas rotas administrativas
@app.middleware("http")
async def verificar_token_admin(request: Request, call_next):
    path = request.url.path
    rotas_protegidas = [
        "/admin/stats", "/admin/moderadores", "/admin/perfil",
        "/roles/aprovar", "/roles/rejeitar", "/roles/status", "/roles/pendentes"
    ]
    
    if any(path.startswith(r) for r in rotas_protegidas):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Acesso negado. Token não enviado."})
        
        token = auth.split("Bearer ")[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return JSONResponse(status_code=401, content={"detail": "Sessão inválida ou expirada."})
            
    return await call_next(request)

# 2. SWAGGER: Proteção HTTP Basic para os Avaliadores Mercos
security = HTTPBasic()

def verificar_acesso_docs(credentials: HTTPBasicCredentials = Depends(security)):
    usuarios_mercos = {
        "joao.rodrigues@mercos.com": "12345",
        "renan@mercos.com": "12345",
        "niler.barcelos@mercos.com": "12345"
    }
    if credentials.username in usuarios_mercos and credentials.password == usuarios_mercos[credentials.username]:
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas. O Swagger é restrito à equipe técnica.",
        headers={"WWW-Authenticate": "Basic"},
    )

@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(verificar_acesso_docs)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Documentação API - Mercos")

@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(verificar_acesso_docs)):
    return get_openapi(title="Onde Hoje API", version="1.0.0", routes=app.routes)

# 3. PASTAS ESTÁTICAS E ROTAS DA API
base_dir = os.path.dirname(os.path.abspath(__file__))
pasta_uploads = os.path.join(base_dir, "uploads")
os.makedirs(pasta_uploads, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=pasta_uploads), name="uploads")

app.include_router(categorias.router)
app.include_router(roles.router)
app.include_router(parceiros.router)
app.include_router(admin.router)
app.include_router(upload.router)

# 4. ROTA PRINCIPAL E FRONTEND ESTÁTICO
pasta_frontend = os.path.join(os.path.dirname(base_dir), "frontend")

@app.get("/", include_in_schema=False)
async def home():
    caminho_index = os.path.join(pasta_frontend, "index.html")
    if os.path.exists(caminho_index):
        return FileResponse(caminho_index)
    return {"status": "ok", "message": "Onde Hoje API rodando com sucesso!"}

if os.path.exists(pasta_frontend):
    app.mount("/", StaticFiles(directory=pasta_frontend, html=True), name="frontend")

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=porta, reload=False)