import pyodbc 
import json
import pandas as pd
#teste
import queries
from env import CONX_STRING,CONX_STRING_ETL,CONX_STRING_REP, env

# ---- OBJETO DE CONEXAO ----
#define a conexão para o banco,
#conn = pyodbc.connect(CONX_STRING)

#conn_etl = pyodbc.connect(CONX_STRING_ETL)

nocount = """ SET NOCOUNT ON; """

conn = pyodbc.connect(CONX_STRING_REP)
cursor = conn.cursor()


# ---- MÉTODOS LOG ----
#define a conexão para o banco


def exec_query_prod(query): 
    conn = pyodbc.connect(CONX_STRING_REP)
    conn.cursor()

    df_result = pd.read_sql(nocount + query, conn)
    conn.close()
    return df_result

def exec_query_prod_dw(query): 
    conn = pyodbc.connect(CONX_STRING_ETL)
    conn.cursor()

    df_result = pd.read_sql(nocount + query, conn)
    conn.close()
    return df_result

def get_tarefas_visita_nao():
    try:
        conn = pyodbc.connect(CONX_STRING_REP)
        conn.cursor()
        
        df_result = pd.read_sql(nocount + queries.get_tarefas_visita_nao, conn)
        conn.close()
        return df_result
    except Exception as e:
        raise e
    
def get_cpf(idtarefa):
    try:
        conn = pyodbc.connect(CONX_STRING)
        conn.cursor()
        
        df_result = pd.read_sql(nocount + queries.get_cpf.format(idtarefa), conn)
        conn.close()
        return df_result
    except Exception as e:
        raise e
    
def get_email_enviado(idtarefa): 
    try:
        conn = pyodbc.connect(CONX_STRING_ETL)
        conn.cursor()
        
        df_result = pd.read_sql(nocount + queries.get_email_enviado.format(idtarefa), conn)
        conn.close()
        return df_result
    except Exception as e:
        raise e
    
def get_recurso(colaborador):
    try:
        conn = pyodbc.connect(CONX_STRING)
        conn.cursor()
        
        df_result = pd.read_sql(nocount + queries.get_recurso.format(colaborador), conn)
        conn.close()
        return df_result
    except Exception as e:
        raise e

def get_gerente_nome(idtarefa):
    try:
        conn = pyodbc.connect(CONX_STRING_REP)
        conn.cursor()
        
        df_result = pd.read_sql(nocount + queries.get_gerente_nome.format(idtarefa), conn)
        conn.close()
        return df_result
    except Exception as e:
        raise e
    
def get_gerente_email(idtarefa):
    try:
        conn = pyodbc.connect(CONX_STRING_REP)
        conn.cursor()
        
        df_result = pd.read_sql(nocount + queries.get_gerente_email.format(idtarefa), conn)
        conn.close()
        return df_result
    except Exception as e:
        raise e
