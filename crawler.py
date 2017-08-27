from robobrowser import RoboBrowser
from pagina2 import Pagina
from sqlalchemy.orm import sessionmaker

def url_navegavel(url):
    global url_pagina_inicial
    if(url.startswith("/")):
        return url_pagina_inicial + url

    return url

def valida_url(url):
    global vetor_links
    if(url.startswith('http') ):
        return False
    
    if(url in vetor_links ):
        return False
    
    if(url.startswith("#")):
        return False
    if(url.startswith('javascript')):
        return False
    
    if(url == '/'):
        return False
    
    return True

def captura (pagina):
    global vetor_paginas
    global nivel
    global vetor_links

    vetor_links.append(pagina.url)
    browser = RoboBrowser()
    browser.open(url_navegavel(pagina.url))

    
    
    pagina.titulo = browser.select('title')
    pagina.h1 = browser.select('h1')
    pagina.h2 = browser.select('h2')
    pagina.h3 = browser.select('h3')
    pagina.h4 = browser.select('h4')
    pagina.h5 = browser.select('h5')
    pagina.h6 = browser.select('h6')
    pagina.negrito = browser.find_all(['strong', 'b'])
    links = browser.select('a')

    if(len(vetor_paginas) <= nivel+1):
        vetor_paginas.insert(nivel+1, [])

    for link in links:
        if(link.has_attr('href') and valida_url(link['href'])):
            p = Pagina(link['href'])
            vetor_paginas[nivel + 1].append(p)
            vetor_links.append(link['href'])

#engine = create_engine('sqlite:///banco.db', echo=True)
#vetor_links = []
vetor_titulos = []
vetor_paginas = []
vetor_links = []

vetor_paginas.insert(0, [])

# Browse to Rap Genius
url_pagina_inicial = 'http://ufba.br'
nivel = 0
posicao_largura = 0

p_inicial = Pagina(url_pagina_inicial)

vetor_paginas[0].append(p_inicial)
#browser = RoboBrowser() # history=true volta para pagina anterior
#browser.open(url_pagina_inicial)
#links = browser.select('a')
#browser.find_all(['h1','h2','h3','h4','h5','h6'])

#for link in links:
#    if(not link['href'].startswith('http') and link['href'] not in vetor_links):
#        vetor_links.append(link['href'])
#        browser.open(url_pagina_inicial + link['href'])

# funcao captura todos os titulos e links da pagina e salva no vetor

while(vetor_paginas[nivel] is not None):
    if(len(vetor_paginas[nivel]) == posicao_largura ):
        nivel += 1
        posicao_largura = 0
    else:
        captura(vetor_paginas[nivel][posicao_largura])
        posicao_largura += 1
    






    #Session = sessionmaker(bind=engine)
    #session = Session()
    #session.add(pagina)
    #session.commit()