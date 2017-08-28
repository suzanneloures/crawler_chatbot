from flask import Flask, current_app, request
from pagina2 import Pagina
from crawler import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    return current_app.send_static_file('webchat.html')

@app.route('/perguntar', methods = ['POST'])
def perguntar():
    pergunta = request.form['pergunta']
    retorno = buscar(pergunta)
    if len(retorno) == 0:
        return "<br/> Não encontrei nada relacionado a sua questão. Tente palavras chaves"
    return '<br/> Verifiquei que as seguintes páginas correspondem à sua pergunta: '+'<br/>'+retorno[0].url


@app.route('/acerto', methods = ['POST'])
def acerto():
    global resultados
    id = request.form['id']
    resultado = resultados[id]
    resultado.acerto = True
    resultado[id] = resultado
    return 1

