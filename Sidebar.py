import load_df as ld
import streamlit as st
import plotly.express as px
from datetime import datetime
import func_planejamento as fc
def sidebar(df):
    # =============================================================================
    # Layout barra Lateral
    # =============================================================================
    img = 'https://i.pinimg.com/474x/fe/c3/85/fec385ea64ab8effe99de3bb9adcc31c.jpg'
    st.sidebar.image(img, width=200)
    st.sidebar.markdown('# Cury Company')
    st.sidebar.markdown('## Fastest Delivery in Town')
    st.sidebar.markdown('''---''')
    st.sidebar.markdown('## Selecione uma data limite')
    date_slider = st.sidebar.slider(
        'Deslize',
        value=datetime(2022, 4, 13),
        min_value=datetime(2022, 2, 11),
        max_value=datetime(2022, 4, 6),
        format = 'DD-MM-YYYY')
        
    #st.header(date_slider)
    
    st.sidebar.markdown('''---''')
    traffic_options = st.sidebar.multiselect(
        'Quais as condições do trânsito?',
        ['Low', 'Medium', 'High', 'Jam'],
        default = ['Low', 'Medium', 'High', 'Jam'])
    st.sidebar.markdown('''---''')
    st.sidebar.markdown('''### Powered by RaelSan''')
    
    #Filtro de data
    linhas_selecionadas = df['Order_Date'] < date_slider
    df = df.loc[linhas_selecionadas,:]
    
    #Filtro de transito
    linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
    df = df.loc[linhas_selecionadas,:]
    #st.dataframe(df.head())
    
    return df