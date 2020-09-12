import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
from streamlit_folium import folium_static
import folium

# Importando valores utilizados nos mapas e gráficos
df = gpd.read_file('C:/Users/USUARIO/Documents/DAG/Trabalhofinal/base_dados.geojson')
valores = pd.DataFrame(df['BAIRRO_CIDADAO'].value_counts())
valores = valores.reset_index()
valores.columns = ['bairros', 'counts']
bairros = gpd.read_file('C:/Users/USUARIO/Documents/DAG/Trabalhofinal/bairros.geojson')

# Menu lateral
st.sidebar.title('Páginas')
option = st.sidebar.selectbox('Selecione a opção desejada', ['Início', 'Estudo de caso', 'Mapas Gerais', 'Mapas '
                                                                                                         'Temáticos'])
dados = gpd.read_file('C:/Users/USUARIO/Documents/DAG/Trabalhofinal/bairros.geojson')
style = {'fillColor': '#0000FF',
         'color': '#556B2F'}
layer_bairros = folium.GeoJson(
    dados,
    name='Bairros_1',
    tooltip=folium.GeoJsonTooltip(fields=['NOME', 'FONTE']),
    style_function=lambda x: style)

if option == 'Início':
    # Página inicial
    st.header('Bem vindo ao Mapas Curitiba!')
    st.write('Navegue pela plataforma e veja mapas interativos')
    st.write("Descrever a plataforma")
    st.write('Área de abrangência')
    m = folium.Map(location=[-25.5, -49.3],
                   tiles='OpenStreetMap',
                   zoom_start=10
                   )
    layer_bairros.add_to(m)
    # Renderizar mapa no streamlit
    folium_static(m)

if option == 'Estudo de caso':
    st.subheader('Mapas de situação, para chamados do 156 de Curitiba')
    st.write('**Bairros com quantidade de solicitações pelo 156**')
    botao = st.selectbox('Selecione o modelo do mapa', ['Selecione', 'Escuro', 'OpenStreetMap', 'Terreno'])
    if botao == 'Selecione':
        st.write('**-**')
    if botao == 'Escuro':
        fig = px.choropleth_mapbox(valores, geojson=bairros, color="counts",
                                   locations="bairros", featureidkey='properties.NOME',
                                   center={"lat": -25.4284, "lon": -49.2733},
                                   mapbox_style="carto-darkmatter", zoom=9)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.write(fig)

    if botao == 'OpenStreetMap':
        fig = px.choropleth_mapbox(valores, geojson=bairros, color="counts",
                                   locations="bairros", featureidkey='properties.NOME',
                                   center={"lat": -25.4284, "lon": -49.2733},
                                   mapbox_style="open-street-map", zoom=9)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.write(fig)

    if botao == 'Terreno':
        fig = px.choropleth_mapbox(valores, geojson=bairros, color="counts",
                                   locations="bairros", featureidkey='properties.NOME',
                                   center={"lat": -25.4284, "lon": -49.2733},
                                   mapbox_style="stamen-terrain", zoom=9)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.write(fig)

if option == 'Mapas Gerais':
    tipo = st.sidebar.selectbox('Selecione o estudo de caso', ['Ocupação Irregular', 'Equipamentos Urbanos'])
    if tipo == 'Ocupação Irregular':
        st.header('Estudo de ocupações irregulares em Curitiba')
        st.subheader('Estudo de ocupações irregulares em Curitiba')
        style = {'fillColor': '#FF0000',
                 'color': '#660000'}
        oc_irr = gpd.read_file('C:/Users/USUARIO/Documents/DAG/Trabalhofinal/oc_irr.geojson')
        m = folium.Map(location=[-25.5, -49.3],
                       tiles='OpenStreetMap',
                       zoom_start=10
                       )
        folium.GeoJson(
            oc_irr,
            name='Ocupação Irregular',
            tooltip=folium.GeoJsonTooltip(fields=['NOME', 'FONTE']),
            style_function=lambda x: style).add_to(m)
        folium.LayerControl().add_to(m)
        # Renderizar mapa no streamlit
        folium_static(m)

    if tipo == 'Equipamentos Urbanos':
        st.header('Mapas de equipamentos urbanos')
        st.write('**Localização das Escolas Municipais de Curitiba**')
        esc_munic = st.checkbox('Exibir mapa de escolas municipais')
        if esc_munic == 1:
            escola_munic = gpd.read_file('C:/Users/USUARIO/Documents/DAG/Trabalhofinal/escola_munic.geojson')
            m = folium.Map(location=[-25.5, -49.3],
                           tiles='OpenStreetMap',
                           zoom_start=14
                           )
            folium.GeoJson(
                escola_munic,
                name='Escolas Municipais',
                tooltip=folium.GeoJsonTooltip(fields=['NOME_COMPL', 'BAIRRO'])
            ).add_to(m)
            folium.LayerControl().add_to(m)
            # Renderizar mapa no streamlit
            folium_static(m)

        st.write('**Localização dos Hospitais de Curitiba**')
        esc_hospitais = st.checkbox('Exibir mapa de hospitais')
        if esc_hospitais == 1:
            hospitais = gpd.read_file('C:/Users/USUARIO/Documents/DAG/Trabalhofinal/hospitais.geojson')
            m = folium.Map(location=[-25.5, -49.3],
                           tiles='OpenStreetMap',
                           zoom_start=14
                           )
            folium.GeoJson(
                hospitais,
                name='Hospitais',
                tooltip=folium.GeoJsonTooltip(fields=['NOME_COMPL', 'BAIRRO'])
            ).add_to(m)
            folium.LayerControl().add_to(m)
            # Renderizar mapa no streamlit
            folium_static(m)

        st.write('**Localização e abrangência das Unidades de Saúde de Curitiba**')
        esc_unitsaude = st.checkbox('Exibir mapa de Unidades de Saúde')
        if esc_unitsaude == 1:
            unidade_saude = gpd.read_file('C:/Users/USUARIO/Documents/DAG/Trabalhofinal/unidade_saude.geojson')
            m = folium.Map(location=[-25.5, -49.3], tiles='OpenStreetMap', zoom_start=12)
            folium.GeoJson(unidade_saude, name='Unidade de Saúde', tooltip=folium.GeoJsonTooltip(fields=['NOME_COMPL', 'BAIRRO'])).add_to(m)
            layer_bairros.add_to(m)
            folium.LayerControl().add_to(m)
            # Renderizar mapa no streamlit
            folium_static(m)
