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

Se clonar este projeto, este arquivo já está criado, sendo assim, não necessitando ser criado novamente. Contudo, antes de usar os scripts, o usuário deve gerar uma chave (key) no seguinte link: https://opendata.aemet.es/centrodedescargas/inicio e seguir as orientações do site. Após isso, pode colar na variável "key" do arquivo .txt disponibilizado neste projeto.

- Segundo Passo: Criar o arquivo todas_estacoes.csv

Mesmo caso do anterior, alguns scripts usa esse arquivo para gerar o arquivo de saída com as informações do código da estação, nome, latitude, longitudo e altitude. Dessa forma, se o usuário fazer o clone deste projeto, o mesmo já estará criado. Caso contrário, deve primeiro executar o código *inventario_stations.py*, onde será criado o arquivo com todas as estações disponibilidado na API da AEMET.

- Terceiro Passo: Executar os download

Agora seu diretório está preparado para realizar os download. Neste projeto, tem três principais opções para realizar o download de variáveis de radiação, são elas: Baixar a estatística mensal da Radiação Global (GL) e Insolação (Sol); baixar estatísticas diárias históricas de Insolação e dados do último dia de Radiação Global, Radiação Difusa e Radiação Direta. A seguir será descrito cada script .py

