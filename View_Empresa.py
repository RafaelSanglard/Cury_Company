import Sidebar as sb
import streamlit as st
import plotly.express as px
from datetime import datetime
import func_planejamento as fc

def View_Empresa(df):
    #visão empresa

    
    # =============================================================================
    #Layout no streamlit
    
    
    st.header('Marketplace - Visão Empresa')
    df=sb.sidebar(df)
    
    # Define the tab labels
    tab_labels = ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica']
    
    # Create a selectbox to choose the tab
    selected_tab = st.selectbox('Selecione a visão:', tab_labels)
    st.markdown('''---''')

    # Define the content for each tab
    if selected_tab == 'Visão Gerencial':
        print("Visão Gerencial selected")
        fc.gerar_gerencial_empresa(df)
    
    elif selected_tab == 'Visão Tática':
        print("Visão Tática selected")
        fc.gerar_tatica_empresa(df)
    
    elif selected_tab == 'Visão Geográfica':
        print("Visão Geográfica selected")
        fc.gerar_geo_empresa(df)