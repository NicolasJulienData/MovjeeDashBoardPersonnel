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
    page_title="Concours Moovjee Prix 100 jours - Suivi du Classement",
    page_icon='https://drive.google.com/uc?export=download&id='+url_icon.split('/')[-2],
    layout="wide",
)

st.title("Concours Prix Moovjee 100 Jours - Suivi du classement     (Réalisé par @Plenumi)")

url = "https://drive.google.com/file/d/1SuEhd6Rqmm5EJM3qxkUamcfyR08JQozd/view?usp=sharing"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]

import urllib.request
from urllib.request import Request, urlopen
from io import StringIO
import pandas as pd
import requests

storage_options = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
pd.read_csv(path, storage_options=storage_options)
# data = pd.read_csv("output_final.csv")
data = data.dropna()

today = datetime.now().strftime("%m-%d")
if today not in np.array(data['date']):
    today = (datetime.now() - timedelta(days = 1)).strftime("%m-%d")

data_today = data[data['date'] == today]
data_Plenumi = data[data['title'] == 'PLENUMI (22)']
top_50 = data_today.sort_values(by=['likes'], ascending = False)[['title', 'likes']][0:50]
classement = data_today.sort_values(by=['likes'], ascending = False)[['title', 'likes','views']].reset_index()
classement_Plenumi = classement[classement['title']=='PLENUMI (22)']

col1, col2 = st.columns([1,6])  
with col2:
    st.markdown("### A propos de ce Dashboard : ###")
    st.markdown("Bienvenue à toi sur ce Dashboard de suivi du classement du **prix 100 jours de Moovjee** 🏆. Que tu sois porteur de projet, soutien actif ou simple curieux, ce Dashboard te permettra de suivre les performances des projets qui t'intéressent. 📊")
    st.markdown("⚠️ Attention : Les données sont actualisées **manuellement** tous les jours à 12h 🕛, par conséquent les **performances affichées ne sont pas les performances en temps réel**. Le dashboard n'est pas supporté par Safari 🧭❌. Pour toute suggestion, remarque, problème, question, n'hésite pas à me contacter : nicolas.julien@essec.edu")
with col1:
    from streamlit_lottie import st_lottie
    from streamlit_lottie import st_lottie_spinner
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    lottie_url_download = "https://assets8.lottiefiles.com/packages/lf20_cv6rdeii.json"
    lottie_download = load_lottieurl(lottie_url_download)
    st_lottie(lottie_download)
    
col3, col_vide, col4 = st.columns([3,1,8])

with col3:
    url_image = "https://drive.google.com/file/d/13olHPYQsb4r3cF6x-r1vefCCFNPYKLfg/view?usp=sharing"
    st.image('https://drive.google.com/uc?export=download&id='+url_image.split('/')[-2], width = 270)
    st.markdown("Si vous aimez ce Dashboard et le projet Plenumi, n'oubliez pas d'aller liker notre vidéo pour nous soutenir 👍 ! Merci pour votre soutien ❤️")
    st.video("https://www.youtube.com/watch?v=O5xTOPv5Dr0")
                
with col4:
    st.markdown("")
    st.markdown("### A propos de Plenumi : ###") 
    st.markdown("*Pourquoi ce Dashboard ?* - Nous te partageons ce Dashboard afin de te montrer que **les données peuvent aider à gagner en motivation et encourager la mise en action**. 💪 Nous pensons que pouvoir analyser et comparer les performances des projets aidera la communauté Moovjee à se mobiliser et permettra de faire grandir l'engouement autour du concours 🚀. Mais nous pensons également que **se servir des données pour générer un impact positif** est possible dans pleins d'autres cadres, notamment celui de **l'éducation**, afin de motiver non pas des porteurs de projets mais des élèves 🎓.")
    st.markdown("*C'est quoi Plenumi ?* - **Plenumi** est une plateforme de révisions en ligne qui utilise les différentes avancées en innovation pédagogique ainsi qu’en *data science* pour **fournir un suivi personnalisé et qualitatif à chaque élève**💡.  En centralisant le travail et les données de l’élève, il est possible d’activer des **leviers de progression**, lui permettant d'avoir un apprentissage **pertinent, ludique et motivant**📚.")
    st.markdown("**Suivre le projet :** https://plenumi.fr")
    st.markdown("**Nous contacter :** contact@plenumi.fr")
    st.markdown("**Soutiens nous et va liker notre vidéo Youtube :** https://www.youtube.com/watch?v=O5xTOPv5Dr0")

projet = 'PLENUMI (22)'
col5, col6, col7 = st.columns(3)
with col6:
    st.markdown("### - Suivre mon projet -") 
    projet = st.selectbox('Nom du projet:', np.sort(data['title'].unique()), index=int(np.where(np.sort(data['title'].unique())=='PLENUMI (22)')[0]))
    
classement_projet = classement[classement['title']==projet]

histo_classement = []
for date in data['date'].unique():
    data_jour = data[data['date'] == date]
    classement_jour = data_jour.sort_values(by=['likes'], ascending = False)[['title', 'likes','views']].reset_index()
    if classement_jour[classement_jour['title']==projet].index != None:
        histo_classement.append(int(classement_jour[classement_jour['title']==projet].index[0]))
top_15_likes = int(data_today.sort_values(by=['likes'], ascending = False).iloc[14]['likes'])
             
col8, col9 = st.columns([1,3])

with col8:
    st.markdown("#### Classement:")
    if classement_projet.index != None:
        st.write((classement_projet.index[0]+1), " /190")
    diff_hier = histo_classement[-2]-histo_classement[-1]
    if diff_hier >= 0:
        st.write("(+",diff_hier," places gagnées par rapport à hier)")
    else:
        st.write(-diff_hier," places perdues par rapport à hier")
    st.markdown("#### Nombre de likes:")
    if len(classement_projet['likes']) != 0 :
        st.write(int(classement_projet['likes']))
        delta_likes = top_15_likes-int(classement_projet['likes'])
        if delta_likes > 0:
            st.write(delta_likes," likes manquants pour être qualifié")
        else:
            st.write(-delta_likes," likes d'avance pour rester qualifié")
        st.markdown("#### Nombre de vues:")
        st.write(int(classement_projet['views']))

    with col9:
        comparatifs = data_today.sort_values(by=['likes'], ascending = False).iloc[[0,14,24,49,99,(classement[classement['title']==projet].index[0])]]['title']
        top_15 = data_today.sort_values(by=['likes'], ascending = False).iloc[14]['title']
        data_special_projet_Chart = data[(data['title'].isin(comparatifs))]
        data_special_projet_Chart['Informations'] = data_special_projet_Chart['title'].apply(lambda x: x[:-5] if x == projet else ('Premier admis' if x == top_15 else ''))
        rankings = []
        for entreprise in data_special_projet_Chart['title']:
          rankings.append(('Top '+str(classement[classement['title']==entreprise].index[0]+1)))
        data_special_projet_Chart['rankings']=rankings
        data_special_projet_Chart['date'] = data_special_projet_Chart['date'].apply(lambda x: x+'-2023')
        fig_projet = px.line(data_special_projet_Chart.sort_values(by=['likes'], ascending = False), x="date", y="likes", symbol = 'rankings' ,color="Informations", hover_data=['title','likes','views','description'], range_x=[-1,15], 
                  title = 'Classement de Likes - {} VS les autres'.format(projet), log_y=True, height=500, width = 800, labels={'title':'Projet', 'likes':"Number of Likes"}, color_discrete_map = {projet[:-5]:'#5F9EA0','Premier admis':'#9ACD32','':'#A9A9A9'}, 
                             category_orders={'date':data_special_projet_Chart.sort_values(by=['date'], ascending = True)['date']})
        st.write(fig_projet)   
    
col10, col11, col12 = st.columns(3)
with col11:
    st.markdown("### - Classement Général -") 
    top = st.slider("Afficher le Top...", min_value=0, max_value=190, value=15) 
    
col13, col14 = st.columns([1,3])
with col13:
    top_data = data_today.sort_values(by=['likes'], ascending = False)[['title', 'likes']][0:top+1]
    st.markdown("**Classement Général**")
    classement_general = top_data.reset_index(drop=True)
    classement_general['Classement']= range(len(top_data)+1)[1:]
    classement_general = classement_general.rename(columns={"title": "Projet"})
    st.write(classement_general.set_index('Classement'))
  
with col14:
    data_graph = data.sort_values(by=['likes'], ascending = False)
    data_graph = data_graph[np.isin(data_graph['title'],top_data['title'])]
    data_graph['date'] = data_graph['date'].apply(lambda x: x+'-2023')
    fig = px.line(data_graph, x="date", y="likes", color="title", hover_data=['title','likes','views','description'], range_x=[-1,15],
              title = 'Suivi général du nombre de Likes', log_y=False, height=650, width = 1050, labels={'title':'Projet', 'likes':"Number of Likes"}, markers = True, category_orders={'date':data_graph.sort_values(by=['date'], ascending = True)['date']})
    st.write(fig)

                    
                    
                    
                    
                    
#col3, col_vide, col4 = st.columns([10,2,5])

#with col3:

    #comparatifs = data_today.sort_values(by=['likes'], ascending = False).iloc[[0,9,19,49,99,(classement[classement['title']=='PLENUMI (22)'].index[0])]]['title']
    #data_special_Plenum_Chart = data[(data['title'].isin(comparatifs))]
    #data_special_Plenum_Chart['Autre'] = data_special_Plenum_Chart['title'].apply(lambda x: 'PLENUMI' if x == 'PLENUMI (22)' else 'Other')
    #rankings = []
    #for entreprise in data_special_Plenum_Chart['title']:
      #rankings.append(('Top '+str(classement[classement['title']==entreprise].index[0]+1)))
    #data_special_Plenum_Chart['rankings']=rankings
    #fig_Plenumi = px.line(data_special_Plenum_Chart.sort_values(by=['likes'], ascending = False), x="date", y="likes", symbol = 'rankings' ,color="Autre", hover_data=['title','likes','views','description'],
             # title = 'Classement de Likes - Plenumi VS les autres', log_y=True, height=500, width = 800, labels={'title':'Projet', 'likes':"Number of Likes"}, color_discrete_sequence=['#A9A9A9','#5F9EA0'], 
                        # category_orders={'date':data.sort_values(by=['date'], ascending = True)['date']})
   # st.write(fig_Plenumi)
    

#with col4:
  #  st.markdown("### Classement Général")
 #   st.write(top_50.reset_index(drop=True))
   

#st.markdown("### Details")
#fig = px.line(data.sort_values(by=['likes'], ascending = False), x="date", y="likes", color="title", hover_data=['title','likes','views','description'], range_x=[-1,20], 
      #        title = 'Suivi général du nombre de Likes', log_y=True, height=600, width = 900, labels={'title':'Projet', 'likes':"Number of Likes"}, markers = True, category_orders={'date':data.sort_values(by=['date'], ascending = True)['date']})
#st.write(fig)
    

# streamlit run /Users/nicolasjulien/.spyder-py3/Dashboard_Moovjee.py

# streamlit run /Users/nicolasjulien/.spyder-py3/Dashboard_Moovjee.py
