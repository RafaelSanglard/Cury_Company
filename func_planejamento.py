import re
import os
import folium
import haversine
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
from streamlit_folium import folium_static
from pandas._libs.tslibs.offsets import Week

# =============================================================================
# Funções Layout Empresa
# =============================================================================

# Generate content for the first tab on View_Empresa
def gerar_gerencial_empresa(df):
    # Pedidos por dia
    col= ['Order_Date']
    df_aux = df.groupby('Order_Date').size().reset_index()
    df_aux.columns = ['Order_Date', 'Count']  # Rename the count column
    #usaermos o plotly pra representação grafica
    fig = px.bar(df_aux, x='Order_Date', y='Count',title='Quantidade de pedidos por dia')
    st.plotly_chart(fig, use_container_width = True)

    col1, col2 = st.columns(2,gap='large')
    with col1:
        df_aux = df.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
        df_aux = df_aux.loc[df_aux['Road_traffic_density']!='NaN', : ]
        
        
        df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
        
        fig = px.pie(df_aux, values = 'entregas_perc', names = 'Road_traffic_density', title='Distribuição dos pedidos por tráfego')
        st.plotly_chart(fig, use_container_width=True)

        
        
    with col2:
        df['City'] = df['City'].str.strip()
        df_aux = df.loc[:, ['ID', 'City','Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
        df_aux = df_aux.loc[df_aux['City']!='NaN']
        fig = px.scatter(df_aux, x ='City', y='Road_traffic_density', size = 'ID', color = 'City', title='Volume de pedidos por cidade')
        st.plotly_chart(fig, use_container_width=True)

# Generate content for the second tab on View_Empresa
def gerar_tatica_empresa(df):
    with st.container():
        df['Week_of_year'] = df ['Order_Date'].dt.strftime('%U')
    
        df_aux2 = df.loc[:,['ID','Week_of_year']].groupby('Week_of_year').count().reset_index()
        df_aux2.columns = [ 'Week_of_year','Quantidade']  # Rename the count column
    
        fig=px.line (df_aux2, x = 'Week_of_year',y='Quantidade', title='Quantidade de pedidos por semana')
        st.plotly_chart(fig, use_comtainer_width = True)

    with st.container():
        df_aux01 = df.loc[:, ['ID','Week_of_year']].groupby('Week_of_year').count().reset_index()
        df_aux02 = df.loc[:, ['Delivery_person_ID','Week_of_year']].groupby('Week_of_year').nunique().reset_index()

        df_aux = pd.merge (df_aux01, df_aux02, how = 'inner')
        df_aux['Order_by_deliver'] = df_aux['ID']/df_aux['Delivery_person_ID']
        
        fig = px.line(df_aux, x='Week_of_year', y='Order_by_deliver', title='Quantidade de pedidos por entregador por semana')
        st.plotly_chart(fig, use_comtainer_width = True)



# Generate content for the third tab on View_Empresa
def gerar_geo_empresa(df):
    with st.container():
            df_aux3 = df.loc[:,
            ['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
    
            map = folium.Map(title='Central por tipo de tráfego')
            
            for index, location_info in df_aux3.iterrows():
              folium.Marker([location_info['Delivery_location_latitude'],
                             location_info['Delivery_location_longitude']],
                            popup = location_info[['City','Road_traffic_density']] ).add_to(map)
            
            folium_static(map, width=1024, height=600)

# =============================================================================
# Funções Layout Entregador
# =============================================================================
# Generate content for the first tab on View_Entregador
def metrica_geral_entregador(df):
    with st.container():
        st.title('Metricas gerais')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            st.subheader('Entregador')
            maior_idade = df.loc[:, "Delivery_person_Age"].max()
            col1.metric('A maior idade é:', maior_idade)
            
        with col2:
            st.subheader('Entregador')
            menor_idade = df.loc[:, "Delivery_person_Age"].min()
            col2.metric('A menor idade é:', menor_idade)

        with col3:
            st.subheader('Veiculos')
            melhor_condicao = df.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição:', melhor_condicao)

        with col4:
            st.subheader('Veiculos')
            pior_condicao = df.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição:', pior_condicao)

# Generate content for the second tab on View_Entregador
def metrica_avaliacoes_entregador(df):
    with st.container():
        st.markdown('---')
        st.title('Avaliações')
        col5, col6 = st.columns(2)
        
        with col5:
            st.subheader('Avaliações médias por entregador')
            average_ratings_per_deliver = (df.loc[:,['Delivery_person_Ratings','Delivery_person_ID']]
                                             .groupby('Delivery_person_ID')
                                             .mean()
                                             .reset_index()
                                          )
            st.dataframe(average_ratings_per_deliver)
            
    
        with col6:
            st.subheader('Avaliação média por transito')
            average_ratings_per_traffic = (df.loc[:,['Delivery_person_Ratings','Road_traffic_density']]
                                             .groupby('Road_traffic_density')
                                             .agg({'Delivery_person_Ratings': ['mean', 'std']})
                                          )
            #Trocar nome das colunas
            average_ratings_per_traffic.columns = ['média_delivery','desvio_padrão_delivery']
            average_ratings_per_traffic = average_ratings_per_traffic.reset_index()

            st.dataframe(average_ratings_per_traffic)

                                                   
            
            st.subheader('Avaliação média por clima')  
            avg_std_ratings_by_weather = (df.loc[:,['Delivery_person_Ratings','Weatherconditions']]
                                             .groupby('Weatherconditions')
                                             .agg({'Delivery_person_Ratings': ['mean', 'std']})
                                          )
            avg_std_ratings_by_weather.columns = ['média_delivery','desvio_padrão_delivery']
            avg_std_ratings_by_weather = avg_std_ratings_by_weather.reset_index()
            st.dataframe(avg_std_ratings_by_weather)

# Generate content for the third tab on View_Entregador
def metrica_velocidade_entregador(df):
    with st.container():
        st.markdown('---')
        st.title('Velocidade de entrega')
        col6, col7 = st.columns(2)
        with col6:
            st.subheader('Top entregadores mais rápidos')
            df2 = (df.loc[:,['Delivery_person_ID','City', 'Time_taken(min)']]
                .groupby(['City', 'Delivery_person_ID'])
                .mean()
                .sort_values(by=['City', 'Time_taken(min)'], ascending=[True, True])
                .reset_index()
                  )
            
            df_aux1 = df2.loc[df2['City'] == 'Metropolitian',:].head(10)
            df_aux2 = df2.loc[df2['City'] == 'Semi-Urban',:].head(10)
            df_aux3 = df2.loc[df2['City'] == 'Urban',:].head(10)
            
            df3 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
            st.dataframe(df3)

        with col7:
            st.subheader('Top entregadores mais lentos')   
            df2 = (df.loc[:,['Delivery_person_ID','City', 'Time_taken(min)']]
                .groupby(['City', 'Delivery_person_ID'])
                .mean()
                .sort_values(by=['City', 'Time_taken(min)'], ascending=[True, False])
                .reset_index()
                  )
            
            
            df_aux1 = df2.loc[df2['City'] == 'Metropolitian',:].head(10)
            df_aux2 = df2.loc[df2['City'] == 'Semi-Urban',:].head(10)
            df_aux3 = df2.loc[df2['City'] == 'Urban',:].head(10)
            
            df3 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
            st.dataframe(df3)

# =============================================================================
# Funções Layout Restaurante
# =============================================================================
# Generate content for the first tab on View_Restaurante
def metrica_geral_restaurante(df):
    with st.container():
        st.title('Metricas gerais')
        col1, col2, col3 = st.columns(3, gap='large')
        #Exibe a quantidade de entregadores unicos
        with col1:
            st.subheader('Entregadores únicos')
            delivery_unique = len(df.loc[:,'Delivery_person_ID'].unique())
            col1.metric('Número:', delivery_unique)
        #tempo médio de entrega durante os festivais
        with col2:
            st.subheader('Tempo médio de entrega')
            cols = [ 'Time_taken(min)','Festival']
            df_aux3 = df.loc[:, cols].groupby('Festival').agg({'Time_taken(min)': ['mean','std']})
            
            df_aux3.columns = ['avg_time','std_time']
            df_aux3 = df_aux3.reset_index()
               
            df_aux3 = df_aux3.loc[df_aux3['Festival'] == "Yes",'avg_time']
            df_aux33 = float(df_aux3)
            col2.metric('com Festival:', '{:.2f}'.format(df_aux33))

        with col3:
            st.subheader('Desvio padrão')
            cols = [ 'Time_taken(min)','Festival']
            df_aux3 = df.loc[:, cols].groupby('Festival').agg({'Time_taken(min)': ['mean','std']})
            
            df_aux3.columns = ['avg_time','std_time']
            df_aux3 = df_aux3.reset_index()
               
            df_aux3 = df_aux3.loc[df_aux3['Festival'] == "Yes",'std_time']
            df_aux33 = float(df_aux3)
            col3.metric('com Festival:', '{:.2f}'.format(df_aux33))
             


        st.markdown('''---''')



        col4, col5, col6 = st.columns(3, gap='large')
        #Distancia média entre destino e origem
        with col4:
            st.subheader('Distancia Média')
            cols = ['Delivery_location_latitude','Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df['distance'] = df.loc[:, cols].apply (lambda x: haversine.haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1
                          )
            avg_distance = df['distance'].mean();
            col4.metric('Entre Restaurante e destino','{:.2f}'.format(avg_distance))
        #tempo médio fora dos festivais    
        with col5:
            st.subheader('Tempo médio de entrega')
            cols = [ 'Time_taken(min)','Festival']
            df_aux3 = df.loc[:, cols].groupby('Festival').agg({'Time_taken(min)': ['mean','std']})
            
            df_aux3.columns = ['avg_time','std_time']
            df_aux3 = df_aux3.reset_index()
               
            df_aux3 = df_aux3.loc[df_aux3['Festival'] == "No",'avg_time']
            df_aux33 = float(df_aux3)

            col5.metric('sem Festival:', '{:.2f}'.format(df_aux33))        
        
        with col6:
            st.subheader('Desvio padrão')
            cols = [ 'Time_taken(min)','Festival']
            df_aux3 = df.loc[:, cols].groupby('Festival').agg({'Time_taken(min)': ['mean','std']})
            
            df_aux3.columns = ['avg_time','std_time']
            df_aux3 = df_aux3.reset_index()
               
            df_aux3 = df_aux3.loc[df_aux3['Festival'] == "No",'std_time']
            df_aux33 = float(df_aux3)
            col6.metric('sem Festival:', '{:.2f}'.format(df_aux33))
            
        st.markdown('''---''')
        with st.container():
            st.subheader('O tempo médio e desvio padrão de entrega por cidade')
    
            cols = ['City', 'Time_taken(min)']
            df_aux3 = df.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
            df_aux3.columns = ['City', 'avg_time', 'std_time']
            
            #df_aux3
            
            fig=go.Figure()
            fig.add_trace(go.Bar(
                name='Control',
                x=df_aux3['City'],
                y=df_aux3['avg_time'],
                error_y = dict ( type='data', array = df_aux3['std_time'])
            ))
            
            fig.update_layout(barmode='group')
            st.plotly_chart(fig)
            


# Generate content for the second tab on View_Restaurante
def metrica_avaliacao_restaurante(df):
    with st.container():
        st.subheader('Tempo médio de entrega por cidade:')
        cols = ['Delivery_location_latitude','Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
        df['distance'] = df.loc[:, cols].apply (lambda x:
                                                    haversine.haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                                         (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        avg_distance = df.loc[:,['City','distance']].groupby('City').mean().reset_index()
            
        fig = go.Figure( data = [go.Pie(labels=avg_distance['City'], values = avg_distance['distance'], pull=[0,0.1,0])])
        st.plotly_chart(fig)
        
        st.markdown('''---''')
        st.subheader('O tempo médio e desvio padrão de entrega por cidade')
    
        cols = ['City', 'Time_taken(min)','Road_traffic_density']
        df_aux3 = df.loc[:, cols].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
        df_aux3.columns = ['City','Road_traffic_density', 'avg_time', 'std_time']
        
        fig= px.sunburst(df_aux3, path = ['City', 'Road_traffic_density'], values = 'avg_time',
                         color = 'std_time', color_continuous_scale='RdBu',
                         color_continuous_midpoint=np.average(df_aux3['std_time']))
        st.plotly_chart(fig)
        
# Generate content for the third tab on View_Restaurante
def metrica_tempo_delivery(df):
    st.subheader('O tempo médio e desvio padrão de entrega por cidade e tipo de pedido')

    cols = ['City', 'Time_taken(min)','Type_of_order']
    df_aux3 = df.loc[:, cols].groupby(['City','Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
    df_aux3.columns = ['City','Type_of_order', 'avg_time', 'std_time']

    st.dataframe(df_aux3)

