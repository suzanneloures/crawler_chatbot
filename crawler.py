from robobrowser import RoboBrowser
from pagina2 import Pagina
from sqlalchemy.orm import sessionmaker
import sys

def url_navegavel(url):
    global url_pagina_inicial

    
    if(not url.startswith("http")):
        return url_pagina_inicial+ "/" + url

    return url

def valida_url(url):
    global vetor_links

    
    if(url.startswith('http') ):
        if(not url.startswith(url_pagina_inicial)):
            return False
    
    if(url in vetor_links ):
        return False
    
    if(url.startswith("#")):
        return False
    if(url.startswith('javascript')):
        return False
    
    if(url.startswith('mailto:')):
        return False
    
    if(url == '/'):
        return False
    
    return True

def captura (pagina):
    global vetor_paginas
    global nivel
    global vetor_links

    
    browser = RoboBrowser()
    try:
        browser.open(url_navegavel(pagina.url))
        
        
        pagina.titulo = "".join([t.text for t in browser.select('title')])
        pagina.h1 = " ".join([t.text for t in browser.select('h1')])
        pagina.h2 = " ".join([t.text for t in browser.select('h2')])
        pagina.h3 = " ".join([t.text for t in browser.select('h3')])
        pagina.h4 = " ".join([t.text for t in browser.select('h4')])
        pagina.h5 = " ".join([t.text for t in browser.select('h5')])
        pagina.h6 = " ".join([t.text for t in browser.select('h6')])
        pagina.negrito = " ".join([t.text for t in browser.find_all(['strong', 'b'])])
        links = browser.select('a')

        if(len(vetor_paginas) <= nivel+1):
            vetor_paginas.insert(nivel+1, [])

        for link in links:
            if(link.has_attr('href') and valida_url(link['href'])):
                p = Pagina(link['href'])
                p.pai = pagina
                pagina.filhos.append(p)
                vetor_paginas[nivel + 1].append(p)
                vetor_links.append(link['href'])
    except:
        print("erro")
        e = sys.exc_info()[0]
        print(e)

#engine = create_engine('sqlite:///banco.db', echo=True)
#vetor_links = []
vetor_titulos = []
vetor_paginas = []
vetor_links = []

vetor_paginas.insert(0, [])

# Browse to Rap Genius
url_pagina_inicial = 'http://www.avansys.com.br'
vetor_links.append(url_pagina_inicial)
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

while(len(vetor_paginas[nivel])>0):
    if(len(vetor_paginas[nivel]) == posicao_largura ):
        nivel += 1
        posicao_largura = 0
    else:
        captura(vetor_paginas[nivel][posicao_largura])
        posicao_largura += 1




while(True):
    comando = input("Deseja fazer uma busca? S/N")
    if(comando.upper() == "N"):
        quit()
    busca = input("Em que posso ajudar?")

    removepalavras = ['e','é','nem', 'não','nao','entanto', 'ainda', 'assim', 'mas', 'tambem','senão','senao','que','como','pois','porque',
                        'por','isso', 'já', 'visto', 'do', 'de', 'ou', 'quer', 'logo', 'porquanto', 'depois', 'mais',
                        'maior', 'melhor','menos', 'menor', 'tanto','se' ,'bem', 'contanto', 'desde', 'dado','ser',
                      'exceto','quando', 'apenas', 'antes', 'logo','sempre', 'tão', 'tal','para', 'os','as','o','a', 'um'
                      'uma', 'uns', 'umas','onde','após', 'até', 'com', 'contra', 'em','entre','perante', 'por', 'sem',
                      'sobre', 'trás']

    #removepontuacao = ['?','.',',','!',':','"',';','-']

    querybusca = busca.split()
    resultadobusca = [palavra for palavra in querybusca if palavra.lower() not in removepalavras]
    #rbusca = ' '.join(resultadobusca)

    for profundidade in range(0,len(vetor_paginas)-1):
        if(len(vetor_paginas[profundidade]) > 0):
            for largura in range(0,len(vetor_paginas[profundidade])-1):
                for palavra in resultadobusca:
                    if palavra.upper() in vetor_paginas[profundidade][largura].h1.upper() + vetor_paginas[profundidade][largura].titulo.upper() \
                            + vetor_paginas[profundidade][largura].h2.upper() + vetor_paginas[profundidade][largura].h3.upper() + \
                            vetor_paginas[profundidade][largura].h4.upper():
                        print(vetor_paginas[profundidade][largura].url)
                        break






    #Session = sessionmaker(bind=engine)
    #session = Session()
    #session.add(pagina)
    #session.commit()