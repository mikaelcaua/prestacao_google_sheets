# from flask import Flask,request
# from flask_cors import CORS
# from model.tabela import Tabela


# app = Flask(__name__)
# CORS(app)  # Habilita CORS para todo o aplicativo

# tabela = Tabela()

# @app.route('/',methods=['GET', 'POST'])
# def homepage():
#     if request.method == 'GET':
#         dados = tabela.obter_dados_como_json()
#         return dados
#     elif request.method == 'POST':
#         tabela.postPrestacao

# if __name__ == "__main__":
#     app.run()

from flask import Flask, request, jsonify
from flask_cors import CORS
from model.tabela import Tabela

app = Flask(__name__)
CORS(app)  # Habilita CORS para todo o aplicativo

tabela = Tabela()

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return tabela.obter_dados_como_json()
    elif request.method == 'POST':
        return tabela.postPrestacao(request.get_json())

if __name__ == "__main__":
    app.run(debug=True)
