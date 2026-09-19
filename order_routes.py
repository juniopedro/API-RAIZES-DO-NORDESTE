from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, ItemPedido

# rotas com acesso publico, para fins do trabalho academico, sem necessidade de autenticação, mas em produção, essas rotas devem ser protegidas com autenticação e autorização.
order_router = APIRouter(prefix="/pedidos", tags=["pedidos " "RU4933864 JUNIO PEDRO CST 202405 PROJETO BACK END"])

@order_router.get("/")
async def pedidos():
    """
    Rota padrão de pedidos. Agora com acesso público para avaliação.
    """
    return {"mensagem": "Voce acessou a rota de pedidos (Acesso Público)"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    session.refresh(novo_pedido)
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail ="Pedido nao encontrado")

    # 2. nao adiconado a trava que exige ser admin ou dono do pedido
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido numero: {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao)):
    pedidos = session.query(Pedido).all()
    return {
        "pedidos": pedidos
    }

@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail ="Pedido nao existe")

    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.produto, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }

@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, session: Session = Depends(pegar_sessao)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "item removido com sucesso",
        "preco_pedido": pedido.preco,
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail ="Pedido nao encontrado")

    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"pedido numero: {pedido.id} finalizado com sucesso",
        "pedido": pedido
    }
