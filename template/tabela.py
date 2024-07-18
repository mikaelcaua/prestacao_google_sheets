# #instalar
# #pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os.path
from flask import jsonify
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SAMPLE_SPREADSHEET_ID = "1-HDlz48aobDDazgdyoZW0LxVU_8ztUik68Bkk786kqA"
SAMPLE_RANGE_NAME = "Página1!A2:J100"

class Tabela:
    def __init__(self):
        self.dados = None
        self.carregar_dados()

    def carregar_dados(self):
        creds = None
        if os.path.exists("./auth/token.json"):
            creds = Credentials.from_authorized_user_file("./auth/token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "./auth/credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("./auth/token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build('sheets', 'v4', credentials=creds, client_options={"quota_project_id": SAMPLE_SPREADSHEET_ID})
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
            self.dados = result.get("values", [])
        except HttpError as err:
            print(err)

    def obter_dados_como_json(self):
        prestacoes_contas = []
        if self.dados is not None:
            for index, linha in enumerate(self.dados):
                dados_linha = {
                    'descricao': str(linha[0]),
                    'instituicao': str(linha[1]),
                    'cpf': str(linha[2]),
                    'tipoPagamento': str(linha[3]),
                    'dataInicial': str(linha[4]),
                    'formaPagamento': str(linha[5]),
                    'dataFinal': str(linha[6]),
                    'valor': str(linha[7]),
                    'mes': str(linha[8]),
                    'ano': str(linha[9]),
                    'id': index+1
                }
                prestacoes_contas.append(dados_linha)
        return jsonify(prestacoes_contas)

    def postPrestacao(self, data):

        descricao= data.get('descricao') 
        instituicao= data.get('instituicao') 
        cpf= data.get('cpf') 
        tipoPagamento= data.get('tipoPagamento') 
        dataInicial= data.get('dataInicial') 
        formaPagamento= data.get('formaPagamento') 
        dataFinal= data.get('dataFinal') 
        valor= data.get('valor') 
        mes= data.get('mes') 
        ano= data.get('ano') 
         
        
        
        creds = Credentials.from_authorized_user_file("./auth/token.json", SCOPES)
        service = build('sheets', 'v4', credentials=creds, client_options={"quota_project_id": SAMPLE_SPREADSHEET_ID})
    
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        next_free_position = len(values) + 2
        valores_adicionar = [
            [descricao, instituicao,cpf,tipoPagamento, dataInicial, formaPagamento,dataFinal,valor,mes,ano]
        ]

        result = sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=f'A{next_free_position}',
            valueInputOption="USER_ENTERED",
            body={'values': valores_adicionar}
        ).execute()

        self.carregar_dados()

        response = {'message': 'Data received and added to spreadsheet successfully', 'descricao': descricao}
        return jsonify(response), 200
