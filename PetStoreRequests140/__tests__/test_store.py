# 1- bibliotecas
import pytest 
import requests # framework de teste de API
import json # leitor e escritor de json


from utils.utils import ler_csv
# 2- classe (opcional) no phyton, em muitos casos

# 2.1 atributos ou variaveis
# consulta e resultado esperado
store_id = 8187
store_petId = 173218101
store_quantity = 1
store_shipDate = "2024-10-03T15:44:39.048Z"
store_status = "placed"
store_complete = "true"

url= 'https://petstore.swagger.io/v2/store/order'   #endereço 
headers= { 'Content-Type': 'application/json' }     

# 2.2 Funções / métodos

def test_post_store():
    # Configura
    # dados de entrada estão no arquivo json
    store=open('./fixtures/json/pedido1.json')   #fazer o arquivo json
    data=json.loads(store.read())
    #dados de saída / resultados esperado estão nos atributos acima das funções

    #excecuta
    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=5
     )
    
    #valida 
    response_body = response.json()

    assert response.status_code == 200

    assert response_body['id'] == int(store_id)
    assert response_body['petId'] == int(store_petId)
    assert response_body['status'] == store_status

def test_get_store():    
    #configura
    #dados de saída

    response = requests.get(
    url=f'{url}/{store_id}',
    headers=headers 
    )  
    
    #valida
    response_body = response.json()

    assert response.status_code == 200

    assert response_body['id'] == store_id
    assert response_body['petId'] == store_petId
    assert response_body['status'] == store_status

def test_delete_store():
    #configura

    #Excecuta
    response = requests.delete(
    url=f'{url}/{store_id}',
    headers=headers
    )
    
    response_body = response.json()
    assert response.status_code == 200

    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(store_id)

@pytest.mark.parametrize('id,petId,quantity,shipDate,status,complete',
                         ler_csv('./fixtures/csv/pedidos.csv'))
def test_post_store_dinamico(id,petId,quantity,shipDate,status,complete):
    #configura

    store = {}
    store['id'] = int(id)
    store['petID'] = int(petId)
    store['quantity'] = int(quantity)
    store['shipDate'] = shipDate
    store['status'] = status
    store['complete'] = complete

    store = json.dumps(obj=store, indent=4)
    print('\n' + store)

    #Excecuta
    response = requests.post(
        url=url,
        headers=headers,
        data=store,
        timeout=20
    )

    #Compara

    response_body = response.json()

    assert response.status_code == 200
    
    assert response_body['id'] == int(id)
    assert response_body['petId'] == int(petId)
    assert response_body['quantity'] == int(quantity)

    

@pytest.mark.parametrize('id,petId,quantity,shipDate,status,complete',
                         ler_csv('./fixtures/csv/pedidos.csv'))
def test_delete_store_dinamico(id,petId,quantity,shipDate,status,complete):

    #Excecuta
    response = requests.delete(
        url=f'{url}/{id}',
        headers=headers
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    
    assert response_body['code'] == 200  
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(id)