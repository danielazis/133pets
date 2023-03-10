import pytest  # motor / engine
import requests  # biblioteca para comunicar com APIs
import csv

base_url = 'https://petstore.swagger.io/v2'  # endereço da API
headers = {'Content-Type': 'application/json'}  # os dados serão no formato json


def ler_dados_csv():
    dados_csv = []  # criamos uma lista vazia
    nome_arquivo = '../../vendors/csv/pet_positivo.csv'
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


def testar_incluir_pet():
    # Configura
    # Dados de entrada virão do pet1.json
    # Resultado Esperado
    status_code_esperado = 200
    nome_pet_esperado = 'Shurato'
    tag_esperada = 'Vacinado'

    # Executa
    resultado_obtido = requests.post(url=base_url + '/pet',
                                     data=open('../../vendors/json/pet1.json', 'rb'),
                                     headers=headers
                                     )

    # Valida
    print(resultado_obtido)
    corpo_da_resposta = resultado_obtido.json()  # extrai o json da response
    print(corpo_da_resposta)
    assert resultado_obtido.status_code == status_code_esperado
    assert corpo_da_resposta['name'] == nome_pet_esperado
    assert corpo_da_resposta['tags'][0]['name'] == tag_esperada


def testar_consultar_pet():
    # 1 - Configura
    # 1.1 - Dados de Entrada
    pet_id = '1989'
    # 1.2 - Resultados esperados
    status_code_esperado = 200
    nome_pet_esperado = 'Shurato'
    tag_esperado = 'Vacinado'

    # Executa
    resultado_obtido = requests.get(url=base_url + '/pet/' + pet_id,
                                    headers=headers
                                    )
    # Valida
    print(resultado_obtido)
    corpo_da_resposta = resultado_obtido.json()
    print(corpo_da_resposta)
    assert resultado_obtido.status_code == status_code_esperado
    assert corpo_da_resposta['name'] == nome_pet_esperado
    assert corpo_da_resposta['tags'][0]['name'] == tag_esperado


def testar_alterar_pet():
    status_code_esperado = 200
    nome_pet_esperado = 'Shurato'
    status_esperado = 'solded'

    resultado_obtido = requests.put(url=base_url + '/pet',
                                    data=open('../../vendors/json/pet2.json', 'rb'),
                                    headers=headers)

    assert resultado_obtido.status_code == status_code_esperado
    corpo_da_resposta = resultado_obtido.json()
    assert corpo_da_resposta['name'] == nome_pet_esperado
    assert corpo_da_resposta['status'] == status_esperado


def testar_excluir_pet():
    pet_id = 1989
    status_code_esperado = 200
    code_esperado = 200
    type_esperado = 'unknown'
    message_esperada = str(pet_id)

    resultado_obtido = requests.delete(url=f'{base_url}/pet/{pet_id}',
                                       headers=headers
                                       )

    assert resultado_obtido.status_code == status_code_esperado
    corpo_da_resposta = resultado_obtido.json()
    print(corpo_da_resposta)
    assert corpo_da_resposta['code'] == code_esperado
    assert corpo_da_resposta['type'] == type_esperado
    assert corpo_da_resposta['message'] == message_esperada


@pytest.mark.parametrize('petid,category_id,category_name,name,tags_id,tags_name,status,status_code', ler_dados_csv())
def testar_incluir_pet_json_dinamico(petid, category_id, category_name, name, tags_id, tags_name, status, status_code):
    # 1 - Configura
    # 1.1 - Dados de Entrada
    # Utilizará o arquivo pets_positivo.csv

    # 1.2 - Resultados Esperados
    # Utilizará o arquivo pets_positivo.csv

    # 1.3 - Extra - Montar o json dinamicamente a partir do csv
    corpo_json = '{'
    corpo_json += f'  "id": {petid},'
    corpo_json += '  "category": {'
    corpo_json += f'    "id": {category_id},'
    corpo_json += f'    "name": "{category_name}"'
    corpo_json += '},'
    corpo_json += f'"name": "{name}",'
    corpo_json += '"photoUrls": ['
    corpo_json += '"string"'
    corpo_json += '],'
    corpo_json += '"tags": ['
    corpo_json += '{'
    corpo_json += f'    "id": {tags_id},'
    corpo_json += f'    "name": "{tags_name}"'
    corpo_json += '}'
    corpo_json += '],'
    corpo_json += f'"status": "{status}"'
    corpo_json += '}'

    print(corpo_json)
    # 2 - Executa
    resultado_obtido = requests.post(
        url=base_url+'/pet',
        data=corpo_json,
        headers=headers
    )

    # 3 - Valida
    assert resultado_obtido.status_code == int(status_code)
    corpo_da_resposta = resultado_obtido.json()
    assert corpo_da_resposta['id'] == int(petid)
    assert corpo_da_resposta['category']['id'] == int(category_id)
    assert corpo_da_resposta['category']['name'] == category_name
    assert corpo_da_resposta['name'] == name
    assert corpo_da_resposta['tags'][0]['id'] == int(tags_id)
    assert corpo_da_resposta['tags'][0]['name'] == tags_name
    assert corpo_da_resposta['status'] == status
