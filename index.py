from flask import Flask
from flask_cors import CORS
from template.tabela import Tabela


app = Flask(__name__)
CORS(app)  # Habilita CORS para todo o aplicativo

arquivo_csv = './base_dados/prestacao_contas.csv'
tabela = Tabela()

@app.route('/')
def homepage():
    dados = tabela.obter_dados_como_json()
    return dados

if __name__ == "__main__":
    app.run()
