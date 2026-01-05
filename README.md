# AEMET-OPENDATA

- Sobre os Scripts

Todos os scripts deste repositório realizam o download, tratamento e organização de dados meteorológicos provenientes da Agencia Estatal de Meteorología (AEMET), da Espanha.

Os dados utilizados são obtidos através da plataforma AEMET OpenData, que disponibiliza diversas variáveis meteorológicas em formato aberto.

-Para mais informações sobre o serviço OpenData da AEMET, consulte:
👉 https://opendata.aemet.es

- O que estes scripts fazem

Os scripts em Python 3.13.9 permitem automatizar a obtenção das seguintes variáveis:

-> Radiação Global (GL) em 10 * kj/m²

-> Radiação Difusa (DF) em 10 * kj/m²

-> Radiação Direta (DT) em 10 * kj/m²

-> Insolação (Sol) em horas

# Bibliotecas

- [datetime](https://docs.python.org/3/library/datetime.html)
- [argparse](https://docs.python.org/3/library/argparse.html)
- [requests](https://requests.readthedocs.io/en/latest/)
- [pandas](https://pandas.pydata.org/docs/)
- [time](https://docs.python.org/3/library/time.html)
- [json](https://docs.python.org/3/library/json.html)
- [time](https://docs.python.org/3/library/time.html)
- [sys](https://docs.python.org/3/library/sys.html)
- [os](https://docs.python.org/3/library/os.html)

# Orientações para Execução dos Scripts

- Primeiro Passo: Criar o arquivo key.txt

Antes de usar os scripts, o usuário precisa gerar sua própria chave (key) no seguinte link: https://opendata.aemet.es/centrodedescargas/inicio

Siga as instruções do site para gerar a chave e, em seguida, cole o valor obtido na variável key dentro do arquivo key.txt criado pelo usuário.
Anteção: Colar entre aspas a chave na variável key nesse formato:

key = " "

- Segundo Passo: Criar o arquivo todas_estacoes.csv

Assim como no passo anterior, este arquivo já está incluído no repositório caso você tenha feito o clone do projeto.

Alguns scripts utilizam este arquivo para gerar as saídas contendo código da estação, nome, latitude, longitude e altitude.

Caso você não tenha o arquivo, basta executar o script inventario_stations.py. Ele fará a requisição à API da AEMET e criará automaticamente o arquivo todas_estacoes.csv com todas as estações disponíveis.

- Terceiro Passo: Executar os downloads

Agora o diretório já está preparado para realizar os downloads.

Este projeto oferece três principais opções para baixar dados de radiação: 

Estatística mensal:

-> Radiação Global (GL)

-> Insolação (Sol)

**OBS:** *Obdecer a regra da API da AEMET, neste caso, eles só liberam baixar 36 meses de uma única vez.*

Estatísticas diárias históricas de Insolação

Dados do último dia de

-> Radiação Global

-> Radiação Difusa

-> Radiação Direta

A seguir, será detalhado como executar cada script .py

