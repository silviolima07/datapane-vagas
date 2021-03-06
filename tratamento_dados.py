# -*- coding: utf-8 -*-
import pandas as pd
import re
import numpy as np

def remove_accents(coluna):
    text=[]
    for name in coluna:
        #print(name)
        name = name.lower()
        #print(name)
        name = re.sub('ç','c', name)
        name = re.sub('á','a', name)
        name = re.sub('é','e', name)
        name = re.sub('í','i', name)
        name = re.sub('ó','o', name)
        name = re.sub('ú','u', name)
        name = re.sub('ý','y', name)
        name = re.sub('à','a', name)
        name = re.sub('è','e', name)
        name = re.sub('ì','i', name)
        name = re.sub('ò','o', name)
        name = re.sub('ù','u', name)
        name = re.sub('ä','a', name)
        name = re.sub('ë','e', name)
        name = re.sub('ï','i', name)
        name = re.sub('ö','o', name)
        name = re.sub('ü','u', name)
        name = re.sub('ÿ','y', name)
        name = re.sub('â','a', name)
        name = re.sub('ê','e', name)
        name = re.sub('î','i', name)
        name = re.sub('ô','o', name)
        name = re.sub('û','u', name)
        name = re.sub('ã','a', name)
        name = re.sub('õ','o', name)
        name = re.sub('@','a', name)
        #print("Final:", name)
        text.append(name)
    return text

# Carregando arquivo csv
AD = 'CSV/indeed_analista_de_dados.csv'
CD = 'CSV/indeed_cientista_de_dados.csv'
EML = 'CSV/indeed_engenheiro_de_machine_learning.csv'
ED = 'CSV/indeed_engenheiro_de_dados.csv'

cidades = 'cidades.csv'


df_AD = pd.read_csv(AD, encoding="utf8")
df_CD = pd.read_csv(CD, encoding="utf8")
df_EML = pd.read_csv(EML, encoding="utf8")
df_ED = pd.read_csv(ED, encoding="utf8")

df_cidade = pd.read_csv(cidades,  encoding="utf8")

df_cidade['nome']= remove_accents(df_cidade['nome'])
df_cidade['cidade'] = df_cidade['nome']
del df_cidade['nome']

##################################

df_AD

"""### Tratemento no dataset AD"""

df_AD['Cargo'] = remove_accents(df_AD['Cargo'])

temp_A = df_AD.query('Cargo.str.contains("analista de dados")', engine='python') # filtra apenas Analista de dados

temp_de_dados = temp_A[~temp_A.Cargo.str.contains('estágio')] # Exclui estágio
temp_de_dados

df_AD2 = temp_de_dados
temp = np.where(df_AD2.Cargo == 'analista de dados senior', 'senior ', np.where (df_AD2.Cargo == 'analista de dados pleno', 'pleno', np.where(df_AD2.Cargo == 'analista de dados jr 01 vaga', 'junior', np.where(df_AD2.Cargo == "analista de dados", 'senior', np.where(df_AD2.Cargo == 'analista de dados pl', 'pleno', 'senior')))))
df_AD2['nivel'] = temp


df_AD2['Cargo'] = remove_accents(df_AD2['Cargo'])

df_AD2 = df_AD2[df_AD2['Cargo'].str.contains(r'analista de (?!$)')]
df_AD2['vaga'] = 'analista de dados'

#############################

"""### Tratemento no dataset CD


"""

df_CD['Cargo'] = remove_accents(df_CD['Cargo'])

df_CD2 = df_CD[df_CD['Cargo'].str.contains(r'cientista de (?!$)')]
df_CD2['vaga'] = 'cientista de dados'

temp  = np.where(df_CD2.Cargo == 'cientista de dados - senior', 'senior ', np.where (df_CD2.Cargo == 'cientista de dados - pleno', 'pleno', np.where(df_CD2.Cargo == 'cientista de dados jr', 'junior', np.where(df_CD2.Cargo == "cientista de dados", 'senior', np.where(df_CD2.Cargo == "cientista de dados pl", 'pleno', np.where(df_CD2.Cargo == "cientista de dados - pl", 'pleno', 'senior'))))))
df_CD2['nivel'] = temp

"""### Tratemento no dataset EML"""

df_EML['Cargo'] = remove_accents(df_EML['Cargo'])

df_EML2 = df_EML[df_EML['Cargo'].str.contains(r'de machine learning')]

df_EML2['vaga'] = 'engenheiro de machine learning'
df_EML2['nivel'] = 'sem informacao'

"""### Tratemento no dataset ED"""

df_ED['Cargo'] = remove_accents(df_ED['Cargo'])

df_ED2 = df_ED[df_ED['Cargo'].str.contains(r'engenheiro de dados')]


temp = np.where(df_ED2.Cargo == 'engenheiro de dados senior', 'senior ', 
np.where (df_ED2.Cargo == 'engenheiro de dados pleno', 'pleno', 
np.where(df_ED2.Cargo == 'engenheiro de dados junior', 'junior', 
np.where(df_ED2.Cargo == "engenheiro de dados", 'senior', 'senior'))))

df_ED2['nivel'] = temp


df_ED2['vaga'] = 'engenheiro de dados'

"""### Concatenando os dataset verticalmente, coluna encima de coluna"""

df = pd.concat([df_AD2, df_CD2, df_EML2, df_ED2], axis=0)

local_remoto = df.Local.replace('remoto', 'remoto,remoto')

df2 = df.copy()
df2['Local'] = local_remoto

df3 = df2.copy()
local_brasil = df3.Local.replace('brasil', 'remoto,remoto')
df3['Local'] = local_brasil

df3[['cidade','estado']] = df3.Local.str.split(',', n=1, expand=True)


df3['cidade']= remove_accents(df3['cidade'])

df3 = pd.merge(df3, df_cidade, on = 'cidade')


df3.to_csv("vagas-ds.csv", columns = ['Cargo', 'Local', 'Empresa', 'Descricao', 'Link', 'nivel', 'vaga',
       'cidade', 'estado', 'latitude', 'longitude'],index=False)
