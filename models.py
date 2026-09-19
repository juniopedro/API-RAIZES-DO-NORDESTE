from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import declarative_base, relationship

# 1. Cria a conexao do seu banco de dados SQLite
db = create_engine("sqlite:///banco.db")

# 2. Cria a base do banco de dados
Base = declarative_base()

# 3. Tabelas do Banco de Dados
class Loja(Base):
    __tablename__ = "lojas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True)
    usuarios = relationship("Usuario", back_populates="loja")
    pedidos = relationship("Pedido", back_populates="loja")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    # Relacionamento com Loja
    loja_id = Column(Integer, ForeignKey("lojas.id"))
    loja = relationship("Loja", back_populates="usuarios")

    # Regras do Projeto (LGPD e Fidelidade)
    aceite_lgpd = Column(Boolean, default=False) 
    pontos_fidelidade = Column(Integer, default=0) 

    def __init__(self, nome: str, email: str, senha: str, ativo: bool = True, admin: bool = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="RECEBIDO") # RECEBIDO, EM_PREPARO, PRONTO, EM_ENTREGA, FINALIZADO    usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    preco = Column(Float, nullable=False, default=0.0)

    # Relacionamento com Loja
    loja_id = Column(Integer, ForeignKey("lojas.id"))
    loja = relationship("Loja", back_populates="pedidos")

    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, status="PENDENTE", usuario=None, preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido = Column("pedido",Integer, ForeignKey("pedidos.id"), nullable=False)
    produto = Column("produto",String, nullable=False)
    quantidade = Column("quantidade",Integer)
    preco_unitario = Column("preco_unitario",Float)
    tamanho = Column("tamanho",String, nullable=False)

    def __init__(self, quantidade=0, produto="", tamanho="", preco_unitario=0, pedido=None):
        self.quantidade = quantidade
        self.produto = produto
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

# 4. Cria as tabelas automaticamente no banco de dados ao iniciar
Base.metadata.create_all(bind=db)
