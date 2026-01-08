# AEMET-OPENDATA

Projeto para **automatizar o download, a organização e o processamento de dados de radiação solar e insolação** provenientes das estações radiométricas operadas pela **Agência Estatal de Meteorologia da Espanha (AEMET)**, utilizando o serviço oficial **OpenData API**.

---

## Visão Geral

O AEMET-OPENDATA fornece scripts reprodutíveis para coleta de dados meteorológicos em **tempo quase real** e **séries históricas consolidadas**, com foco em variáveis radiométricas e insolação. O projeto foi estruturado para facilitar a manutenção, a expansão e a integração em pipelines de análise científica.

---

## Funcionalidades

O projeto permite a obtenção automatizada das seguintes variáveis:

* **Radiação Global (GL)** — `10 × kJ/m²`
* **Radiação Difusa (DF)** — `10 × kJ/m²`
* **Radiação Direta (DT)** — `10 × kJ/m²`
* **Insolação (Sol)** — horas

Os dados podem ser coletados em:

* **Tempo quase real** (D-1)
* **Histórico diário** para períodos definidos

---

## Estrutura do Projeto

```text
aemet-opendata/
├── aemet_insolation_history.py     # Download do histórico diário de insolação para todas as estações
├── aemet_insolation_pipeline.py    # Pipeline de organização da insolação diária (horas)
├── aemet_real_time_radiation.py    # Download diário (D-1) de radiação Global, Direta e Difusa
├── aemet_inventory_stations.py     # Geração do inventário completo de estações disponíveis na API
├── utils.py                        # Funções auxiliares e listas utilitárias
├── todas_estacoes.csv              # Inventário de todas as estações disponíveis via API
├── aemet_metadata_real_time.csv    # Estações com dados de radiação em tempo real
└── README.md                       # Documentação do projeto
```

---

## Instalação

### Pré-requisitos

* **Anaconda ou Miniconda** (testado com `conda 25.5.1`)
* **Python 3.13.5**

### Clonagem do repositório

```bash
git clone https://github.com/francisconeto06/aemet-opendata.git
cd aemet-opendata
```

### Criação do ambiente Conda

```bash
conda create -n aemet-opendata python=3.13.5 pandas tqdm requests
conda activate aemet-opendata
```

Observação: as demais dependências utilizadas fazem parte da biblioteca padrão do Python.

---

## Dependências

Bibliotecas utilizadas pelos scripts:

* `argparse`
* `datetime`
* `json`
* `os`
* `pandas`
* `requests`
* `sys`
* `time`

---

## Configuração da Chave de Acesso (API Key)

Para utilizar a API da AEMET, é necessária uma chave de acesso pessoal.

### Geração da chave

Acesse o portal oficial do AEMET OpenData:

* [https://opendata.aemet.es/centrodedescargas/inicio](https://opendata.aemet.es/centrodedescargas/inicio)

Siga as instruções para gerar sua chave de acesso.

### Arquivo `key.txt`

Na raiz do projeto (`aemet-opendata/`), crie o arquivo `key.txt` com o seguinte conteúdo:

```python
key = "SUA_CHAVE_AQUI"
```

Requisitos:

* A chave deve estar entre aspas
* O arquivo `key.txt` deve permanecer no mesmo diretório dos scripts

---

## Inventário de Estações

O projeto utiliza o arquivo `todas_estacoes.csv`, que contém o inventário completo das estações disponíveis na API da AEMET.

### Geração do inventário

Caso o arquivo ainda não exista, execute:

```bash
python aemet_inventory_stations.py
```

O script consulta a API da AEMET e gera automaticamente o arquivo com as seguintes colunas:

* `provincia`
* `latitud`
* `longitud`
* `altitud`
* `indicativo`
* `nombre`
* `indsinop`

---

## Uso dos Scripts

### Histórico Diário de Insolação

Script: `aemet_insolation_history.py`

Responsável pelo download do **histórico diário de insolação** para todas as estações disponíveis.

#### Argumentos

* `--ano` — Ano desejado (padrão: `2024`)
* `--datai` — Data inicial (`YYYY-MM-DD`)
* `--dataf` — Data final (`YYYY-MM-DD`)
* `--janela` — Número de dias por requisição (padrão: `14`)

Nota: a limitação de janela decorre das restrições da API da AEMET.

#### Exemplos

```bash
# Ano padrão (2024) e janela de 14 dias
python aemet_insolation_history.py

# Ano específico
python aemet_insolation_history.py --ano 2023

# Intervalo de datas
python aemet_insolation_history.py --datai 2023-01-01 --dataf 2023-03-31

# Ajuste da janela de requisição
python aemet_insolation_history.py --ano 2025 --janela 7
```

#### Saída

Os arquivos são salvos em:

```text
dataset_daily/insolacao_diaria_ANO.csv
```

A pasta `dataset_daily` é criada automaticamente, caso não exista.

---

### Pipeline de Organização da Insolação

Script: `aemet_insolation_pipeline.py`

Processa os arquivos consolidados de insolação diária presentes em `dataset_daily`:

* Leitura dos CSVs anuais
* Separação dos dados por estação
* Geração de arquivos individuais organizados por **ano** e **estação**

#### Execução

```bash
python aemet_insolation_pipeline.py
```

Pré-requisito: a pasta `dataset_daily` deve conter os arquivos gerados pelo script `aemet_insolation_history.py`.

---

## Referências

* AEMET OpenData: [https://opendata.aemet.es](https://opendata.aemet.es)

---

## Contribuições

Contribuições são bem-vindas. Para sugerir melhorias, relatar problemas ou propor novas funcionalidades, utilize as **issues** do repositório ou envie um **pull request**.
