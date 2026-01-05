# Bibliotecas necessárias

import requests
import time
import os
import pandas as pd
from datetime import datetime
from utils import gms_to_decimal

# -------------------------------------------------------------
# 1. Ler API KEY
# -------------------------------------------------------------
api_key = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "key.txt")

with open(KEY_PATH, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("key ="):
            _, valor = line.split("=", 1)
            api_key = valor.strip().strip('"')

if api_key is None:
    print("ERRO: Não encontrei a chave no arquivo key.txt")
    exit()

# -------------------------------------------------------------
# 2. Endpoint
# -------------------------------------------------------------
url = "https://opendata.aemet.es/opendata/api/red/especial/radiacion"
headers = {"cache-control": "no-cache"}
querystring = {"api_key": api_key}


# -------------------------------------------------------------
# 3. Requisição com retry
# -------------------------------------------------------------
def request_with_retries():
    tentativas = 0
    max_tentativas = 3

    while tentativas < max_tentativas:
        print("Solicitando acesso ao recurso...")
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            controle = response.json()
            if "datos" in controle:
                return controle["datos"]

        tentativas += 1
        print(
            f"Falha ({response.status_code}), "
            f"tentativa {tentativas}/{max_tentativas}"
        )

        if tentativas < max_tentativas:
            print("Aguardando 90s…")
            time.sleep(90)

    print("❌ Falha após 3 tentativas.")
    return None


# -------------------------------------------------------------
# 4. Obter URL de dados
# -------------------------------------------------------------
url_dados = request_with_retries()
if url_dados is None:
    exit()

response_dados = requests.get(url_dados)
raw_text = response_dados.text

# -------------------------------------------------------------
# 5. Preparar linhas
# -------------------------------------------------------------
linhas = [line.strip() for line in raw_text.split("\n") if line.strip()]

data_bruta = linhas[1].replace('"', "")
data_fmt = datetime.strptime(data_bruta, "%d-%m-%y").strftime("%Y%m%d")

linhas_estacoes = linhas[3:]

# -------------------------------------------------------------
# 6. Carregar metadados
# -------------------------------------------------------------
df_meta = pd.read_csv(BASE_DIR + "/todas_estacoes.csv")
df_meta["lat_decimal"] = df_meta["latitud"].apply(gms_to_decimal)
df_meta["lon_decimal"] = df_meta["longitud"].apply(gms_to_decimal)
df_meta_idx = df_meta.set_index("indicativo", drop=False)

# -------------------------------------------------------------
# 7. Criar pasta de saída
# -------------------------------------------------------------
os.makedirs(BASE_DIR + "/real_time", exist_ok=True)


# -------------------------------------------------------------
# 8. Função para extrair bloco baseado no marcador "Tipo"
# -------------------------------------------------------------
def extrair_bloco(cols, pos_tipo):
    """
    A partir do índice do campo Tipo, extrai:
    - 16 valores horários (5–20)
    - SUMA
    Retorna (lista_horas, valor_suma, nova_posicao)
    """
    horas = []
    i = pos_tipo + 1

    # 16 valores horários
    for _ in range(16):
        if i < len(cols):
            horas.append(cols[i] if cols[i] != "" else None)
        else:
            horas.append(None)
        i += 1

    # SUMA
    suma = cols[i] if i < len(cols) else None
    i += 1

    return horas, suma, i


# -------------------------------------------------------------
# 9. Processar cada estação
# -------------------------------------------------------------
for linha in linhas_estacoes:
    cols = [c.strip('"') for c in linha.split(";")]

    nome = cols[0]
    indicativo = cols[1]

    # detecta posições dos marcadores "Tipo"
    pos_tipos = [i for i,
                 v in enumerate(cols) if v == "GL" or v == "DF" or v == "DT"]

    if len(pos_tipos) < 3:
        print(f"""⚠ Estação {nome} ({indicativo}) tem menos blocos que o
            esperado. Ignorada.""")
        continue

    pos_GL, pos_DF, pos_DT = pos_tipos[:3]

    # extrair blocos de forma segura
    GL_horas, GL_suma, _ = extrair_bloco(cols, pos_GL)
    DF_horas, DF_suma, _ = extrair_bloco(cols, pos_DF)
    DT_horas, DT_suma, _ = extrair_bloco(cols, pos_DT)

    # Garantir tamanho correto (evita erro do DataFrame)
    if not (len(GL_horas) == len(DF_horas) == len(DT_horas) == 16):
        print(f"""⚠ Tamanhos inconsistentes na estação {nome}.
            Ajustado automaticamente.""")
        GL_horas = (GL_horas + [None] * 16)[:16]
        DF_horas = (DF_horas + [None] * 16)[:16]
        DT_horas = (DT_horas + [None] * 16)[:16]

    # Criar DataFrame final
    df = pd.DataFrame({
        "hora": list(range(5, 21)),
        "GL": GL_horas,
        "DF": DF_horas,
        "DT": DT_horas
    })

    df = df.astype({
        "GL": "float",
        "DF": "float",
        "DT": "float"
    })

    # lat/lon
    if indicativo in df_meta_idx.index:
        lat = df_meta_idx.loc[indicativo, "lat_decimal"]
        lon = df_meta_idx.loc[indicativo, "lon_decimal"]
    else:
        lat = None
        lon = None

    df.insert(0, "indicativo", indicativo)
    df.insert(1, "nombre", nome)
    df.insert(2, "latitud", lat)
    df.insert(3, "longitud", lon)

    # salvar arquivo
    nome_limpo = nome.replace(" ", "_").replace("/", "_")
    nome_arquivo = f"{nome_limpo}_radiacion_{data_fmt}.csv"
    caminho = os.path.join(BASE_DIR + "/real_time", nome_arquivo)

    df.to_csv(caminho, index=False, encoding="utf-8")
    print(f"✔ Arquivo gerado: {caminho}")
