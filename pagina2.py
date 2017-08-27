class Pagina(object):
    

    def __init__ (self, url, titulo = '', h1='', h2='', h3='', h4='', h5='', h6='', negrito=''):
        self.titulo = titulo
        self.url = url
        self.titulo = titulo
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.h5 = h5
        self.h6 = h6
        self.negrito = negrito

        self.filhos = []

    
