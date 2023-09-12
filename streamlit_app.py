import streamlit as st

#st.write('Este es nuestra WEB LEO!')



import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import folium.plugins as plugins
import time
import random
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import pydeck as pdk
from folium import FeatureGroup, LayerControl, Map, Marker


APP_TITLE = 'Sistema Inteligente para la Gestión del Agua'
APP_SUB_TITLE = 'minaguas.gob.ve'

#path_data_reg ='C://Users//Gateway//Desktop//Cursos Perozo 2023//SIG//proto_streamlite//SIGAv2//data_reg//'
path_data_reg ='//data_reg//'


def display_map_cond_actuales_almacenamiento():
    hoy=datetime.today();
    st.subheader(":blue[Estado de los embalses al ]"+ ' ' + str(hoy.day)+'-'+str(hoy.month)+'-'+str(hoy.year) + " a las " + str(hoy.hour) +':'+str(hoy.minute))

    #map = folium.Map(location=[7.51, -66.44], zoom_start=6, scrollWheelZoom=False, tiles="Stamen Terrain")
    map = folium.Map(location=[7.51, -66.44], zoom_start=6, scrollWheelZoom=False, tiles='stamentoner')

    #Graficar marcadores y nombres de embalses
    data_emb = pd.read_excel(path_data_reg+'embalses.xlsx')
    data_emb = data_emb[data_emb.lat.notnull()].reset_index(drop=True)

    for i in range(0,len(data_emb)):
           marker =folium.Marker(
              location = [data_emb.iloc[i]['lat'], data_emb.iloc[i]['lon']],
              #popup    = data_emb.iloc[i]['nombre_embalse'],
              icon=folium.DivIcon(html=f"""<div style="font-family: courier new; color: blue">{data_emb.iloc[i]['nombre_embalse']}</div>""")
           ).add_to(map)
            # Mostrar flechas
           marker = folium.Marker(
                location=[data_emb.iloc[i]['lat'], data_emb.iloc[i]['lon']],
                popup= data_emb.iloc[i]['nombre_embalse'] + ' ' + '+'+ str( abs( round( data_emb.iloc[i]['lon']*2 ,2)))  + ' Hm3' ,
                icon=folium.Icon(icon="arrow-up" if i>=4 else "arrow-down", prefix='fa',color="red" if i<4 else 'blue'),

            ).add_to(map)

    st_map = st_folium(map, width=700, height=450)



def display_map_and_donuts_por_periodo():
 # seleccionar por fechas VARIACIÓN DE VOLUMEN DE ALMACENAMIENTO
    st.subheader(":blue[Variaciones de Volúmenes en el tiempo]")
    col1, col2 = st.columns((2))
    # Getting the min and max date
    hoy=datetime.today()
    startDate =  datetime.strptime('01-10-2000', '%m-%d-%Y'); endDate   = datetime.strptime(str(hoy.month)+'-'+str(hoy.day)+'-'+str(hoy.year), '%m-%d-%Y')
    with col1:
        date1 = pd.to_datetime(st.date_input("Desde", startDate))
    with col2:
        date2 = pd.to_datetime(st.date_input("Hasta", endDate))
    ## desplegar mapa nacional por periodo
    st.subheader("Nacional")
    col1, col2 = st.columns((2))
    with col1:
        map1   = folium.Map(location=[7.51, -59.4], zoom_start=5, scrollWheelZoom=False,opacity=0.1,tiles="Stamen Terrain")
        #Graficar marcadores y nombres de embalses
        data_emb = pd.read_excel(path_data_reg+'embalses.xlsx')
        data_emb = data_emb[data_emb.lat.notnull()].reset_index(drop=True)
        for i in range(0,len(data_emb)):
               marker =folium.Marker(
                  location = [data_emb.iloc[i]['lat'], data_emb.iloc[i]['lon']],
                  #popup    = data_emb.iloc[i]['nombre_embalse'],
                  icon=folium.DivIcon(html=f"""<div style="font-family: courier new; color: blue">{data_emb.iloc[i]['nombre_embalse']}</div>""")
               ).add_to(map1)
                # Mostrar flechas
               marker = folium.Marker(
                    location=[data_emb.iloc[i]['lat'], data_emb.iloc[i]['lon']],
                    popup= data_emb.iloc[i]['nombre_embalse'] + ' ' + '+'+ str( abs( round( data_emb.iloc[i]['lon']/3 ,1)))  + ' Hm3'+ ' - 8%',
                    icon=folium.Icon(icon="arrow-up" if i<4 else "arrow-down", prefix='fa',color="red" if i>=4 else 'blue'),

                ).add_to(map1)
        st_map = st_folium(map1, width=700, height=450)
    with col2:
        #st.subheader("Region wise Sales")
        df=pd.DataFrame(); df['cambio']=['Aumento', 'Disminución', 'Sin cambio']; df['valor']=[19, 69, 3]
        fig = px.pie(df, values = "valor", names = "cambio", hole = 0.5)
        fig.update_traces(text = df["cambio"], textposition = "outside")
        st.plotly_chart(fig,use_container_width=True)
 # por regiones
    st.subheader("Hidrocapital")
    col1, col2 , col3= st.columns((3))
    with col1:
        map_reg_cap = folium.Map(location=[10.190847, -65.671223], zoom_start=8, scrollWheelZoom=False, tiles="cartodb positron")
        #Graficar marcadores y nombres de embalses
        data_emb = pd.read_excel(path_data_reg+'embalses.xlsx'); data_emb = data_emb[data_emb.lat.notnull()].reset_index(drop=True)
        data_emb_cap =data_emb[data_emb['nombre_hidrologica']=='Hidrocapital']
        for i in range(0,len(data_emb_cap)):
           marker =folium.Marker(
              location = [data_emb_cap.iloc[i]['lat'], data_emb_cap.iloc[i]['lon']],
              icon=folium.DivIcon(html=f"""<div style="font-family: courier new; color: blue">{data_emb_cap.iloc[i]['nombre_embalse']}</div>""")
           ).add_to(map_reg_cap)
            # Mostrar flechas
           marker = folium.Marker(
                location=[data_emb_cap.iloc[i]['lat'], data_emb_cap.iloc[i]['lon']],
                popup= data_emb_cap.iloc[i]['nombre_embalse'] + ' ' + str( abs( round( data_emb_cap.iloc[i]['lon']/2 ,1)))  + ' Hm3'+ ' - 5%',
                icon=folium.Icon(icon="arrow-up" if i>=4 else "arrow-down", prefix='fa',color="red" if i<4 else 'blue'),

            ).add_to(map_reg_cap)
        st_map = st_folium(map_reg_cap, width=700, height=450)

    with col2:
        df_vol =pd.DataFrame(); df_vol['Nombre']=['La Pereza','La Mariposa', 'Taguaza', 'Lagartijo']
        df_vol['Var.Vol(Hm3)']=[-0.3,-0.9,19.8,-11.4];df_vol['%Var.Vol(%)']=[-98.5,-32.3,15.7,-35.4]
        fig = px.bar(df_vol, x = "Nombre", y = "Var.Vol(Hm3)", text = ['{:,.2f} Hm3'.format(x) for x in df_vol['Var.Vol(Hm3)']],
                 template = "seaborn")
        fig.update_layout(title='Variaciones de Vol. (Hm3)')
        st.plotly_chart(fig,use_container_width=True, height = 300)

    with col3:
        fig = px.bar(df_vol, x = "Nombre", y = "%Var.Vol(%)", text = ['{:,.2f} %'.format(x) for x in df_vol['%Var.Vol(%)']],
                 template = "seaborn")
        fig.update_layout(title='Variaciones de Volúmenes (%)')
        st.plotly_chart(fig,use_container_width=True, height = 300)




def display_critical_maps():
    hoy=datetime.today();
    st.subheader(":blue[Condiciones de Embalses al ]"+ ' ' + str(hoy.day)+'-'+str(hoy.month)+'-'+str(hoy.year) + " a las " + str(hoy.hour) +':'+str(hoy.minute))
    map_critical= folium.Map(location=[7.51, -66.44], zoom_start=6, scrollWheelZoom=False, tiles='cartodb positron')
    #marker_cluster = MarkerCluster().add_to(map_critical)
    data_emb = pd.read_excel(path_data_reg+'embalses.xlsx'); data_emb = data_emb[data_emb.lat.notnull()].reset_index(drop=True)
    for i in range(0,len(data_emb)):
        if i<=2:
            color ="green"
            grupo ='Bajo'
        if 2<i<=4:
            color="blue"
            grupo ='Normal Bajo'
        if 4<i<=6:
            color="yellow"
            grupo ='Normal Alto'
        if 6<i<=8:
            color ="red"
            grupo ='Buena'
        if i>8:
            color='black'
            grupo ='Alivio'
        feature_group = folium.FeatureGroup(grupo)
        Marker(
            location=[data_emb.iloc[i]['lat'], data_emb.iloc[i]['lon']],
            icon=plugins.BeautifyIcon(
                             icon="tent",
                             icon_shape="circle",
                             border_color='purple',
                             text_color="#007799",
                             background_color=color)
            ).add_to(feature_group)
        feature_group.add_to(map_critical)

    LayerControl().add_to(map_critical)
    st_map = st_folium(map_critical, width=700, height=450)









# Programa principal##########################################################

def main():
    st.set_page_config(APP_TITLE)
    st.title(" :droplet: Sistema Inteligente para la Gestión del Agua")
    st.markdown(
            """
            <style>
            .sidebar .sidebar-content {
                width: 1000px;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
    st.caption(APP_SUB_TITLE)


    # Sincornizar BD
    if st.sidebar.button('Sincronizar'):
        with st.spinner('Espere mientras se cargan los informes de las hidrologicas...'):
            time.sleep(2)
        t = time.localtime(); current_time = time.strftime("%H:%M:%S", t)
        st.sidebar.success('Ultima sincronización a las ' + current_time)
        st.sidebar.text('Ultima sincronización a las ' + current_time)

    # desplegar opciones de subsistemas
    lista_Subsistema = ['Embalses', 'Obras de captación superficial']
    sub_choice       =  st.sidebar.selectbox('Elemento de Consulta', lista_Subsistema, len(lista_Subsistema)-1)

    if sub_choice == 'Embalses':
        # Desplegar opciones de embalses

        # Custom CSS to set sidebar size

        tipo_reporte_emb = st.sidebar.radio('Estatus de embalses', ['Condiciones actuales de almacenamiento',
                                                                    'Condiciones críticas actuales por Hidrológica',
##                                                                    'Estatus global por fechas',
##                                                                    'Estatus regional por fechas ',
##                                                                    'Resumen almacenamiento por región',
                                                                    'Garantía de abastecimiento global', 'Garantía de abastecimiento por región',
                                                                    'Resumen de Garantía de abastecimiento',
                                                                    ])


        if tipo_reporte_emb == 'Condiciones actuales de almacenamiento':
            display_map_cond_actuales_almacenamiento()
            display_map_and_donuts_por_periodo()

        if tipo_reporte_emb == 'Condiciones críticas actuales por Hidrológica':
            display_critical_maps()




if __name__ == "__main__":
    main()


# Para mostrar ciruclos de color
 ##           folium.Marker(
##                location=[data_emb.iloc[i]['lat'], data_emb.iloc[i]['lon']],
##                icon=plugins.BeautifyIcon(
##                                 icon="tent",
##                                 icon_shape="circle",
##                                 border_color='purple',
##                                 text_color="#007799",
##                                 background_color='yellow')
##           ).add_to(map)




##        with col2:
##            chart_data = pd.DataFrame(
##               np.random.randn(100, 2) / [50, 50] + [37.76, -122.4],
##               columns=['lat', 'lon'])
##
##            st.pydeck_chart(pdk.Deck(
##                map_style=None,
##                initial_view_state=pdk.ViewState(
##                    latitude=37.76,
##                    longitude=-122.4,
##                    zoom=11,
##                    pitch=50,
##                ),
##                layers=[
##                    pdk.Layer(
##                       'HexagonLayer',
##                       data=chart_data,
##                       get_position='[lon, lat]',
##                       radius=200,
##                       elevation_scale=4,
##                       elevation_range=[0, 1000],
##                       pickable=True,
##                       extruded=True,
##                    ),
##                    pdk.Layer(
##                        'ScatterplotLayer',
##                        data=chart_data,
##                        get_position='[lon, lat]',
##                        get_color='[200, 30, 0, 160]',
##                        get_radius=200,
##                    ),
##                ],
##            ))






##    year_list = ['Embalses', 'Obras de captación superficial', 'Obras de captación subterránea']
##    year = st.sidebar.selectbox('Elemento de Consulta', year_list, len(year_list)-1)
##
##    if year == "Embalses":
##        state_name = display_state_filter(df_continental, state_name)
##    ##    #Load Data
##        p='C://Users//alejandro//Desktop//Cursos Perozo 2023//SIG//proto_streamlite//SIGAv2//'
##        df_continental = pd.read_csv(p+'data//AxS-Continental_Full Data_data.csv')
##        df_fraud = pd.read_csv(p+'data//AxS-Fraud Box_Full Data_data.csv')
##        df_median = pd.read_csv(p+'data//AxS-Median Box_Full Data_data.csv')
##        df_loss = pd.read_csv(p+'data//AxS-Losses Box_Full Data_data.csv')
##
##        espera()
##        #Display Filters and Map
##
##        year, quarter = display_time_filters(df_continental)
##        state_name = display_map(df_continental, year, quarter)
##
##        report_type = display_report_type_filter()
##
##        #Display Metrics
##
##        # display grafica de dos curvas
##        #st.subheader(f'{state_name} {report_type} ')
##        st.subheader(f'{state_name} ')
##        df =pd.read_excel ('C://Users//alejandro//Desktop//Cursos Perozo 2023//SIG//proto_streamlite//SIGAv2//niv.xlsx')
##        st.line_chart(df, x="meses", y=["Volumen Actual (Hm3)", "Media 10 años (Hm3)"])
##
##
##        #st.table(df)
##
##        # Para desplegar valores puntuales como texto
##    ##    col1, col2, col3 = st.columns(3)
##    ##    with col1:
##    ##        display_fraud_facts(df_fraud, year, quarter, report_type, state_name, 'State Fraud/Other Count', f'# of {report_type} Reports', string_format='{:,}')
##    ##    with col2:
##    ##        display_fraud_facts(df_median, year, quarter, report_type, state_name, 'Overall Median Losses Qtr', 'Median $ Loss', is_median=True)
##    ##    with col3:
##    ##        display_fraud_facts(df_loss, year, quarter, report_type, state_name, 'Total Losses', 'Total $ Loss')







import json

import requests

url = (
    "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
)
vis1 = json.loads(requests.get(f"{url}/vis1.json").text)
vis2 = json.loads(requests.get(f"{url}/vis2.json").text)
vis3 = json.loads(requests.get(f"{url}/vis3.json").text)


def espera():
    if st.sidebar.button('Sincronizar'):
        with st.sidebar.spinner('Espere mientras se cargan los informes de las hidrologicas...'):
            time.sleep(4)
        t = time.localtime(); current_time = time.strftime("%H:%M:%S", t)

        st.sidebar.success('Ultima sincronización a las ' + current_time)
        st.sidebar.text('Ultima sincronización a las ' + current_time)

    else:
        pass
        #st.write('Ultima sincronización a las ' + current_time')



def display_time_filters(df):

    quarter = st.sidebar.radio('Embalse', ['Embalse1', 'Embalse2', 'Embalse3', 'Embalse4'])
    st.header(f'{year} {quarter}')
    return year, quarter

def display_state_filter(df, state_name):
##    state_list = [''] + list(df['State Name'].unique())
##    state_list.sort()
    state_list =['Variacion de reservas ultimas 24 h', 'Variacion de reservas ultimos 7 dias',
                    'Variacion de reservas ultimo año', 'Comparacion con el año anterior'  ]

    state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    return st.sidebar.selectbox('Tipo de Reporte', state_list, state_index)

def display_report_type_filter():
##    return st.sidebar.radio('Tipo de Report Type', ['Variacion de reservas ultimas 24 h', 'Variacion de reservas ultimos 7 dias',
##                                            'Variacion de reservas ultimo año', 'Comparacion con el año anterior'  ])
    pass



def display_map(df, year, quarter):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]

    map = folium.Map(location=[7.51, -66.44], zoom_start=6, scrollWheelZoom=False, tiles="Stamen Terrain")
     # agregar icon
##    folium.Marker(location=[7.70, -62.80],popup = 'Embalse 1',
##                      icon= folium.Icon(color='blue',
##                      icon_color='yellow',icon = 'cloud').add_child(
##                        folium.Vega(vis2, width=450, height=250)
##                        ),
##                        ).add_to(map)

    folium.Marker( location=[7.70, -62.80],  popup='Embalse 1  Nivel=134 msnm',
                        icon= folium.Icon(color='blue',
                        icon_color='yellow',icon = 'cloud')).add_to(map)

    folium.Marker( location=[7.230, -60.80],  popup='Embalse 2 , Nivel=234 msnm',
                        icon= folium.Icon(color='red',
                        icon_color='yellow',icon = 'cloud')).add_to(map)


##    folium.Marker(
##    location=[7.70, -62.80],
##    popup=folium.Popup(max_width=450).add_child(
##        folium.Vega(vis1, width=350, height=200)
##    ),
##    ).add_to(map)

##    choropleth = folium.Choropleth(
##        geo_data='C://Users//alejandro//Desktop//SIG//proto_streamlite//data//us-state-boundaries.geojson',
##        data=df,
##        columns=('State Name', 'State Total Reports Quarter'),
##        key_on='feature.properties.name',
##        line_opacity=0.8,
##        highlight=True
##    )
##    choropleth.geojson.add_to(map)
##
##    df_indexed = df.set_index('State Name')
##    for feature in choropleth.geojson.data['features']:
##        state_name = feature['properties']['name']
##        feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'State Pop'][0]) if state_name in list(df_indexed.index) else ''
##        feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''
##
##    choropleth.geojson.add_child(
##        folium.features.GeoJsonTooltip(['name', 'population', 'per_100k'], labels=False)
##    )

    st_map = st_folium(map, width=700, height=450)



    state_name = ''
    if st_map['last_active_drawing']:
        state_name = st_map['last_active_drawing']['properties']['name']
    return state_name


def display_fraud_facts(df, year, quarter, report_type, state_name, field, title, string_format='${:,}', is_median=False):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
    df = df[df['Report Type'] == report_type]
    if state_name:
        df = df[df['State Name'] == state_name]
    df.drop_duplicates(inplace=True)
    if is_median:
        total = df[field].sum() / len(df[field]) if len(df) else 0
    else:
        total = df[field].sum()
    st.metric(title, string_format.format(round(total)))

