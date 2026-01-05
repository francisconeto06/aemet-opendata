# -*- coding: utf-8 -*-

# Biliotecas necessárias
import os

import pandas as pd
from tqdm import tqdm

# Pasta onde estão os arquivos consolidados (originais)
base_input_dir = "dataset_daily"

# Lista todos os arquivos .csv da pasta
arquivos = [f for f in os.listdir(base_input_dir) if f.endswith(".csv")]

print("📂 Arquivos encontrados:")
for a in arquivos:
    print("  -", a)

print("\n🚀 Iniciando processamento...\n")

# Barra de progresso externa (por arquivo consolidado)
for arquivo in tqdm(arquivos, desc="Processando arquivos consolidados",
                    unit="arquivo"):

    path_arquivo = os.path.join(base_input_dir, arquivo)

    # Lê o CSV
    df = pd.read_csv(path_arquivo)

    # Garantir coluna data como datetime
    df["data"] = pd.to_datetime(df["data"], format="ISO8601", errors="coerce")

    # Identificar ano automaticamente
    ano = df["data"].dt.year.unique()[0]

    # Criar pasta dataset_daily/<ano>/
    output_dir = os.path.join(base_input_dir, str(ano))
    os.makedirs(output_dir, exist_ok=True)

    # Barra de progresso interna (por estação)
    grouped = df.groupby("cod")

    for od, df_est in tqdm(grouped, desc=f" - Estações ({arquivo})",
                           leave=False, unit="est"):

        nome_estacao = df_est["nome"].iloc[0]

        # Montar nome do arquivo final
        filename = f"{od}_{nome_estacao}_{ano}_diario.csv"
        filename = filename.replace(" ", "_").replace("/", "-")
        path_out = os.path.join(output_dir, filename)

        # Se já existir → atualizar
        if os.path.exists(path_out):
            df_old = pd.read_csv(path_out)
            df_old["data"] = pd.to_datetime(df_old["data"])

            # Combinar e remover duplicados
            df_final = pd.concat([df_old, df_est], ignore_index=True)
            df_final = df_final.drop_duplicates(subset=["data"], keep="last")

        else:
            df_final = df_est.copy()

        # 🔥 GARANTIR ORDEM CRONOLÓGICA
        df_final = df_final.sort_values("data").reset_index(drop=True)

        # Salvar arquivo final
        df_final.to_csv(path_out, index=False, encoding="utf-8")

    # Após processar, excluir o arquivo consolidado
    os.remove(path_arquivo)

print("\n✅ PROCESSO FINALIZADO COM SUCESSO!")
