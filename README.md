# 🌵 API Raízes do Nordeste - Back-end

Este repositório contém a API RESTful desenvolvida como parte do Projeto Multidisciplinar para o estudo de caso da rede de franquias "Raízes do Nordeste". 

O sistema foi construído utilizando **Python** e o framework assíncrono **FastAPI**, com foco em alta disponibilidade, arquitetura multi-lojas (multi-tenant) e adequação à LGPD.

## 🚀 Tecnologias Utilizadas
* **Framework:** FastAPI
* **Linguagem:** Python 3.x
* **Banco de Dados:** SQLite (via SQLAlchemy ORM)
* **Segurança:** JWT (JSON Web Tokens) e Bcrypt (Hash de senhas)
* **Validação de Dados:** Pydantic

## ⚙️ Funcionalidades Implementadas
* **Autenticação e Autorização:** Login com geração de token JWT e controle de rotas protegidas.
* **Gestão Multi-lojas:** Separação lógica de usuários e pedidos por unidade da franquia.
* **Gestão de Pedidos:** Criação, adição/remoção de itens, cálculo automático de valores e atualização de status.
* **Conformidade Legal:** Registro de aceite da LGPD no cadastro de usuários.
* **Múltiplos Canais:** API configurada com CORS liberado para consumo via Site, Totem ou Mobile.

---

## 🛠️ Como rodar o projeto localmente

Siga os passos abaixo para executar a API na sua máquina:

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2. Crie e ative o ambiente virtual
**No Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```
**No Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes chaves de segurança:
```env
SECRET_KEY=sua_chave_secreta_aqui_exemplo_ihYqYDuXlxARN044qzpT7vC9EQxmdKBa
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1500
```

### 5. Execute o Servidor
```bash
uvicorn main:app --reload
```

---

## 📖 Documentação Interativa (Swagger)
Com o servidor rodando, acesse o navegador para testar as rotas diretamente pela interface interativa gerada automaticamente pelo FastAPI:

👉 **Acesse:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Lá você poderá criar um usuário, fazer o login para obter o token (botão *Authorize*) e testar todo o fluxo de criação e finalização de pedidos.