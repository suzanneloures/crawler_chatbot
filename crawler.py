import re
from robobrowser import RoboBrowser


vetor_links = []
vetor_titulos = []

# Browse to Rap Genius
browser = RoboBrowser(history=True) # history=true volta para pagina anterior
browser.open('http://www.dmat.ufba.br/')
links = browser.select('a')
browser.find_all(['h1','h2','h3','h4','h5','h6'])

for link in links:
    if(not link['href'].startswith('http') and link['href'] not in vetor_links):
        vetor_links.append(link['href'])
        browser.open('http://www.dmat.ufba.br' + link['href'])
        print(browser.select('title')[0])

# funcao captura todos os titulos e links da pagina e salva no vetor

def captura (url):
    global vetor_links
    global vetor_titulos
    browser = RoboBrowser()
    browser.open(url)
    links = browser.select('a')
    cabecalho = browser.find_all(['h1','h2','h3','h4','h5','h6','strong','b'])
    for posicao in links:
        if(not link['href'].startswith('http') and link['href'] not in vetor_links):
            vetor_links.append(link['href'])
             
    