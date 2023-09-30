import requests
from bs4 import BeautifulSoup
import pandas as pd


# Pesquisa sobre profissões do futuro
URL = 'https://exame.com/carreira/estas-sao-as-10-profissoes-do-futuro-segundo-estudo-do-forum-economico-mundial/'
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

options = soup.find('div', {'id': 'news-body'}).find_all('li')

profissoes_futuro = [item.text for item in options][:10]
profissoes_desaparecer = [item.text for item in options][10:]

# Extraindo dados da base do cliente
dados_colab = pd.read_csv('Imaginario_colaboradores.csv')

# Modificando dados
colab_transicao_carreira = dados_colab[dados_colab[' profissaoColab'].isin(profissoes_desaparecer)]
colab_incentivo_carreira = dados_colab[dados_colab[' profissaoColab'].isin(profissoes_futuro)]

# Update ou criação dos relatórios
def criar_ou_editar_csv(arquivo, dados):
  try:
    arquivo_existe = pd.read(arquivo)
    update_arquivo = pd.concat([arquivo_existe,dados]).drop_duplicates(subset=['idColab'], keep='last')
  except:
    dados.to_csv(arquivo, index= False)

criar_ou_editar_csv('transicao_carreira.csv', colab_transicao_carreira)
criar_ou_editar_csv('incentivo_carreira.csv', colab_incentivo_carreira)
