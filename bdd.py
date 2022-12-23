import builtins
import pandas as pd 
import sqlalchemy
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import sqlite3
import json
from folium.plugins import HeatMap
import streamlit_folium as stf


tab1,tab2,tab3,tab4 = st.tabs(["Question1 ","Question2 ","Question3 ","Question4"])


# Créer une connexion à la base de données
engine = sqlalchemy.create_engine('sqlite:///db.sqlite')





with tab1:
# Récupérer les données à partir de la base de données
    df = pd.read_sql_query("SELECT date, objet FROM PerteObjet", engine)
    df['date'] = pd.to_datetime(df['date']) - pd.to_timedelta(7, unit='d')

    # Extraire l'année des dates
    df['annee'] = pd.DatetimeIndex(df['date']).year

    # Filtrer les données entre 2016 et 2021
    df_filtre = df[(df['annee'] >= 2016) & (df['annee'] <= 2021)]

    # Calculer le nombre d'objets perdus par semaine
    df_objet_semaine = df_filtre.groupby(pd.Grouper(key='date', freq='W'))['objet'].count()

    df_objet_semaine_type=pd.DataFrame(df_filtre.groupby([pd.Grouper(key='date', freq='W'),"objet"]).count().reset_index().set_index('date'))


    # Afficher le résultat
    #dfObjetPerdu = df_filtre.groupby(pd.Grouper(key='date', freq='W'))['objet_perdu_semaine'].count()
    st.bar_chart(df_objet_semaine)

with tab2:
    listTypeObjet = df_filtre['objet'].unique()

    st.subheader("ObjetPerdu")
    filter_byTypeObject = st.selectbox("TypeObjet" , listTypeObjet)
    # df_filtre_type = df_filtre[df_filtre['objet'].isin(filter_byGenre)]

    #fig,ax = plt.subplots()
    # ax.hist(df_filtre_type.groupby(pd.Grouper(key='date', freq='W'))['objet_perdu_semaine'].count(),bins = 20)
    # st.pyplot(fig)
    #st.dataframe(df_objet_semaine_type)

    st.line_chart(df_objet_semaine_type[df_objet_semaine_type["objet"]==filter_byTypeObject]['annee'])





with tab3:
    db_string = "sqlite:///db.sqlite"
    db = sqlalchemy.create_engine(db_string)

    #ajouter les données de la table Gare
    gare_df = pd.read_sql_table("Gare",db)

    #ajouter les données de la table PerteObjet
    perte_df = pd.read_sql_table("PerteObjet",db)

    #ajouter les données de la table Frequentation
    frequ_df = pd.read_sql_table("Frequentation",db)

    #fusionner les tables
    df = pd.merge(gare_df,perte_df,on="code_uic")
    df = pd.merge(df,frequ_df,on="code_uic")

    #créer une fonction pour afficher la carte


    def afficher_carte(year,type):
        #filtrer les données par année et type
        df_filtre = df.loc[(df["date"].str.contains(year)) & (df["objet"] == type)]
        #ajouter le nombre d'objets a la table gare
    
    
        df_filtre_gare = df_filtre.groupby("region")["objet"].count().reset_index()
        #st.dataframe(df_filtre_gare)
        
        
        df_filtre_gare = pd.merge(gare_df,df_filtre_gare,left_on="region",right_on="region").drop_duplicates(['region'])
        #df_filtre_gare = pd.merge(gare_df,df_filtre_gare,on=['region','code_uic']).drop_duplicates(['region','code_uic'])

        anciennes_regions = {"REGION BOURGOGNE FRANCHE-COMTE": "Bourgogne-Franche-Comté",
                        "REGION CENTRE" : "Centre-Val de Loire",
                        "REGION CHAMPAGNE-ARDENNE": "Grand Est",
                        "REGION LORRAINE": "Grand Est",
                        "REGION ALSACE":"Grand Est",
                        "REGION PICARDIE": "Hauts-de-France",
                        "REGION NORD PAS DE CALAIS": "Hauts-de-France",
                        "REGION DE PARIS RIVE GAUCHE": "\u00cele-de-France",
                        "REGION DE PARIS SAINT-LAZARE": "\u00cele-de-France",
                        "REGION DE PARIS-EST": "\u00cele-de-France",
                        "REGION DE PARIS-NORD":"\u00cele-de-France",
                        "REGION DE PARIS-SUD-EST":"\u00cele-de-France",
                        "REGION NORMANDIE": "Normandie",
                        "REGION POITOU-CHARENTES AQUITAINE": "Nouvelle-Aquitaine",
                        "REGION LIMOUSIN":"Nouvelle-Aquitaine",
                        "REGION LANGUEDOC-ROUSSILLON": "Occitanie",
                        "REGION MIDI PYRENEES":"Occitanie",
                        "REGION PAYS DE LA LOIRE": "Pays de la Loire",
                        "REGION PROVENCE ALPES COTE D'AZUR": "Provence-Alpes-Côte d'Azur",
                        "REGION ALPES": "Provence-Alpes-Côte d'Azur",
                        "REGION AUVERGNE": "Auvergne-Rhône-Alpes",
                        "REGION RHONE-ALPES": "Auvergne-Rhône-Alpes",
                        "REGION BRETAGNE":"Bretagne"
                        }
    
        df_filtre_gare = df_filtre_gare.replace(anciennes_regions)
        #st.dataframe(df_filtre_gare)

        df_filtre_voy = frequ_df[["code_uic","nbVoyageur"+str(year)]]
        df_filtre_final = pd.merge(df_filtre_gare,df_filtre_voy,on="code_uic")
        df_filtre_final = df_filtre_gare.groupby("region")["objet"].sum().reset_index()
        #st.dataframe(df_filtre_gare)
        #ajouter le nombre de voyageur a la table gare
        #st.dataframe(df_filtre_final)

        #dfFinal =pd.concat([df_filtre_final,df_filtre_voy])
        #st.dataframe(dfFinal)
        #créer la carte
        carte = folium.Map(location=[46.227638,2.213749], zoom_start=6)
        folium.Choropleth(geo_data="regions.geojson",
                        data=df_filtre_final,
                        columns=["region","objet","nbVoyageur"],
                        key_on="feature.properties.nom",
                        fill_color="YlGn",
                        legend_name="Nombre d'objets perdus en {} par rapport à la fréquentation des voyageurs en {}".format(type,year)).add_to(carte)
        
    
        return carte 

    #créer les widgets
    year = st.selectbox("Choisissez l'année : ",["2016","2017","2018","2019","2020","2021"])
    type = st.selectbox("Choisissez le type d'objet : ",listTypeObjet)

    #afficher la carte

    stf.st_folium(afficher_carte(year,type))

with tab4:
    st.write("youpi")
    db_string = "sqlite:///donnees_sncf.sqlite"
    db = sqlalchemy.create_engine(db_string)

    meteo = pd.read_sql_table("meteo_region",db)

    meteo.columns =["region","tenperature","meteo_station"]

    #st.dataframe(gare)

    

    





