from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

ws_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@ws_router.websocket("/ws/cozinha/{loja_id}")
async def websocket_endpoint(websocket: WebSocket, loja_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Aqui você pode processar mensagens vindas da cozinha
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
        
# foi criado um WebSocket para a cozinha (KDS) que permite que múltiplas telas na cozinha recebam 
# atualizações em tempo real sobre novos pedidos ou mudanças de status. 
# Quando um pedido é atualizado, todos os clientes conectados recebem uma mensagem com a atualização.      
# pelo motivo de erros do windows exigir um banco de dados mais dedicado, fica como sugestao 
# a utilização do MySQL ou PostgreSQL para produção, mas o SQLite é suficiente para testes e desenvolvimento local.
