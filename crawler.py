import urllib.parse
from robobrowser import RoboBrowser
from pagina2 import Pagina
from resultado import Resultado
from config import *
import sys

#função p/ buscar sinônimos (não utilizado)
def sinonimos(palavra):
    palavra = urllib.parse.quote(palavra)
    browser = RoboBrowser()
    browser.open('https://www.sinonimos.com.br/'+ palavra)
    return [t.text for t in browser.select('.sinonimo')]

#inclui (se necessário) o http://site.com... antes do link
def url_navegavel(url):
    global url_pagina_inicial
    
    if(not url.startswith("http")):
        return url_pagina_inicial+ "/" + url

    return url

#função para validar url(se é interna e já não foi capturada)
def valida_url(url):
    global vetor_links

    #verfica se começa com http.. se começa verifica se o endereço inicial é do proprio site
    if(url.startswith('http') ):
        if(not url.startswith(url_pagina_inicial)):
            return False
    #verifica se  não é arquivo
    if(url.endswith(".jpg") or url.endswith(".png") or url.endswith(".jpeg") or url.endswith(".bmp") or url.endswith(".pdf") or url.endswith(".gif")):
        return False

    #verifica se já não está no vetor de links
    if(url in vetor_links ):
        return False

    #verifica se não começa com hashtag
    if(url.startswith("#")):
        return False

    #verifica se não é uma ação javascrit
    if(url.startswith('javascript')):
        return False

    #verifica se não é link para email
    if(url.startswith('mailto:')):
        return False

    if(url == '/'):
        return False
    
    return True

#pega as informações de uma página (h1 titulo...) e cria nós filhos a partir dos links encontrados (filhos vão pro proximo nivel do vetor)
def captura (pagina):
    global vetor_paginas
    global nivel
    global vetor_links
    global MAX_PAGINAS

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

        #cria filhos em vetor_pagina
        for link in links:
            if(link.has_attr('href') and valida_url(link['href'])):
                p = Pagina(link['href'])
                p.pai = pagina
                pagina.filhos.append(p)
                niveis = len(vetor_paginas) - 1
                total_paginas = 0
                for n in range(0,niveis):
                    total_paginas += len(vetor_paginas[n])
                if total_paginas < MAX_PAGINAS:
                    vetor_paginas[nivel + 1].append(p)
                    vetor_links.append(link['href'])
    except:
        print("erro")
        e = sys.exc_info()[0]
        print(e)


vetor_titulos = []
vetor_paginas = [] #vetor para salvar as paginas no formato de árvore
vetor_links = [] #vetor para validar lins já encontrados

#inicializa vetor de páginas com a página inicial
vetor_paginas.insert(0, [])
global PAGINA_INICIAL
url_pagina_inicial = PAGINA_INICIAL
print(PAGINA_INICIAL)
vetor_links.append(url_pagina_inicial)
nivel = 0
posicao_largura = 0
resultados = []
id_resultado = 0
p_inicial = Pagina(url_pagina_inicial)

vetor_paginas[0].append(p_inicial)

#inicia a captura pela posição inicial do vetor (que vai gerando os filhos) e segue para próximos níveis
def inicia():
    global vetor_paginas
    global nivel
    global posicao_largura
    while(len(vetor_paginas[nivel])>0): #se o nível tem páginas.. se não tem é pq o nivel de cima n tem filhos
        if(len(vetor_paginas[nivel]) == posicao_largura ):
            nivel += 1
            posicao_largura = 0
        else:
            captura(vetor_paginas[nivel][posicao_largura])
            posicao_largura += 1

#ordena o vetor de resultados ordenado pela probabilidade
def ordernar_resultados(lista):
    global resultados
    print(len(resultados))

    #se o total de resultados > 0
    if len(resultados) > 0:
        prob_acerto = float(len([r for r in resultados if r.acerto==True])) / float(len(resultados)) #probabilidade de um acerto
        print(prob_acerto)
    else:
        prob_acerto = 0
    for l in lista: #para cada resultado na lista de resultados
        print(prob_acerto)
        if(prob_acerto==0):
            l.probabilidade = 0
        else:
            prob_condicao = float(len([r for r in resultados if r.h1 == l.h1 and r.h2 == l.h2 and r.h3 == l.h3 and r.h4 == l.h4  and r.h5 == l.h5 and r.h6 == l.h6
                                       and r.negrito == l.negrito and r.titulo == l.titulo ]))/float(len(resultados))
            if prob_condicao == 0:
                l.probabilidade = 0
            else:
                prob_acerto_e_condicao = float(len([r for r in resultados if r.h1 == l.h1 and r.h2 == l.h2 and r.h3 == l.h3 and r.h4 == l.h4  and r.h5 == l.h5 and r.h6 == l.h6
                                       and r.negrito == l.negrito and r.titulo == l.titulo and r.acerto==True]))/float(len(resultados))
                l.probabilidade = float(prob_acerto_e_condicao) / float(prob_condicao)
    lista.sort(key=lambda x: x.probabilidade, reverse=True) #ordena pela probabilidade

#dado um texto (busca) tenta encontrar no vetor_paginas uma página que tenha as tags em h1..titulo...
def buscar(busca):
    resposta = []
    #busca = input("Em que posso ajudar?")
    global profundidade
    global vetor_paginas
    global largura
    global vetor_links
    global id_resultado
    removepalavras = ['e', 'é', 'nem', 'não', 'nao', 'entanto', 'ainda', 'assim', 'mas', 'tambem', 'senão', 'senao',
                      'que', 'como', 'pois', 'porque',
                      'por', 'isso', 'já', 'visto', 'do', 'de', 'ou', 'quer', 'logo', 'porquanto', 'depois', 'mais',
                      'maior', 'melhor', 'menos', 'menor', 'tanto', 'se', 'bem', 'contanto', 'desde', 'dado', 'ser',
                      'exceto', 'quando', 'apenas', 'antes', 'logo', 'sempre', 'tão', 'tal', 'para', 'os', 'as', 'o',
                      'a', 'um'
                           'uma', 'uns', 'umas', 'onde', 'após', 'até', 'com', 'contra', 'em', 'entre', 'perante',
                      'por', 'sem',
                      'sobre', 'trás','vocês','têm','será','como']

    removepontuacao = ['?','.',',','!',':','"',';','-']
    for p in removepontuacao:
        busca = busca.replace(p,"")

    querybusca = busca.split()
    resultadobusca = [palavra for palavra in querybusca if palavra.lower() not in removepalavras]

    #varre o vetor paginas para achar as paginas com "Match" e devolve um vetor de Resultado()
    for profundidade in range(0, len(vetor_paginas) - 1):
        if (len(vetor_paginas[profundidade]) > 0):
            for largura in range(0, len(vetor_paginas[profundidade]) - 1):
                for palavra in resultadobusca:
                    resultado = Resultado(id_resultado + 1)
                    palavra = palavra.upper()
                    if palavra.upper() in vetor_paginas[profundidade][largura].h1.upper():
                        resultado.h1 = True
                    if palavra.upper() in vetor_paginas[profundidade][largura].h2.upper():
                        resultado.h2 = True
                    if palavra.upper() in vetor_paginas[profundidade][largura].h3.upper():
                        resultado.h3 = True
                    if palavra.upper() in vetor_paginas[profundidade][largura].h4.upper():
                        resultado.h4 = True
                    if palavra.upper() in vetor_paginas[profundidade][largura].h5.upper():
                        resultado.h5 = True
                    if palavra.upper() in vetor_paginas[profundidade][largura].h6.upper():
                        resultado.h6 = True
                    if palavra.upper() in vetor_paginas[profundidade][largura].negrito.upper():
                        resultado.negrito = True
                    if palavra.upper() in vetor_paginas[profundidade][largura].titulo.upper():
                        resultado.titulo = True
                    if(resultado.titulo or resultado.h1 or resultado.h2 or resultado.h3 or resultado.h4 or resultado.h5 or resultado.h6 or resultado.negrito):
                        resultado.url = url_navegavel(vetor_paginas[profundidade][largura].url)
                        #resultados.append(resultado)
                        id_resultado += 1
                        resposta.append(resultado)
    return resposta


#apenas caso rode pelo console
if __name__ == "__main__":
    while(True):
        comando = input("Deseja fazer uma busca? S/N")
        if(comando.upper() == "N"):
            quit()
        texto = input("Em que posso ajudar?")
        resultado_busca = buscar(texto)
        ordernar_resultados(resultado_busca)
        for r in resultado_busca:
            print(r.url + "/" )








    #Session = sessionmaker(bind=engine)
    #session = Session()
    #session.add(pagina)
    #session.commit()