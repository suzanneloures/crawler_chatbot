from flask import Flask, current_app, request, jsonify, Response, redirect
import json
from pagina2 import Pagina
from crawler import *
from resultado import Resultado
app = Flask(__name__)


@app.route('/')
def hello_world():
    return current_app.send_static_file('webchat.html')

@app.route('/perguntar', methods = ['POST'])
def perguntar():
    global resultados
    pergunta = request.form['pergunta']
    retorno = buscar(pergunta)
    '''if len(retorno) == 0:
        return "<br/> Não encontrei nada relacionado a sua questão. Tente palavras chaves"
    return '<br/> Verifiquei que as seguintes páginas correspondem à sua pergunta: '+'<br/>'+retorno[0].url'''
    ordernar_resultados(retorno)
    resposta = retorno[:5]
    resultados.extend(resposta)
    return Response(json.dumps([ob.__dict__ for ob in resposta]),  mimetype='application/json')


@app.route('/acerto', methods = ['POST'])
def acerto():
    global resultados
    id = request.form['id']
    for r in resultados:
        if r.id == int(id):
            r.setacerto()
            break
    #resultado = resultados[int(id)]
    #resultado.setacerto()
    #resultados[int(id)] = resultado
    return "ok"

@app.route('/lista')
def lista():
    global resultados
    return Response(json.dumps([ob.__dict__ for ob in resultados]), mimetype='application/json')

@app.route('/segue',methods=['GET'])
def segue():
    global resultados
    print(request.args.get('id'))
    id = int(request.args.get('id'))
    for r in resultados:
        if(r.id == id):
            return redirect(r.url)

@app.route('/captura',methods=['GET'])
def home():
    inicia()
    return "ok"