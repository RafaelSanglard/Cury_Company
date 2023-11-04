import re
import os
import folium
import haversine
import pandas as pd
import streamlit as st
import plotly.express as px
import func_planejamento as fc
from datetime import datetime
from streamlit_folium import folium_static

#!pip install streamlit
#!pip install folium
#pip install haversine
#pip install streamlit-folium
def load_df():    
    #Load the content from a .csv file located on my github
    url = 'https://raw.githubusercontent.com/RafaelSanglard/4POA/main/train.csv'
    df_raw = pd.read_csv(url)
    df_raw.head()
    
    
    #Fcreate a copy for preserve the original cvs
    df = df_raw.copy()
    
    
    #remove empty spaces from the string using .strip()    
    df['City'] = df['City'].apply(str.strip)
    df['Delivery_person_ID'] = df['Delivery_person_ID'].apply(str.strip)
    df['Festival'] = df['Festival'].str.strip()
    df['ID'] = df['ID'].apply(str.strip)
    df['Road_traffic_density'] = df['Road_traffic_density'].str.strip()
    df['Type_of_order'] = df['Type_of_order'].str.strip()
    df['Type_of_vehicle'] = df['Type_of_vehicle'].str.strip()
    df['Weatherconditions'] = df['Weatherconditions'].str.strip()
    # Clean the 'Time_taken(min)' column by replacing non-numeric characters with an empty string
    df['Time_taken(min)'] = df['Time_taken(min)'].str.replace(r'\D', '', regex=True)
    
    #Converting type, string to int/float
    df['Delivery_person_Age'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce').astype('Int64')
    
    
    #strings to decimal
    df['Delivery_person_Ratings'] = df ['Delivery_person_Ratings'].astype(float)
    df['Time_taken(min)'] = df['Time_taken(min)'].astype(float)
    
    
    #String to date
    df['Order_Date'] = pd.to_datetime(df ['Order_Date'],format='%d-%m-%Y')
    
    #excluding lines with values 'NaN
    # conditional selection
    # pd.notna()
    linhas_selecionadas = (df['City'] != 'NaN')
    df = df.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df['Delivery_person_Age'] != 'NaN')
    df = df.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df['Festival'] != 'NaN')
    df = df.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df['ID'] != 'NaN ')
    df = df.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df['Road_traffic_density'] != 'NaN')
    df = df.loc[linhas_selecionadas, :].copy()
    
    #df['multiple_deliveries'] = df['multiple_deliveries'].astype(int)
    df['multiple_deliveries'] = pd.to_numeric(df['multiple_deliveries'], errors='coerce')
    
    linhas_selecionadas = (df['Type_of_order'] != 'NaN ')
    df = df.loc[linhas_selecionadas, :].copy()
    linhas_selecionadas = (df['Type_of_vehicle'] != 'NaN ')
    df = df.loc[linhas_selecionadas, :].copy()
    
    # Remove trailing spaces and replace 'NaN' with NaN
    linhas_selecionadas1 = (df['Weatherconditions'] != 'NaN')
    df = df.loc[linhas_selecionadas1, :].copy()
    
    return df