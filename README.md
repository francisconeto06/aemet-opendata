# 🌞 AEMET-OPENDATA

Projeto desenvolvido para **automatizar o download, organização e processamento de dados de radiação solar e insolação** das estações radiométricas operadas pela **Agência Estatal de Meteorologia da Espanha (AEMET)**, utilizando o serviço **OpenData** oficial.

---

## 📌 Funcionalidades

O projeto permite a obtenção automatizada das seguintes variáveis meteorológicas:

* **Radiação Global (GL)** — em `10 × kJ/m²`
* **Radiação Difusa (DF)** — em `10 × kJ/m²`
* **Radiação Direta (DT)** — em `10 × kJ/m²`
* **Insolação (Sol)** — em horas

Os dados podem ser obtidos tanto em **tempo quase real** quanto em **séries históricas consolidadas**.

---

## 📁 Estrutura do Projeto

```text
aemet-opendata/
├── aemet_insolation_history.py     # Download do histórico diário de insolação para todas as estações
├── aemet_insolation_pipeline.py    # Pipeline de organização dos dados de insolação diária (horas)
├── aemet_real_time_radiation.py    # Download diário (D-1) de radiação Global, Direta e Difusa via API
├── aemet_inventory_stations.py     # Geração do inventário completo de estações disponíveis na API
├── utils.py                        # Funções auxiliares e listas utilitárias
├── todas_estacoes.csv              # Inventário de todas as estações disponíveis via API
├── aemet_metadata_real_time.csv    # Inventário das estações com dados de radiação em tempo real
└── README.md                       # Documentação do projeto
```

---

## ⚙️ Instalação

### Pré-requisitos

* **Anaconda / Miniconda** (testado com `conda 25.5.1`)
* **Python 3.13.5**

### Clonando o repositório

```bash
git clone https://github.com/francisconeto06/aemet-opendata.git
cd aemet-opendata
```

### Criação do ambiente Conda

```bash
conda create -n aemet-opendata python=3.13.5 pandas tqdm requests
conda activate aemet-opendata
```

> 💡 As demais bibliotecas utilizadas fazem parte da biblioteca padrão do Python.

---

## 📦 Bibliotecas Utilizadas

Além das dependências instaladas via conda, os scripts utilizam:

* `datetime`
* `argparse`
* `requests`
* `pandas`
* `time`
* `json`
* `sys`
* `os`

---

## 🔑 Configuração da Chave de Acesso (API Key)

Antes de executar qualquer script, é necessário criar uma **chave de acesso pessoal** para a API da AEMET.

### Passo 1: Gerar a chave

Acesse o portal oficial da AEMET OpenData:

👉 [https://opendata.aemet.es/centrodedescargas/inicio](https://opendata.aemet.es/centrodedescargas/inicio)

Siga as instruções do site para gerar sua chave.

### Passo 2: Criar o arquivo `key.txt`

Na pasta raiz do projeto (`aemet-opendata/`), crie um arquivo chamado `key.txt` com o seguinte conteúdo:

```python
key = "SUA_CHAVE_AQUI"
```

⚠️ **Importante:**

* A chave deve estar **entre aspas**
* O arquivo `key.txt` deve estar **no mesmo diretório dos scripts**

---

## 🗺️ Inventário de Estações

O projeto utiliza o arquivo `todas_estacoes.csv`, que contém o inventário completo das estações disponíveis na API da AEMET.

### Gerando o inventário

Caso o arquivo não exista, basta executar:

```bash
python aemet_inventory_stations.py
```

O script irá consultar a API da AEMET e gerar automaticamente o arquivo `todas_estacoes.csv` com as seguintes colunas:

* `provincia`
* `latitud`
* `longitud`
* `altitud`
* `indicativo`
* `nombre`
* `indsinop`

---

## ▶️ Uso dos Scripts

### 1️⃣ Inventário de Estações

```bash
python aemet_inventory_stations.py
```

Baixa e atualiza o inventário completo de estações meteorológicas da AEMET.

---

### 2️⃣ Histórico Diário de Insolação

Script: `aemet_insolation_history.py`

Realiza o download do **histórico diário de insolação** para todas as estações disponíveis.

#### Argumentos disponíveis

* `--ano` → Ano desejado (padrão: `2024`)
* `--datai` → Data inicial (`YYYY-MM-DD`)
* `--dataf` → Data final (`YYYY-MM-DD`)
* `--janela` → Número de dias por requisição (padrão: `14`)

> ℹ️ A limitação de janela existe devido às restrições da API da AEMET.

#### Exemplos de uso

```bash
# Ano completo (padrão)
python aemet_insolation_history.py

# Ano específico
python aemet_insolation_history.py --ano 2023

# Intervalo de datas
python aemet_insolation_history.py --datai 2023-01-01 --dataf 2023-03-31

# Ajustando a janela de requisição
python aemet_insolation_history.py --ano 2025 --janela 7
```

📂 **Saída padrão:**

Os arquivos são salvos em:

```text
dataset_daily/insolacao_diaria_ANO.csv
```

Caso a pasta `dataset_daily` não exista, ela será criada automaticamente.

---

### 3️⃣ Pipeline de Organização da Insolação

Script: `aemet_insolation_pipeline.py`

Processa os arquivos consolidados de insolação diária presentes na pasta `dataset_daily`:

* Lê os CSVs anuais
* Separa os dados por estação
* Salva arquivos individuais organizados por **ano** e **estação**

#### Execução

```bash
python aemet_insolation_pipeline.py
```

⚠️ **Pré-requisito:**

* A pasta `dataset_daily` deve conter os arquivos gerados pelo script `aemet_insolation_history.py`

---

## 📚 Referências

* Serviço OpenData da AEMET: 👉 [https://opendata.aemet.es](https://opendata.aemet.es)

---

## 🤝 Contribuições

Sugestões, correções e melhorias são bem-vindas!

Sinta-se à vontade para abrir uma **issue** ou enviar um **pull request**.

---

## 📄 Licença

Este projeto é distribuído para fins acadêmicos e científicos. Consulte os termos de uso do **OpenData AEMET** para restrições adicionais sobre redistribuição dos dados.
