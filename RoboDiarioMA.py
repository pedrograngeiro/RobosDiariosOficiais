from datetime import date
from bs4 import BeautifulSoup
import requests

# Função para pegar a data atual
def dataAtual():
    data = date.today()
    return data

def pegar_html(url):
    # Faz a solicitação para a URL
    resposta = requests.get(url)
    
    # Verifica se a resposta foi bem-sucedida
    if resposta.status_code == 200:
        # Usa o BeautifulSoup para analisar
        soup = BeautifulSoup(resposta.text, 'html.parser')
        pegar_links_dos_diarios(soup)
        return soup
    else:
        return None

def numero_de_diarios(soup):
    strong_tags = soup.find_all('strong')

    if len(strong_tags) >= 2:
        # Pegue o texto do segundo strong
        numero_str = strong_tags[1].get_text(strip=True).replace('\xa0', ' ')
        
        # Divida a string usando o hífen para pegar a segunda parte (ex: '1 - 10' -> '10')
        numero = int(numero_str.split('-')[-1].strip())
        
        return numero
    else:
        return None

def pegar_links_dos_diarios(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('https://www3.tjma.jus.br/diario/diarios/') and href.endswith('.pdf'):
            links.append(href)
            print(href)
    return links


if __name__ == '__main__':
    data_inicio = date(2023, 1, 1)
    data_fim = dataAtual()

    link = f'https://www.tjma.jus.br/portal/diario/1?data_inicial={data_inicio.day}/{data_inicio.month}/{data_inicio.year}&data_final={data_fim.day}/{data_fim.month}/{data_fim.year}'
    # link = f'https://www.tjma.jus.br/portal/diario?data_inicial={data_inicio.day}%2F{data_inicio.month}%2F{data_inicio.year}&data_final={data_fim.day}%2F{data_fim.month}%2F{data_fim.year}&pesquisar='
    
    htmlArmazenado = pegar_html(link)
    numero_de_diarios(htmlArmazenado)
    total_de_paginas = numero_de_diarios(htmlArmazenado) // 10 + 1
    print(total_de_paginas)
    for i in range(2, total_de_paginas + 1):
        link = f'https://www.tjma.jus.br/portal/diario/{i}?data_inicial={data_inicio.day}/{data_inicio.month}/{data_inicio.year}&data_final={data_fim.day}/{data_fim.month}/{data_fim.year}'
        htmlArmazenado = pegar_html(link)
        numero_de_diarios(htmlArmazenado)
        pegar_links_dos_diarios(htmlArmazenado)
        print(link)
    
    
    
    