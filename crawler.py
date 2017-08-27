import re
from robobrowser import RoboBrowser
from .pagina2 import Pagina
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///banco.db', echo=True)
vetor_links = []
vetor_titulos = []
vetor_paginas = []

vetor_links.insert(1, [])

# Browse to Rap Genius
url_pagina_inicial = 'http://www.dmat.ufba.br'
nivel = 1



browser = RoboBrowser() # history=true volta para pagina anterior
browser.open(url_pagina_inicial)
links = browser.select('a')
browser.find_all(['h1','h2','h3','h4','h5','h6'])

for link in links:
    if(not link['href'].startswith('http') and link['href'] not in vetor_links):
        vetor_links.append(link['href'])
        browser.open(url_pagina_inicial + link['href'])

# funcao captura todos os titulos e links da pagina e salva no vetor

def captura (url):
    global vetor_links
    global vetor_titulos
    global engine
    global nivel

    browser = RoboBrowser()
    browser.open(url)

    pagina = Pagina()
    pagina.url = url
    pagina.titulo = browser.select('title')
    pagina.h1 = browser.select('h1')
    pagina.h2 = browser.select('h2')
    pagina.h3 = browser.select('h3')
    pagina.h4 = browser.select('h4')
    pagina.h5 = browser.select('h5')
    pagina.h6 = browser.select('h6')
    pagina.negrito = browser.find_all(['strong', 'b'])
    links = browser.select('a')

    for posicao in links:
        if(not link['href'].startswith('http') and link['href'] not in vetor_links):
            vetor_links.append(link['href'])

    pagina = Pagina()
    pagina.link = url
    pagina.titulo = titulo
    pagina.h1 = h1
    pagina.h2 = h2
    pagina.h3 = h3
    pagina.h4 = h4
    pagina.h5 = h5
    pagina.h6 = h6
    pagina.strong = strong
    pagina.negrito = negrito

    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(pagina)
    session.commit()