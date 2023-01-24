import pytest
import csv
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


def ler_dados_csv():
    dados_csv = []  # criamos uma lista vazia
    nome_arquivo = '../../vendors/csv/users.csv'
    try:
        with open(nome_arquivo, newline='') as arquivo_csv:
            campos = csv.reader(arquivo_csv, delimiter=',')
            next(campos)
            for linha in campos:
                dados_csv.append(linha)

        return dados_csv
    except FileNotFoundError:
        print(f'Arquivo não encontrado: {nome_arquivo}')
    except Exception as fail:
        print(f'Falha não prevista: {fail}')


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


# testes dinamicos POST/GET/DELETE

def montar_corpo_json(userid, username, fisrtName, lastName, email, password, phone, userStatus):
    # montando o json
    corpo_json = '{'
    corpo_json += f'    "id": {userid},'
    corpo_json += f'    "username": "{username}",'
    corpo_json += f'    "firstName": "{fisrtName}",'
    corpo_json += f'    "lastName": "{lastName}",'
    corpo_json += f'    "email": "{email}",'
    corpo_json += f'    "password": "{password}",'
    corpo_json += f'    "phone": "{phone}",'
    corpo_json += f'    "userStatus": {userStatus}'
    corpo_json += '}'
    return corpo_json


@pytest.mark.parametrize('userid,username,fisrtName,lastName,email,password,phone,userStatus', ler_dados_csv())
def testar_criar_usuario_json_dinamico(userid, username, fisrtName, lastName, email, password, phone, userStatus):
    # Configura
    status_code_esperado = 200
    code_esperado = 200
    type_esperado = "unknown"
    message_esperado = userid

    corpo_json = montar_corpo_json(userid, username, fisrtName, lastName, email, password, phone, userStatus)

    # Executa
    resultado_obtido = requests.post(url=base_url + '/user',
                                     headers=headers,
                                     data=corpo_json
                                     )

    # Valida
    assert resultado_obtido.status_code == status_code_esperado
    corpo_da_resposta = resultado_obtido.json()
    assert corpo_da_resposta['code'] == code_esperado
    assert corpo_da_resposta['type'] == type_esperado
    assert corpo_da_resposta['message'] == message_esperado


@pytest.mark.parametrize('userid,username,fisrtName,lastName,email,password,phone,userStatus', ler_dados_csv())
def testar_consultar_usuario_json_dinamico(userid, username, fisrtName, lastName, email, password, phone, userStatus):
    # Configura
    status_code_esperado = 200

    resultado_obtido = requests.get(url=base_url+'/user/'+username)

    assert resultado_obtido.status_code == status_code_esperado
    corpo_da_resposta = resultado_obtido.json()
    assert corpo_da_resposta['username'] == username
    assert corpo_da_resposta['id'] == int(userid)
    assert corpo_da_resposta['email'] == email
    assert corpo_da_resposta['password'] == password
    assert corpo_da_resposta['phone'] == phone
    assert corpo_da_resposta['userStatus'] == int(userStatus)

@pytest.mark.parametrize('userid,username,fisrtName,lastName,email,password,phone,userStatus', ler_dados_csv())
def testar_deletar_usuario_json_dinamico(userid, username, fisrtName, lastName, email, password, phone, userStatus):
    status_code_esperado = 200
    code_esperado = 200
    type_esperado = "unknown"

    resultado_obtido = requests.delete(url=base_url + '/user/' + username)

    assert resultado_obtido.status_code == status_code_esperado
    corpo_da_resposta = resultado_obtido.json()
    assert corpo_da_resposta['code'] == code_esperado
    assert corpo_da_resposta['type'] == type_esperado
    assert corpo_da_resposta['message'] == username