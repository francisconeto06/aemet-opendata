# Bibliotecas

import pandas as pd
import requests

# url
url = (
    "https://opendata.aemet.es/opendata/api/valores/"
    "climatologicos/inventarioestaciones/todasestaciones/"
)

print(url)
# Lendo a key do arquivo
api_key = None

with open("key.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("key ="):
            _, valor = line.split("=", 1)
            api_key = valor.strip().strip('"')

# Verificação
if api_key is None:
    print("ERRO: Não encontrei a chave no arquivo key.txt")
    exit()

# Cabeçalhos corretos
headers = {
    "cache-control": "no-cache"
}

querystring = {"api_key": api_key}

# Requisição
response = requests.request("GET", url, headers=headers, params=querystring)

# Retorno
if response.status_code != 200:
    print(f"Erro na requisição: {response.status_code}")
else:
    print("Resposta recebida:")
    print(response.text)

controle = response.json()

# Pegando a URL dos dados reais
url_dados = controle["datos"]

# Segunda requisição: baixando os dados reais
response_dados = requests.get(url_dados)
lista_estacoes = response_dados.json()

# Criando DataFrame
df = pd.DataFrame(lista_estacoes, columns=[
    "provincia", "latitud", "longitud", "altitud",
    "indicativo", "nombre", "indsinop"
])

df.to_csv('todas_estacoes.csv', index=False, encoding="utf-8")

print("Arquivo salvo: estacoes_aemet.csv")
