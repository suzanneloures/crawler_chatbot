from flask import Flask, current_app, request
from pagina2 import Pagina
from crawler import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    return current_app.send_static_file('chat.html')

@app.route('/perguntar', methods = ['POST'])
def perguntar():
    pergunta = request.form['pergunta']
    retorno = buscar(pergunta)
    if len(retorno) == 0:
        return "<br/> Não encontrei nada relacionado a sua questão. Por favor reformule"
    return '<br/>'+'<br/>'.join(retorno)