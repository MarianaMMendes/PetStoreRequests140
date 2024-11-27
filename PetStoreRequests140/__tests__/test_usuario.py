# 1- bibliotecas
import pytest # engine /framwwork teste de unidade
import requests # framework de teste de API
import json # leitor e escritor de json


from utils.utils import ler_csv   # importar a função de leitura do csv 

# 2- classe (opcional) no phyton, em muitos casos

# 2.1 atributos ou variaveis
# consulta e resultado esperado
usuario_id = 8181877              
usuario_username = "alana"
usuario_firstName = "Mariana"          
usuario_lastName = "Mendes"    
usuario_email= "mari"     
usuario_password = "123456"               
usuario_phone = "33991558187"    
usuario_userstatus = 1

# informações em comum

url= 'https://petstore.swagger.io/v2/user'   #endereço 
headers= { 'Content-Type': 'application/json' } 

# 2.2 Funções e métodos

def test_post_usuario():
    #configura
    usuario=open('./fixtures/json/meuusuario1.json')
    data=json.loads(usuario.read())
    # dados de saída

    #executa
    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=5
    )

    #válida
    response_body = response.json()

    assert response.status_code == 200
    
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(usuario_id)
  

def test_get_usuario():
    #Configura

    #Executa 
    response = requests.get(
       url=f'{url}/{usuario_username}',
        headers=headers
    )

    response_body = response.json()

    assert response.status_code == 200

    assert response_body['username'] == usuario_username
    assert response_body['firstName'] == usuario_firstName
    assert response_body['lastName'] == usuario_lastName


def test_put_usuario():
    # Configura
    # Dados de entrada vem de um arquivo json
    usuario = open('./fixtures/json/meuusuario2.json')
    data = json.loads(usuario.read())
    # Dados de saída / resultado esperado vem dos atributos decritos antes da funções
    
    # Executa
    response = requests.put(
        url=f'{url}/{usuario_username}',
        headers=headers,
        data=json.dumps(data),
        timeout=5
    )

    # Válida
    response_body = response.json()

    assert response.status_code == 200

    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(usuario_id)
    
    
def test_delete_usuario():
    #Configura 
    
    #Executa
    response = requests.delete(
            url=f'{url}/{usuario_username}',
            headers=headers
        )

    response_body = response.json()

    assert response.status_code == 200
    
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == usuario_username
      

@pytest.mark.parametrize('id,username,firstName,lastName,email,password,phone,userStatus',
                         ler_csv('./fixtures/csv/usuario.csv'))
def test_post_usuario_dinamico(id,username,firstName,lastName,email,password,phone,userStatus):
    #configura

    usuario = {}
    usuario['id'] = int(id)
    usuario['username'] = username
    usuario['firstName'] = firstName
    usuario['lastName'] = lastName
    usuario['email'] = email
    usuario['password'] = password
    usuario['phone'] = phone
    usuario['userStatus'] = int(userStatus)

    usuario = json.dumps(obj=usuario, indent=4)
    print('\n' + usuario)

    #Executa
    response = requests.post(
        url=url,
        headers=headers,
        data=usuario,
        timeout=20
    )

    #Compara

    response_body = response.json()

    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(id)


@pytest.mark.parametrize('id,username,firstName,lastName,email,password,phone,userStatus',
                         ler_csv('./fixtures/csv/usuario.csv'))
def test_delete_usuario_dinamico(id,username,firstName,lastName,email,password,phone,userStatus):

    #Excecuta
    response = requests.delete(
        url=f'{url}/{username}',
        headers=headers
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == username