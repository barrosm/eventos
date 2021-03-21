import requests
from bs4 import BeautifulSoup as bs

# Por hábito, separo a url em domain, path e query (quando há)
domain_url = "https://www.gov.br/"
path_url = "planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/"
query_url = "2021-03-19"
url = domain_url + path_url + query_url

# Envio requisição HTTP para o servidor e armazeno o conteúdo
site = requests.get(url)

# print(site.status_code)
# OUTPUT: 200

# Faço o parsing do conteúdo com BeautifulSoup
content = bs(site.content, 'html.parser')

# print(content)
# OUTPUT: código-fonte do site
# <!DOCTYPE html>
# <html lang="pt-br" xml:lang="pt-br" xmlns="http://www.w3.org/1999/xhtml">
# <head>
# ...
# </body>
# </html>

# Ao observar o código-fonte, percebo que as informações que desejo estão
# aninhadas em <ul class="list-compromissos">...</ul>. Posso, então, descartar
# todo o restante do site.

lista = content.find('ul', class_='list-compromissos')

# print(lista)
# OUTPUT: código-fonte do elemento <ul>
# <ul class="list-compromissos">
# <li class="item-compromisso-wrapper">
# ...
# </li>
# <li class="item-compromisso-wrapper">
# ...
# </li>
# </ul>

# No código-fonte do elemento <ul>, observo que os dados que desejo
# estão dentro de <li class="item-compromisso-wrapper">...</li>, sendo:
# 1. horário inicial: <time class="compromisso-inicio">
# 2. horário final: <time class="compromisso-fim">
# 3. compromisso: <h4 class="compromisso-titulo">
# 4. local: <div class="compromisso-local">

# Encontro todos os <li class="item-compromisso-wrapper">
itens = lista.find_all('li', class_='item-compromisso-wrapper')

# Itero sobre os elementos <li class="item-compromisso-wrapper">
# e guardo as informações que desejo
for i in itens:
    inicio = i.find('time', class_="compromisso-inicio").text
    fim = i.find('time', class_="compromisso-fim").text
    compromisso = i.find('h4', class_="compromisso-titulo").text
    local = i.find('div', class_="compromisso-local").text
    # Salvo os dados num dict
    dicionario = dict(
        inicio=inicio,
        fim=fim,
        compromisso=compromisso,
        local=local
    )
    # print(dicionario)
    # OUTPUT: dict com os dados
    # {'inicio': '10h40', 'fim': '11h10', 'compromisso': 'Braga Netto,
    # Ministro-Chefe da Casa Civil da Presidência da República', 'local':
    # 'Palácio do Planalto'}
    # {'inicio': '15h00', 'fim': '15h50', 'compromisso': 'Pedro Cesar Sousa,
    # Subchefe para Assuntos Jurídicos da Secretaria-Geral da Presidência da
    # República', 'local': 'Palácio do Planalto'}
