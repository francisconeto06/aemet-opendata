# -*- coding: utf-8 -*-
"""
Download e atualização diária de dados de radiação solar da AEMET.

Os dados são armazenados em arquivos CSV únicos por estação, no formato:
date, hora, GL, DF, DT

A cada execução:
- Se a data não existir no arquivo, ela é adicionada
- Se a data existir:
    - Valores existentes não são sobrescritos
    - Apenas colunas faltantes (NaN) são preenchidas
"""

# =========================================================
# Bibliotecas
# =========================================================
import os
import re
import time
from datetime import datetime

import pandas as pd
import requests

# =========================================================
# 1. Ler API KEY
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "key.txt")

api_key = None

with open(KEY_PATH, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line.startswith("key ="):
            _, value = line.split("=", 1)
            api_key = value.strip().strip('"')

if api_key is None:
    raise RuntimeError("❌ API key não encontrada em key.txt")


# =========================================================
# 2. Endpoint
# =========================================================
URL = "https://opendata.aemet.es/opendata/api/red/especial/radiacion"
HEADERS = {"cache-control": "no-cache"}
PARAMS = {"api_key": api_key}


# =========================================================
# 3. Requisição com retry
# =========================================================
def request_with_retries(max_attempts=3, wait_seconds=90):
    """Solicita a URL de dados com tentativas e espera."""
    attempts = 0

    while attempts < max_attempts:
        print("Solicitando acesso ao recurso...")
        response = requests.get(
            URL,
            headers=HEADERS,
            params=PARAMS,
            timeout=60,
        )

        if response.status_code == 200:
            payload = response.json()
            if "datos" in payload:
                return payload["datos"]

        attempts += 1
        print(
            f"Falha ({response.status_code}), "
            f"tentativa {attempts}/{max_attempts}"
        )

        if attempts < max_attempts:
            print(f"Aguardando {wait_seconds}s…")
            time.sleep(wait_seconds)

    raise RuntimeError("❌ Falha ao obter dados da AEMET")


# =========================================================
# 4. Normalização do nome da estação
# =========================================================
def normalizar_nome_estacao(nome):
    """
    Normaliza o nome da estação mantendo acentos,
    parênteses, vírgula e underscore.
    """
    nome = nome.replace(" ", "_")
    nome = re.sub(r"[^\w().,À-ÿ]", "", nome)
    return nome


# =========================================================
# 5. Exceções de nomes históricos
# =========================================================
ARQUIVOS_ESPECIAIS = {
    "Madrid_Ciudad_Universitaria": "Madrid,_Ciudad_Universitaria",
}


# =========================================================
# 6. Extrair bloco horário por tipo
# =========================================================
def extrair_bloco(cols, pos_tipo):
    """
    Extrai 16 valores horários (05–20) após o campo Tipo
    (GL, DF, DT).
    """
    valores = []
    idx = pos_tipo + 1

    for _ in range(16):
        if idx < len(cols) and cols[idx] != "":
            valores.append(cols[idx])
        else:
            valores.append(None)
        idx += 1

    return valores


# =========================================================
# 7. Obter dados
# =========================================================
url_dados = request_with_retries()
response = requests.get(url_dados, timeout=60)
raw_text = response.text

lines = [
    line.strip()
    for line in raw_text.split("\n")
    if line.strip()
]

data_bruta = lines[1].replace('"', "")
data_iso = datetime.strptime(
    data_bruta,
    "%d-%m-%y",
).strftime("%Y-%m-%d")

stations_lines = lines[3:]


# =========================================================
# 8. Pasta de saída
# =========================================================
OUTPUT_DIR = os.path.join(BASE_DIR, "real_time")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================================
# 9. Processamento por estação
# =========================================================
for line in stations_lines:
    cols = [col.strip('"') for col in line.split(";")]

    nome_estacao = cols[0]

    pos_tipos = [
        i for i, value in enumerate(cols)
        if value in {"GL", "DF", "DT"}
    ]

    if len(pos_tipos) < 3:
        print(f"⚠ Estação ignorada (dados incompletos): {nome_estacao}")
        continue

    pos_gl, pos_df, pos_dt = pos_tipos[:3]

    gl_horas = extrair_bloco(cols, pos_gl)
    df_horas = extrair_bloco(cols, pos_df)
    dt_horas = extrair_bloco(cols, pos_dt)

    df_novo = pd.DataFrame(
        {
            "date": data_iso,
            "hora": list(range(5, 21)),
            "GL": gl_horas,
            "DF": df_horas,
            "DT": dt_horas,
        }
    ).astype(
        {
            "hora": int,
            "GL": "float",
            "DF": "float",
            "DT": "float",
        }
    )

    nome_normalizado = normalizar_nome_estacao(nome_estacao)
    nome_normalizado = ARQUIVOS_ESPECIAIS.get(
        nome_normalizado,
        nome_normalizado,
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{nome_normalizado}_radiacion_completo.csv",
    )

    # =====================================================
    # 10. Atualização inteligente do CSV
    # =====================================================
    if os.path.exists(output_path):
        df_existente = pd.read_csv(
            output_path,
            dtype={"hora": int},
        )

        df_existente["date"] = df_existente["date"].astype(str)

        df_merged = pd.merge(
            df_existente,
            df_novo,
            on=["date", "hora"],
            how="outer",
            suffixes=("_old", ""),
        )

        for col in ["GL", "DF", "DT"]:
            df_merged[col] = df_merged[col].combine_first(
                df_merged[f"{col}_old"]
            )
            df_merged.drop(
                columns=f"{col}_old",
                inplace=True,
            )

        df_merged.sort_values(
            by=["date", "hora"],
            inplace=True,
        )

        df_merged.to_csv(
            output_path,
            index=False,
            encoding="utf-8",
        )

        print(f"🔄 Dados atualizados: {output_path}")

    else:
        df_novo.to_csv(
            output_path,
            index=False,
            encoding="utf-8",
        )

        print(f"✔ Arquivo criado: {output_path}")
