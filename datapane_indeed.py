# -*- coding: utf-8 -*-

import altair as alt
import pandas as pd
import datapane as dp
from datetime import date
from folium import plugins
import folium
import plotly.express as px
import sys

import plotly.io as pio
pio.templates.default = "plotly_dark"

token_datapane = sys.argv[1]

dp.login(token= token_datapane)

cidades = pd.read_csv("cidades.csv")
df_vagas = pd.read_csv("vagas-ds.csv")

df_AD = df_vagas.loc[df_vagas.vaga == 'analista de dados']
df_CD = df_vagas.loc[df_vagas.vaga == 'cientista de dados']
df_ED = df_vagas.loc[df_vagas.vaga == 'engenheiro de dados']
df_EML = df_vagas.loc[df_vagas.vaga == 'engenheiro de machine learning']
colunas = ['Local', 'Empresa', 'Descricao','Link']

df_AD.reset_index(drop=True, inplace=True)
df_CD.reset_index(drop=True, inplace=True)
df_ED.reset_index(drop=True, inplace=True)
df_EML.reset_index(drop=True, inplace=True)



##########################

fig1 = px.histogram(df_vagas, x="estado", color="vaga", title=' ', hover_name ='vaga')

#fig1.show()

##########################

fig2 = px.histogram(df_vagas, x="nivel", color="nivel", hover_name ='nivel', facet_col= 'vaga')

##########################

fig3 = px.histogram(df_vagas, x="vaga", color="vaga", hover_name ='vaga')

##########################

# Mapa do Brasil

coordenadas=[]
for lat,lng in zip(df_vagas.latitude,df_vagas.longitude):
  coordenadas.append([lat,lng])

mapa = folium.Map(location=[-15.788497,-47.879873],zoom_start=4,tiles='Stamen Toner')

mapa.add_child(plugins.HeatMap(coordenadas))

####
#title_html = '''
#             <h3 align="center" style="font-size:20px"><b>Heatmap de vagas pelo Brasil</br></br></b></h3>
#             '''
#mapa.get_root().html.add_child(folium.Element(title_html))

#######################
"""
# Create report
pagina1 = dp.Page(
       title="Dashes",
       blocks=[
               "#### Heatmap de Vagas pelo Brasil", 
               dp.Plot(mapa),
               "#### Total Vagas", 
               dp.Plot(fig3),
               "#### Total Vagas por Estado", 
               dp.Plot(fig1),
               "#### Total Vagas por Nível", 
               dp.Plot(fig2)
               ]
     )

pagina2 = dp.Page(
       title="Cientista de Dados",
       blocks=["#### Vagas - Cientista de Dados",
       dp.DataTable(df_CD[colunas], label="Cientista de Dados")]
     )

pagina3 = dp.Page(
       title="Analista de Dados",
       blocks=["#### Vagas Analista de Dados", 
       dp.DataTable(df_AD[colunas], label= "Analista de Dados")]
     )

pagina4 = dp.Page(
       title="Engenheiro de Dados",
       blocks=["#### Vagas - Engenheiro de Dados", 
       dp.DataTable(df_ED[colunas], label = "Engenheiro de Dados")]
     )

pagina5 = dp.Page(
       title ="Engenheiro de Machine Learning",
       blocks=["#### Vagas - Engenheiro de Machine Learning", 
       dp.DataTable(df_EML[colunas], label = "Engenheiro de Machine Learning")]
     )

"""
r = dp.Report(
    dp.Page(
       title="Dashes",
       blocks=[
               "#### Heatmap de Vagas pelo Brasil", 
               dp.Plot(mapa),
               "#### Total Vagas", 
               dp.Plot(fig3),
               "#### Total Vagas por Estado", 
               dp.Plot(fig1),
               "#### Total Vagas por Nível", 
               dp.Plot(fig2)
               ]
     ),
    dp.Page(
       title="Cientista de Dados",
       blocks=["#### Vagas - Cientista de Dados",
       dp.DataTable(df_CD[colunas], label="Cientista de Dados")]
     ),
    dp.Page(
       title="Analista de Dados",
       blocks=["#### Vagas Analista de Dados", 
       dp.DataTable(df_AD[colunas], label= "Analista de Dados")]
     ),
    dp.Page(
       title="Engenheiro de Dados",
       blocks=["#### Vagas - Engenheiro de Dados", 
       dp.DataTable(df_ED[colunas], label = "Engenheiro de Dados")]
     ),
    dp.Page(
       title="Engenheiro de Machine Learning",
       blocks=["#### Vagas - Engenheiro de Machine Learning", 
       dp.DataTable(df_EML[colunas], label = "Engenheiro de Machine Learning")]
     )
    )
      
#r
# Publish
#r.upload(name=f'Vagas em Data Science', open = True, description='Vagas ---> Cientista de Dados, Analista de Dados, Engenheiro de Dados e Engenheiro de Machine Learning')

dp.Report(
  dp.Page(
       title="Dashes",
       blocks=[
               "#### Heatmap de Vagas pelo Brasil", 
               dp.Plot(mapa),
               "#### Total Vagas", 
               dp.Plot(fig3),
               "#### Total Vagas por Estado", 
               dp.Plot(fig1),
               "#### Total Vagas por Nível", 
               dp.Plot(fig2)
               ]
  )
    ).upload(name='TESTE')
