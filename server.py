from flask import Flask, current_app, request, jsonify, Response, redirect
import json
from pagina2 import Pagina
from crawler import *
from resultado import Resultado
app = Flask(__name__)

#SERVE PAGINA INICIAL
@app.route('/')
def index():
    return current_app.send_static_file('webchat.html')

#SERVE POR JSON AS RESPOSTAS DAS PERGUNTAS
@app.route('/perguntar', methods = ['POST'])
def perguntar():
    global resultados
    pergunta = request.form['pergunta']
    retorno = buscar(pergunta)
    ordernar_resultados(retorno)
    resposta = retorno[:5]
    resultados.extend(resposta)
    return Response(json.dumps([ob.__dict__ for ob in resposta]),  mimetype='application/json')

#RECEBE A INFORMAÇÃO QUE UMA RESPOSTA ESTÁ CORRETA
@app.route('/acerto', methods = ['POST'])
def acerto():
    global resultados
    id = request.form['id']
    for r in resultados:
        if r.id == int(id):
            r.setacerto()
            break
    return "ok"

@app.route('/remove', methods = ['POST'])
def remover():
    global resultados
    id = request.form['id']
    for r in resultados:
        if r.id == int(id):
            resultados.remove(r)
            break
    return "ok"

#LISTA TODOS OS RESULTADOS
@app.route('/lista')
def lista():
    global resultados
    return Response(json.dumps([ob.__dict__ for ob in resultados]), mimetype='application/json')

#NÃO UTILIZADO
@app.route('/segue',methods=['GET'])
def segue():
    global resultados
    print(request.args.get('id'))
    id = int(request.args.get('id'))
    for r in resultados:
        if(r.id == id):
            return redirect(r.url)

#MÉTODO QUE DEVE SER CHAMADO PRIMEIRO PARA CAPTURAR DE UM SITE
@app.route('/captura',methods=['GET'])
def home():
    inicia()
    return "ok"