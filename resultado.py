class Resultado():

    def __init__(self,id,h1= False,h2= False,h3=False,titulo=False, url=False, acerto = False):
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.h5 = h5
        self.titulo = titulo
        self.url = url
        self.acerto = acerto
        self.probabilidade = 0
        self.id = id

    def setacerto(self):
        self.acerto=True