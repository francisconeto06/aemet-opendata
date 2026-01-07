# AEMET-OPENDATA

Projeto desenvolvido para automatizar o download e a coleta de dados de radiação solar das estações radiométricas operadas pela Agência Estatal de Meteorologia da Espanha (AEMET).

# Estrutura do Projeto

aemet-opendata/
├── aemet_insolation_history.py     # Algoritmo para baixar histórico diário de insolação da AEMET para todas as estações.
├── aemet_insolation_pipeline.py    # Organiza os dados baixados de Insolação diária em Horas
├── aemet_real_time_radiation.py    # Realiza download de Radiação Global, Direta e Difusa do dia anterior (disponível pela API)
├── aemet_inventory_stations.py     # Constrói csv com todas informações das estações disponíveis via API
├── utils.py                        # Contém funções e listas auxiliares
├── todas_estacoes.csv              # Inventário de todas estações disponível via API
├── aemet_metadata_real_time.csv    # Inventário que disponibiliza informações das estações "real-time" de radiação
└── README.md                       # Este arquivo

# Instalação

1) Realize o clone ou download deste projeto;
2) Este projeto foi testado usando Anaconda (conda 25.5.1);
3) Foi utilizado o Python 3.13.5

- Exemplo de criação de ambiente:

>> conda create -n aemet-opendata python=3.13.5 pandas tqdm requests
>> conda activate aemet-opendata

# Bibliotecas

Bibliotecas que os scripts fazem uso. Mas, se realizou a criação do ambiente conda da forma anterior, essas bibliotecas estaram instaladas. 

- [datetime](https://docs.python.org/3/library/datetime.html)
- [argparse](https://docs.python.org/3/library/argparse.html)
- [requests](https://requests.readthedocs.io/en/latest/)
- [pandas](https://pandas.pydata.org/docs/)
- [time](https://docs.python.org/3/library/time.html)
- [json](https://docs.python.org/3/library/json.html)
- [time](https://docs.python.org/3/library/time.html)
- [sys](https://docs.python.org/3/library/sys.html)
- [os](https://docs.python.org/3/library/os.html)

# Uso

Os scripts em Python 3.13.5 permitem automatizar a obtenção das seguintes variáveis:

-> Radiação Global (GL) em 10 * kj/m²

-> Radiação Difusa (DF) em 10 * kj/m²

-> Radiação Direta (DT) em 10 * kj/m²

-> Insolação (Sol) em horas

**Primeiro Passo:** Criar o arquivo key.txt

Antes de usar os scripts, o usuário precisa gerar sua própria chave (key) no seguinte link: https://opendata.aemet.es/centrodedescargas/inicio

Siga as instruções do site para gerar a chave e, em seguida, cole o valor obtido na variável key dentro do arquivo key.txt criado pelo usuário.

Atenção: Colar entre aspas a chave na variável key nesse formato:

key = " "

OBS: o arquivo key.txt deve está dentro da mesma pasta do projeto, ou seja, dentro da pasta aemet-opendata

**Segundo Passo:** Criar o arquivo todas_estacoes.csv

Assim como no passo anterior, este arquivo já está incluído no repositório caso você tenha feito o clone do projeto.

Alguns scripts utilizam este arquivo para gerar as saídas contendo código da estação, nome, latitude, longitude e altitude.

Caso você não tenha o arquivo, basta executar o script aemet_inventory_stations.py. Ele fará a requisição à API da AEMET e criará automaticamente o arquivo todas_estacoes.csv com todas as estações disponíveis via API.

**Terceiro Passo:** Executar os downloads

- aemet_inventory_stations.py

Script que baixa o inventário de todas as estações da AEMET. Os dados são armazenados em arquivos CSV com as seguintes colunas:
provincia, latitud, longitud, altitud, indicativo, nombre, indsinop

Exemplo de uso
>> python aemet_inventory_stations.py

- aemet_insolation_history.py
  
Algoritmo para baixar histórico diário de insolação da AEMET para todas as estações.

Faz uso de argumentos de linha de comando para definir o ano, datas inicial e final, tamanho da janela de dias para cada requisição, e arquivo de saída.

Exemplo de uso:
>> python aemet_insolation_history.py  **(Default --ano 2024 e --janela 14)**
>> python aemet_insolation_history.py --ano 2023
>> python aemet_insolation_history.py --datai 2023-01-01 --dataf 2023-03-31
>> python aemet_insolation_history.py --ano 2025 --janela 7

Se usuário usar somente o argumento **--ano**, o script baixa dados de 1º de janeiro até 31 de dezembro daquele ano.

Se usar **--datai** e/ou **--dataf**, o script baixa dados entre essas datas.

O argumento **--janela** define quantos dias cada requisição abrange (padrão 14). Isso devido a limitações da API da AEMET.

O arquivo de saída padrão é 'dataset_daily/insolacao_diaria_ANO.csv', onde ANO é o ano especificado. Se a pasta dataset_daily não existir, será criada automáticamente.

- aemet_insolation_pipeline.py

Pipeline para processar os arquivos consolidados de insolação diária da AEMET. Lê os arquivos CSV na pasta 'dataset_daily', separa os dados por estação, e salva arquivos individuais para cada estação em subpastas organizadas por ano.

Requer a pasta 'dataset_daily' com os arquivos CSV baixados previamente pelo script **aemet_insolation_history.py**.

Exemplo de uso
>> python aemet_insolação_pipeline.py

# Referencias

-Para mais informações sobre o serviço OpenData da AEMET, consulte:
👉 https://opendata.aemet.es
