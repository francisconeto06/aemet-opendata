# -*- coding: utf-8 -*-
# Bibliotecas necessárias

import argparse
import os
import time
from datetime import datetime, timedelta

import pandas as pd
import requests

from utils import gms_to_decimal

# =========================================================
# Criando a pasta dataset_daily
# =========================================================

# cria pasta se não existir
os.makedirs("dataset_daily", exist_ok=True)


# =========================================================
# FUNÇÃO: BAIXAR UM PERÍODO
# =========================================================
def baixar_periodo(datai, dataf, api_key, tentativas=5):
    url = (
        f"https://opendata.aemet.es/opendata/api/valores/climatologicos/"
        f"diarios/datos/fechaini/{datai}T00%3A00%3A00UTC/fechafin/"
        f"{dataf}T00%3A00%3A00UTC/todasestaciones"
    )

    headers = {"cache-control": "no-cache"}
    querystring = {"api_key": api_key}

    for tentativa in range(1, tentativas + 1):
        resp = requests.get(url, headers=headers, params=querystring)

        if resp.status_code == 200:
            controle = resp.json()
            if "datos" not in controle:
                print("⚠ API não retornou campo 'datos'. Pulando...")
                return None

            # segunda requisição
            try:
                dados = requests.get(controle["datos"]).json()
                return dados
            except Exception:
                print("Erro ao converter JSON dos dados reais.")
                return None

        else:
            print(f"""❌ Erro HTTP {resp.status_code} — tentativa
                {tentativa}/{tentativas}""")
            time.sleep(10)

    print("⚠ Máximo de tentativas atingido.")
    return None


# =========================================================
# FUNÇÃO: EXTRAIR CAMPOS FILTRADOS
# =========================================================
def extrair_filtrados(lista):
    filtrados = []
    for item in lista:
        if "sol" in item:
            filtrados.append({
                "cod": item.get("indicativo"),
                "provincia": item.get("provincia"),
                "nome": item.get("nombre"),
                "alt": item.get("altitud"),
                "data": item.get("fecha"),
                "insolacao": item.get("sol")
            })
    return filtrados


# =========================================================
# FUNÇÃO: MESCLAR LAT/LON
# =========================================================
def mesclar_lat_lon(df):
    estacoes = pd.read_csv("todas_estacoes.csv")
    df_final = df.merge(
        estacoes[["indicativo", "latitud", "longitud"]],
        left_on="cod",
        right_on="indicativo",
        how="left"
    ).drop(columns=["indicativo"])

    df_final.rename(columns={"latitud": "lat", "longitud": "lon"},
                    inplace=True)

    df_final["lat"] = df_final["lat"].apply(gms_to_decimal)
    df_final["lon"] = df_final["lon"].apply(gms_to_decimal)

    return df_final


# =========================================================
# FUNÇÃO: SALVAR APPEND NO MESMO ARQUIVO
# =========================================================
def salvar_incremental(df_final, output):

    try:
        df_old = pd.read_csv(output)
        df_concat = pd.concat([df_old, df_final], ignore_index=True)
        df_concat.drop_duplicates(subset=["cod", "data"], inplace=True)
    except FileNotFoundError:
        df_concat = df_final

    df_concat = df_concat.sort_values(by=["cod", "data"])
    df_concat.to_csv(output, index=False)


def carregar_api_key():
    with open("key.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("key ="):
                return line.split("=", 1)[1].strip().strip('"')
    raise RuntimeError("ERRO: não encontrei chave em key.txt")


def configurar_datas(args):
    data_atual = (
        datetime(args.ano, 1, 1)
        if args.datai is None
        else datetime.fromisoformat(args.datai)
    )

    data_limite = (
        datetime(args.ano, 12, 31)
        if args.dataf is None
        else datetime.fromisoformat(args.dataf)
    )

    return data_atual, data_limite


def imprimir_cabecalho(args, data_atual, data_limite):
    print("=========================================")
    print(f" Baixando dados do ano {args.ano}")
    print(f" Período: {data_atual.date()} → {data_limite.date()}")
    print(f" Janela: {args.janela} dias")
    print("=========================================\n")


def processar_janela(data_atual, data_limite, args, api_key):
    datai = data_atual.strftime("%Y-%m-%d")

    dataf_raw = data_atual + timedelta(days=args.janela - 1)
    dataf = min(dataf_raw, data_limite).strftime("%Y-%m-%d")

    print(f"\n➡ Baixando período {datai} → {dataf}")

    dados = baixar_periodo(datai, dataf, api_key)

    if dados is None:
        print(f"⚠ Falha no período {datai} → {dataf}. Pulando...")
        return data_atual + timedelta(days=args.janela)

    filtrados = extrair_filtrados(dados)

    if not filtrados:
        print(f"⚠ Nenhum dado no período {datai} → {dataf}")
        return data_atual + timedelta(days=args.janela)

    df = pd.DataFrame(filtrados)
    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values(by=["cod", "data"])

    df_final = mesclar_lat_lon(df)
    salvar_incremental(df_final, args.saida)

    return data_atual + timedelta(days=args.janela)


def main():
    parser = argparse.ArgumentParser(description="Insolacao diária AEMET")

    parser.add_argument("--ano", type=int, default=2024,
                        help="Ano a processar (default: 2024)")
    parser.add_argument("--datai", type=str, default=None,
                        help="Data inicial no formato YYYY-MM-DD")
    parser.add_argument("--dataf", type=str, default=None,
                        help="Data final no formato YYYY-MM-DD")
    parser.add_argument("--janela", type=int, default=14,
                        help="Tamanho da janela de dias (default: 14)")

    parser.add_argument(
        "--saida",
        type=str,
        default=None,
        help="""Arquivo de saída
        (default: dataset_daily/insolacao_diaria_ANO.csv)"""
    )

    args = parser.parse_args()

    if args.saida is None:
        args.saida = f"dataset_daily/insolacao_diaria_{args.ano}.csv"

    api_key = carregar_api_key()
    data_atual, data_limite = configurar_datas(args)

    imprimir_cabecalho(args, data_atual, data_limite)

    while data_atual <= data_limite:
        data_atual = processar_janela(
            data_atual, data_limite, args, api_key
        )

    print("\n✔ FINALIZADO!")
    print(f"Arquivo salvo em: {args.saida}")


if __name__ == "__main__":
    main()
