from fastapi import FastAPI
from dotenv import load_dotenv
import os
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

# 1. Carrega as variáveis de ambiente primeiro
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1500))

print(f"SECRET_KEY carregada: {SECRET_KEY}")
print(f"ALGORITHM carregada: {ALGORITHM}")

# 2. Cria o App e configura o CORS
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login_form")

# 3. Define as funções de segurança ANTES das rotas
def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

def verificar_senha(senha_plana: str, senha_hashed: str) -> bool:
    return bcrypt.checkpw(senha_plana.encode('utf-8'), senha_hashed.encode('utf-8'))

# 4. IMPORTA AS ROTAS NO FINAL
from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

from fastapi import WebSocket, WebSocketDisconnect

# Gerenciador de conexões em tempo real para a Cozinha (KDS)
clientes_cozinha = []

@app.websocket("/ws/cozinha")
async def websocket_cozinha(websocket: WebSocket):
    await websocket.accept()
    clientes_cozinha.append(websocket)
    try:
        while True:
            # Mantém a conexão aberta esperando mensagens
            data = await websocket.receive_text()
            # Quando um pedido novo chegar, avisa todas as telas da cozinha
            for cliente in clientes_cozinha:
                await cliente.send_text(f"Atualização na cozinha: {data}")
    except WebSocketDisconnect:
        clientes_cozinha.remove(websocket)
# foi criado um WebSocket para a cozinha (KDS) que permite que múltiplas telas na cozinha recebam 
# atualizações em tempo real sobre novos pedidos ou mudanças de status. 
# Quando um pedido é atualizado, todos os clientes conectados recebem uma mensagem com a atualização.      
# pelo motivo de erros do windows exigir um banco de dados mais dedicado, fica como sugestao 
# a utilização do MySQL ou PostgreSQL para produção, mas o SQLite é suficiente para testes e desenvolvimento local.  



# para rodar comando: uvicorn main:app --reload

# endpoint: http://localhost:8000 utilizado o endereço http://127.0.0.1:8000/docs do meu navegador.

# /ordens é o (path) do endpoint endereço local
# Rest API para gerenciar ordens de gestao de pedidos de uma loja de alimentos, com autenticação e autorização de usuários.
# Get -> leitura / pegar / rotas
# Post -> criar / adicionar / remover / listar

# utilizado o SQLite como banco de dados via SQLAlchemy, mas pode ser alterado para MySQL, PostgreSQL, etc.


#https://github.com/juniopedro/API-RAIZES-DO-NORDESTE.git
