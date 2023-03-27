# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time  # to simulate a real time data, time loop

import requests
from bs4 import BeautifulSoup
from PIL import Image
import re  
import json as json 
from requests_html import HTMLSession 
from stqdm import stqdm
from datetime import datetime
from datetime import timedelta
from io import BytesIO

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

url_icon = "https://drive.google.com/file/d/1rsobE8pEosOFjGyihHg6tN1oiqZQmwUV/view?usp=sharing"

st.set_page_config(
    page_title="Classement Concours Moovjee",
    page_icon='https://drive.google.com/uc?export=download&id='+url_icon.split('/')[-2],
    layout="wide",
)

st.title("Moovjee Challenge Ranking x Plenumi")

url = "https://drive.google.com/file/d/1BDCO-9eYCRHnZMi9AK2PBD-Y3ZoDWwKm/view?usp=sharing"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]

import urllib.request
from urllib.request import Request, urlopen
from io import StringIO
import pandas as pd
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
content=requests.get(path, headers= headers)
data_test = urlopen(req,timeout=10).read()
pd.read_csv(data_test)
data = pd.read_csv(path)

today = datetime.now().strftime("%m-%d")
if today not in data['date']:
    today = (datetime.now() - timedelta(days = 1)).strftime("%m-%d")
    
data_today = data[data['date'] == today]
data_Plenumi = data[data['title'] == 'PLENUMI (22)']
top_50 = data_today.sort_values(by=['likes'], ascending = False)[['title', 'likes']][0:50]
classement = data_today.sort_values(by=['likes'], ascending = False)[['title', 'likes','views']].reset_index()
classement_Plenumi = classement[classement['title']=='PLENUMI (22)']

histo_classement = []
for date in data['date'].unique():
    data_jour = data[data['date'] == date]
    classement_jour = data_jour.sort_values(by=['likes'], ascending = False)[['title', 'likes','views']].reset_index()
    histo_classement.append(int(classement_jour[classement_jour['title']=='PLENUMI (22)'].index[0]))

url_image = "https://drive.google.com/file/d/13olHPYQsb4r3cF6x-r1vefCCFNPYKLfg/view?usp=sharing"
st.image('https://drive.google.com/uc?export=download&id='+url_image.split('/')[-2])

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Classement de Plenumi:")
    st.write(classement_Plenumi.index[0], " /190")
    diff_hier = histo_classement[-1]-classement_Plenumi.index[0]
    if diff_hier >= 0:
        st.write("(+",diff_hier," places gagnées par rapport à hier)")
    else:
        st.write(diff_hier," places perdues par rapport à hier)")
    st.markdown("#### Nombre de likes:")
    st.write(int(classement_Plenumi['likes']))
    st.markdown("#### Nombre de vues:")
    st.write(int(classement_Plenumi['views']))
    
    st.markdown("## N'oubliez pas d'aller liker la vidéo !! 👍")
    
    
with col2: st.video("https://www.youtube.com/watch?v=O5xTOPv5Dr0")

col3, col_vide, col4 = st.columns([10,2,5])

with col3:

    comparatifs = data_today.sort_values(by=['likes'], ascending = False).iloc[[0,9,19,49,99,(classement[classement['title']=='PLENUMI (22)'].index[0])]]['title']
    data_special_Plenum_Chart = data[(data['title'].isin(comparatifs))]
    data_special_Plenum_Chart['Autre'] = data_special_Plenum_Chart['title'].apply(lambda x: 'PLENUMI' if x == 'PLENUMI (22)' else 'Other')
    rankings = []
    for entreprise in data_special_Plenum_Chart['title']:
      rankings.append(('Top '+str(classement[classement['title']==entreprise].index[0]+1)))
    data_special_Plenum_Chart['rankings']=rankings
    fig_Plenumi = px.line(data_special_Plenum_Chart.sort_values(by=['likes'], ascending = False), x="date", y="likes", symbol = 'rankings' ,color="Autre", hover_data=['title','likes','views','description'], range_x=[-1,20], 
              title = 'Classement de Likes - Plenumi VS les autres', log_y=True, height=500, width = 800, labels={'title':'Projet', 'likes':"Number of Likes"}, color_discrete_sequence=['#A9A9A9','#5F9EA0'])
    st.write(fig_Plenumi)
    

with col4:
    st.markdown("### Classement Général")
    st.write(top_50.reset_index(drop=True))
   

st.markdown("### Details")
fig = px.line(data.sort_values(by=['likes'], ascending = False), x="date", y="likes", color="title", hover_data=['title','likes','views','description'], range_x=[-1,20], 
              title = 'Suivi général du nombre de Likes', log_y=True, height=800, width = 1200, labels={'title':'Projet', 'likes':"Number of Likes"}, markers = True, category_orders={'date':data.sort_values(by=['date'], ascending = True)['date']})
st.write(fig)
    

# streamlit run /Users/nicolasjulien/.spyder-py3/Dashboard_Moovjee.py

# streamlit run /Users/nicolasjulien/.spyder-py3/Dashboard_Moovjee.py
