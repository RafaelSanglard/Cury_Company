import load_df as ld
import Sidebar as sb
import streamlit as st
import plotly.express as px
from datetime import datetime
import func_planejamento as fc

def View_Entregador(df):

    
    # =============================================================================
    #Layout no streamlit
    
    
    st.header('Marketplace - Visão Entregador')
    df=sb.sidebar(df)
    
    st.markdown('''---''')
    # Define the tab labels
    tab_labels = ['Métricas gerais', 'Avaliações', 'Velocidade de entrega']
    
    # Create a selectbox to choose the tab
    selected_tab = st.selectbox('Selecione a visão:', tab_labels)
    
    # Define the content for each tab
    if selected_tab == 'Métricas gerais':
        fc.metrica_geral_entregador(df)
    
    elif selected_tab == 'Avaliações':
        fc.metrica_avaliacoes_entregador(df)
    
    elif selected_tab == 'Velocidade de entrega':
        fc.metrica_velocidade_entregador(df)