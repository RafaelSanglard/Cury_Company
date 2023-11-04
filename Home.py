import View_Empresa as V_E
import View_Restaurante as V_R
import View_Entregador as V_EN
import Sidebar as sb
import streamlit as st
import load_df as ld
st.set_page_config(page_title='Cury Delivery', page_icon='📈', layout = 'wide')

df=ld.load_df()



#Menu 
# =============================================================================
#Layout no streamlit
st.subheader('Menu principal')

# Define the tab labels
tab_labels = ['Visão Empresa', 'Visão Entregador','Visão Restaurante']

# Create a selectbox to choose the tab
selected_tab = st.selectbox('Escolha qual player visualizar:', tab_labels)

st.markdown('''---''')
# Define the content for each tab
if selected_tab   == 'Visão Restaurante':
    V_R.View_Restaurante(df)

elif selected_tab == 'Visão Empresa':
    V_E.View_Empresa    (df)

elif selected_tab == 'Visão Entregador':
    V_EN.View_Entregador(df)
