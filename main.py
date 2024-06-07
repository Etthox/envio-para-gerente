import calendar
import os
import sys
import requests
import pandas as pd
import pyodbc 
import numpy as np
import warnings
from datetime import date, datetime, timedelta
import json
import queries
import db
import time
import json
import smtplib
import ssl
from email.message import EmailMessage
import pyodbc
import pandas as pd
from datetime import datetime
from env import CONX_STRING,CONX_STRING_ETL, env

# Define email sender and receiver


# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email
try:
    def envio_email(descricao_estrutura,nome_gerente, nome_tarefa, numero_tarefa, data, estrutura, colaborador_nome, colaborador_funcao,juncao, email_gerente, pdf, id_tarefa, criado_tarefa, servico_descricao):
        email_sender = '...'
        email_password = '...'
        #email_receiver = email_gerente
        email_receiver = str(email_gerente)

        # Set the subject and body of the email
        subject = 'Não Conformidade | Visita Oper. Liderança: {}'.format(descricao_estrutura)

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject

        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            data_hora = str(data)
            if '.' not in data_hora:
                # Adicionar três zeros para representar os segundos
                data_hora += '.000'
            
            # Formatar a data e hora corretamente antes de converter em objeto datetime
            try:
                data_hora_obj = datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S.%f")
                data_hora_formatada = data_hora_obj.strftime("%d/%m/%Y %H:%M:%S")
            except ValueError:
                # Tratar o erro de formato de data
                data_hora_formatada = "Formato de data inválido"

            link_clicavel = f"<a href='{pdf}'>Baixar Relatório (PDF)</a>"

            # Construir o corpo do e-mail
            body = f" {nome_tarefa} | {servico_descricao} | #{numero_tarefa} <br><br> Data de realização da visita: {data_hora_formatada} <br><br> Local: {estrutura} <br><br> Executor: {colaborador_nome} Função: {colaborador_funcao} <br><br> {juncao} <br><br> {link_clicavel} <br><br>"
            print(body)

            # Configurar o conteúdo do e-mail
            em.set_content(body, subtype='html')

            # Conectar ao servidor SMTP e enviar o e-mail
            smtp.connect("smtp.office365.com", 587)
            smtp.ehlo('127.0.0.1')
            smtp.starttls()
            smtp.ehlo('127.0.0.1')
            smtp.login(email_sender, email_password)
            smtp.send_message(em)

            conn = pyodbc.connect(CONX_STRING_ETL)
            cursor = conn.cursor()

            print(id_tarefa,criado_tarefa)
            criado_tarefa_formatado = criado_tarefa[:-3]
            criado_tarefa_datetime = datetime.strptime(criado_tarefa_formatado, "%Y-%m-%d %H:%M:%S.%f")
            cursor.execute("INSERT INTO logEmailVisita (Id, IdTarefa, CriadoTarefa, Criado) VALUES (NEWID(), ?, ?, GETDATE())", (id_tarefa, criado_tarefa_datetime))


            conn.commit()

except Exception as e:
    print("Erro ao enviar o email: ", e)

    
def main():
    perguntas = []
    respostas = []
    while True:
        df_get_tarefas_visita_nao = db.get_tarefas_visita_nao()
        grouped = df_get_tarefas_visita_nao.groupby('numero')

        # Iterar sobre cada grupo
        for numero_tarefa, group_df in grouped:
            juncao = ""
            # Preencher a lista de perguntas e respostas com os dados de cada linha do grupo
            for index, row in group_df.iterrows():
                df_get_email_enviado = db.get_email_enviado(row['Id'])
                if df_get_email_enviado.empty:
                    df_get_gerentes_nome = db.get_gerente_nome(row['Id'])
                    df_get_gerentes_email = db.get_gerente_email(row['Id'])
                    df_get_cpf = db.get_cpf(row['Id'])
                    df_get_recurso = db.get_recurso(df_get_cpf['finalizadopor'].iloc[0])

                    nome_gerente = df_get_gerentes_nome['Conteudo'].iloc[0]
                    email_gerente = df_get_gerentes_email['Conteudo'].iloc[0]
                    servico_descricao = row['servico']
                    id_tarefa = row['Id']
                    criado_tarefa = row['criado']
                    nome_tarefa = row['nome']
                    data = row['terminoreal']
                    estrutura = row['hierarquiadescricao']
                    colaborador_nome = df_get_recurso['Nome'].iloc[0]
                    colaborador_funcao = df_get_recurso['_String2'].iloc[0]
                    pergunta = row['perguntadescricao'] 
                    resposta = row['conteudo']
                    descricao_estrutura = row['descricao']
                    pdf = f"...={row['Id']}"

                    perguntas.append(pergunta)
                    respostas.append(resposta)


            # Se houver pelo menos uma pergunta não enviada por e-mail, enviar o e-mail
            # Inicializando uma string vazia para armazenar as perguntas e respostas formatadas
                    juncao = ""

                    # Se houver pelo menos uma pergunta não enviada por e-mail, enviar o e-mail
                    for pergunta, resposta in zip(perguntas, respostas):
                        pergunta_sem_colchetes = pergunta.replace("[", "").replace("]", "")
                        resposta_sem_colchetes = resposta.replace("[", "").replace("]", "")
                        perguntas_e_respostas = f"Pergunta: {pergunta_sem_colchetes}<br>Resposta: {resposta_sem_colchetes}<br><br>"
                        juncao += perguntas_e_respostas

                    # Imprimindo a string resultante
                    print(juncao)
                    envio_email(descricao_estrutura,nome_gerente, nome_tarefa, numero_tarefa, data, estrutura, colaborador_nome, colaborador_funcao,juncao, email_gerente, pdf, id_tarefa, criado_tarefa, servico_descricao)


            
if __name__ == "__main__":
    main()