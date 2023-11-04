import Sidebar as sb
import streamlit as st
import plotly.express as px
from datetime import datetime
import func_planejamento as fc

def View_Restaurante(df):
    
    # =============================================================================
    #Layout no streamlit
    
    
    st.header('Marketplace - Visão Restaurante')
    df=sb.sidebar(df)
    
    st.markdown('''---''')
    # Define the tab labels
    tab_labels = ['Métricas gerais', 'Desvio padrão', 'Tempo médio e desvio padrão por tipo']
    
    # Create a selectbox to choose the tab
    selected_tab = st.selectbox('Selecione a visão:', tab_labels)
    
    # Define the content for each tab
    if selected_tab == 'Métricas gerais':
        fc.metrica_geral_restaurante(df)
    
    elif selected_tab == 'Desvio padrão':
        fc.metrica_avaliacao_restaurante(df)
    
    elif selected_tab == 'Tempo médio e desvio padrão por tipo':
        fc.metrica_tempo_delivery(df)