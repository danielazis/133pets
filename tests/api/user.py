import pytest

import requests

base_url = 'https://petstore.swagger.io/v2'
headers = {'Content-Type': 'application/json'}

user1 = {
  "id": 23061989,
  "username": "Petlover",
  "firstName": "Anna",
  "lastName": "Levi",
  "email": "anna777@petlover.com",
  "password": "123456",
  "phone": "4567841",
  "userStatus": 1
}


# POST
def testar_criar_usuario():
    status_code_esperado = 200
    code_esperado = 200
    type_esperado = "unknown"
    message_esperado = "23061989"

    resultado_obtido = requests.post(url=base_url+'/user',
                                     json=user1,
                                     )

    assert resultado_obtido.status_code == status_code_esperado
    corpo_da_resposta = resultado_obtido.json()
    assert corpo_da_resposta['code'] == code_esperado
    assert corpo_da_resposta['type'] == type_esperado
    assert corpo_da_resposta['message'] == message_esperado


def testar_criar_usuario_com_lista():
    status_code_esperado = 200
    code_esperado = 200
    type_esperado = "unknown"
    message_esperado = "ok"

    resultado_obtido = requests.post(url=base_url+'/user/createWithList',
                                     data=open('../../vendors/json/userlist.json', 'rb'),
                                     headers=headers
                                     )
    assert resultado_obtido.status_code == status_code_esperado
    corpo_da_resposta = resultado_obtido.json()
    assert corpo_da_resposta['code'] == code_esperado
    assert corpo_da_resposta['type'] == type_esperado
    assert corpo_da_resposta['message'] == message_esperado


# GET
def testar_consultar_usuario():
    username = "Petlover"
    user_id_esperado = 23061989
    email_esperado = "anna777@petlover.com"
    status_code_esperado = 200

    resultado_obtido = requests.get(url=base_url+'/user/'+username)

    assert resultado_obtido.status_code == status_code_esperado
    corpo_da_resposta = resultado_obtido.json()
    assert corpo_da_resposta['username'] == username
    assert corpo_da_resposta['id'] == user_id_esperado
    assert corpo_da_resposta['email'] == email_esperado


# PUT
def testar_atualizar_usuario():
    username = "Petlover"
    status_code_esperado = 200
    code_esperado = 200
    type_esperado = "unknown"

    resultado_obtido = requests.put(url=base_url + '/user/' + username,
                                    data=open('../../vendors/json/user2.json', 'rb'),
                                    headers=headers
                                    )

    assert resultado_obtido.status_code == status_code_esperado
    corpo_da_resposta = resultado_obtido.json()
    assert corpo_da_resposta['code'] == code_esperado
    assert corpo_da_resposta['type'] == type_esperado


# DELETE
def testar_excluir_usuario():
    username = "Petlover"
    status_code_esperado = 200
    code_esperado = 200
    type_esperado = "unknown"

    resultado_obtido = requests.delete(url=base_url + '/user/' + username)

    assert resultado_obtido.status_code == status_code_esperado
    corpo_da_resposta = resultado_obtido.json()
    assert corpo_da_resposta['code'] == code_esperado
    assert corpo_da_resposta['type'] == type_esperado
    assert corpo_da_resposta['message'] == username
