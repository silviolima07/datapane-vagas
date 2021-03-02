# -*- coding: utf-8 -*-
"""Indeed.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JqZpsfWao6rTKD09rgUp_iNEduXf-9v0
"""

#from IPython.display import Javascript

#def window_open(url):
#    display(Javascript('window.open("{url}");'.format(url=url)))


#window_open('https://datapane.com/home')

#!pip3 install datapane

#token = input('Insert your token after signing in Datapane ')
#print('Your token is', token)

#!datapane login --server=https://datapane.com/ --token=$token

#import logging

# ===== START LOGGER =====
#logger = logging.getLogger(__name__)

#root_logger = logging.getLogger()
#root_logger.setLevel(logging.INFO)
#sh = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#sh.setFormatter(formatter)
#root_logger.addHandler(sh)

import altair as alt
import pandas as pd
import datapane as dp
from datetime import date

import seaborn as sns
sns.set_theme(style="darkgrid")

import plotly.express as px

# Sign-in with your unique token
dp.login(token="429c0773e39cc7b0a0a2aa7ed74e85edeea6d7b5")



cidades = pd.read_csv("cidades.csv")
df_vagas = pd.read_csv("vagas-ds.csv")


fig = px.histogram(df_vagas, x="estado", color="vaga", title='Total Vagas', hover_name ='vaga')

from folium import plugins
import folium

coordenadas=[]
for lat,lng in zip(df_vagas.latitude,df_vagas.longitude):
  coordenadas.append([lat,lng])

mapa = folium.Map(location=[-15.788497,-47.879873],zoom_start=4,tiles='Stamen Toner')

mapa.add_child(plugins.HeatMap(coordenadas))

####
title_html = '''
             <h3 align="center" style="font-size:30px"><b>Heatmap de vagas</br></br></b></h3>
             '''
mapa.get_root().html.add_child(folium.Element(title_html))

mapa

# Create report
r = dp.Report(
    f'## Total Vagas por Estado',
    f'#### - Analista de Dados, Cientista de Dados',
    f'#### - Engenheiro de Machine Learning e Engenheiro de Dados',
    dp.Plot(fig),
    dp.Plot(mapa),

)

# Publish
r.publish(name=f'Vagas em Data Science', open=True, description=f'Vagas anunciadas no indeed.com')