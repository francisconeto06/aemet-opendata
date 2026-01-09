# # -*- coding: utf-8 -*-
# """
# Docstring for aemet_insolação_pipeline

# Pipeline para processar os arquivos consolidados de insolação diária da AEMET.
# Lê os arquivos CSV na pasta 'dataset_daily', separa os dados por estação,
# e salva arquivos individuais para cada estação em subpastas organizadas por ano.

# Requer a pasta 'dataset_daily' com os arquivos CSV baixados previamente pelo
# script 'aemet_insolation_history.py'.

# Exemplo de uso:
# python aemet_insolação_pipeline.py
# """
# # Biliotecas necessárias

# import os

# import pandas as pd
# from tqdm import tqdm

# # Pasta onde estão os arquivos consolidados (originais)
# base_input_dir = "dataset_daily"

# # Lista todos os arquivos .csv da pasta
# arquivos = [f for f in os.listdir(base_input_dir) if f.endswith(".csv")]

# print("📂 Arquivos encontrados:")
# for a in arquivos:
#     print("  -", a)

# print("\n🚀 Iniciando processamento...\n")

# # Barra de progresso externa (por arquivo consolidado)
# for arquivo in tqdm(arquivos, desc="Processando arquivos consolidados",
#                     unit="arquivo"):

#     path_arquivo = os.path.join(base_input_dir, arquivo)

#     # Lê o CSV
#     df = pd.read_csv(path_arquivo)

#     # Garantir coluna data como datetime
#     df["data"] = pd.to_datetime(df["data"], format="ISO8601", errors="coerce")

#     # Identificar ano automaticamente
#     ano = df["data"].dt.year.unique()[0]

#     # Criar pasta dataset_daily/<ano>/
#     output_dir = os.path.join(base_input_dir, str(ano))
#     os.makedirs(output_dir, exist_ok=True)

#     # Barra de progresso interna (por estação)
#     grouped = df.groupby("cod")

#     for od, df_est in tqdm(grouped, desc=f" - Estações ({arquivo})",
#                            leave=False, unit="est"):

#         nome_estacao = df_est["nome"].iloc[0]

#         # Montar nome do arquivo final
#         filename = f"{od}_{nome_estacao}_{ano}_diario.csv"
#         filename = filename.replace(" ", "_").replace("/", "-")
#         path_out = os.path.join(output_dir, filename)

#         # Se já existir → atualizar
#         if os.path.exists(path_out):
#             df_old = pd.read_csv(path_out)
#             df_old["data"] = pd.to_datetime(df_old["data"])

#             # Combinar e remover duplicados
#             df_final = pd.concat([df_old, df_est], ignore_index=True)
#             df_final = df_final.drop_duplicates(subset=["data"], keep="last")

#         else:
#             df_final = df_est.copy()

#         # 🔥 GARANTIR ORDEM CRONOLÓGICA
#         df_final = df_final.sort_values("data").reset_index(drop=True)

#         # Salvar arquivo final
#         df_final.to_csv(path_out, index=False, encoding="utf-8")

#     # Após processar, excluir o arquivo consolidado
#     os.remove(path_arquivo)

# print("\n✅ PROCESSO FINALIZADO COM SUCESSO!")
# -*- coding: utf-8 -*-
"""
Pipeline para processar os arquivos consolidados de insolação diária da AEMET.

- Lê arquivos CSV da pasta 'dataset_daily'
- Identifica automaticamente se o arquivo é por ANO ou por PERÍODO
- Separa os dados por estação
- Salva arquivos individuais organizados em subpastas apropriadas

Estrutura de saída:
- dataset_daily/<ano>/
- dataset_daily/periodos/<datai_dataf>/
"""

import os
import re

import pandas as pd
from tqdm import tqdm


# =========================================================
# CONFIGURAÇÕES
# =========================================================

BASE_INPUT_DIR = "dataset_daily"


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def identificar_tipo_arquivo(nome_arquivo):
    """
    Identifica se o arquivo consolidado é por ano ou por período.

    Retorna:
        ("ano", "2024")
        ("periodo", "2026-01-01_2026-01-07")
        ("desconhecido", None)
    """
    padrao_periodo = (
        r"insolacao_diaria_"
        r"(\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2})\.csv"
    )
    padrao_ano = r"insolacao_diaria_(\d{4})\.csv"

    match_periodo = re.match(padrao_periodo, nome_arquivo)
    if match_periodo:
        return "periodo", match_periodo.group(1)

    match_ano = re.match(padrao_ano, nome_arquivo)
    if match_ano:
        return "ano", match_ano.group(1)

    return "desconhecido", None


# =========================================================
# PIPELINE PRINCIPAL
# =========================================================

def main():
    # Listar arquivos CSV
    arquivos = [
        f for f in os.listdir(BASE_INPUT_DIR)
        if f.endswith(".csv")
    ]

    if not arquivos:
        print("⚠ Nenhum arquivo CSV encontrado.")
        return

    print("📂 Arquivos encontrados:")
    for arquivo in arquivos:
        print(f"  - {arquivo}")

    print("\n🚀 Iniciando processamento...\n")

    # Barra de progresso externa (por arquivo consolidado)
    for arquivo in tqdm(
        arquivos,
        desc="Processando arquivos consolidados",
        unit="arquivo"
    ):
        path_arquivo = os.path.join(BASE_INPUT_DIR, arquivo)

        tipo, identificador = identificar_tipo_arquivo(arquivo)

        if tipo == "ano":
            ano = identificador
            output_dir = os.path.join(BASE_INPUT_DIR, ano)
            sufixo = ano

        elif tipo == "periodo":
            periodo = identificador
            output_dir = os.path.join(
                BASE_INPUT_DIR,
                "periodos",
                periodo
            )
            sufixo = periodo

        else:
            print(
                f"⚠ Arquivo ignorado (padrão desconhecido): {arquivo}"
            )
            continue

        os.makedirs(output_dir, exist_ok=True)

        # Ler CSV consolidado
        df = pd.read_csv(path_arquivo)

        # Garantir coluna data como datetime
        df["data"] = pd.to_datetime(
            df["data"],
            format="ISO8601",
            errors="coerce"
        )

        # Agrupar por estação
        grouped = df.groupby("cod")

        # Barra de progresso interna (por estação)
        for cod, df_est in tqdm(
            grouped,
            desc=f" - Estações ({arquivo})",
            leave=False,
            unit="est"
        ):
            nome_estacao = df_est["nome"].iloc[0]

            filename = f"{cod}_{nome_estacao}_{sufixo}_diario.csv"
            filename = (
                filename
                .replace(" ", "_")
                .replace("/", "-")
            )

            path_out = os.path.join(output_dir, filename)

            # Se já existir → atualizar incrementalmente
            if os.path.exists(path_out):
                df_old = pd.read_csv(path_out)
                df_old["data"] = pd.to_datetime(df_old["data"])

                df_final = pd.concat(
                    [df_old, df_est],
                    ignore_index=True
                ).drop_duplicates(
                    subset=["data"],
                    keep="last"
                )
            else:
                df_final = df_est.copy()

            # Garantir ordem cronológica
            df_final = (
                df_final
                .sort_values("data")
                .reset_index(drop=True)
            )

            # Salvar arquivo final
            df_final.to_csv(
                path_out,
                index=False,
                encoding="utf-8"
            )

        # Remover arquivo consolidado após processamento
        os.remove(path_arquivo)

    print("\n✅ PROCESSO FINALIZADO COM SUCESSO!")


if __name__ == "__main__":
    main()
