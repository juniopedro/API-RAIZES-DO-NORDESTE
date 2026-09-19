import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzg5NTIwMzg4fQ.w0hiyzbzSnKjGnme7g6sVT7jS5XvhDnX3C_neRd836A"
    #token de autenticacao
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json)




