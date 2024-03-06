import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dataanalise


def analisar():
    dados = pd.read_html('https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_taxa_de_homic%C3%ADdios')
    mais250 = dados[0]
    menores = dados[1]
    print(dados[0])

def lerdados():
    dados = pd.read_csv(r'C:\Users\joseb\PycharmProjects\ProjetoWeb\dadosIndicadoresPB3.csv')
    #excluir colunas
    dados.drop(columns=['code'], inplace=True)
    return dados

def exibirmapacorrelacoes(data):
    data.drop(columns=['municipio'], inplace=True)
    fig = px.imshow(data.corr())
    return fig

def exibirgraficobarraseduc(dados):
    fig = px.bar(dados, x='municipio', y='somaedu')
    return fig

def exibirgraficopibpemprego(dados):
    dados['pibemprego'] = dados['pessoalocupado'], dados["pib"]
    fig = px.pie(dados, values='pibemprego', names='municipio', title='Pessoas empregadoas por municipios')
    return fig

def exibirgraficoidebidh(dados):
    fig = px.line(dados, x='idh', y='municipio')
    return fig


def gerar_tabela(nome_coluna):
    if nome_coluna not in lerdados().columns:
        return "A coluna especificada não foi encontrada."

    else:
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Município', nome_coluna]),
            cells=dict(values=[lerdados()['municipio'], lerdados()[nome_coluna]])
        )])

        return fig

'''
['Municípios', 'Gentílico',
       'Salário médio mensal dos trabalhadores formais', 'PIB per capita',
       'IDEB – Anos finais do ensino fundamental (Rede pública)',
       'População no último censo']
'''