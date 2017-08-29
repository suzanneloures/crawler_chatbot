class Resultado():

    def __init__(self,id,h1= False,h2= False,titulo=False, url=False, acerto = False):
        self.h1 = h1
        self.h2 = h2
        self.titulo = titulo
        self.url = url
        self.acerto = acerto
        self.probabilidade = 0
        self.id = id

    def setacerto(self):
        self.acerto=True