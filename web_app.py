import streamlit as st
import geopandas as gpd
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image


# Função para plotar os mapas
def plot_map(nome_camada, camada, estilo, campos, ):
    mapa = folium.Map(location=[-25.5, -49.3], tiles='OpenStreetMap', zoom_start=10)
    folium.GeoJson(camada, name=nome_camada, tooltip=folium.GeoJsonTooltip(fields=campos),
                   style_function=lambda x: estilo).add_to(mapa)
    folium.LayerControl().add_to(mapa)
    # Renderizar mapa no streamlit
    return mapa


# importando dados usados em todos mapas
layer_bairros = gpd.read_file('bairros.geojson')
styleBairros = {'fillColor': '##FFCCFF', 'color': '#333333'}
style = {'fillColor': '##FFCCFF', 'color': '#333333'}
fields = ['NOME', 'FONTE']
nome = 'Bairros'
bairros = plot_map(nome, layer_bairros, styleBairros, fields)
image = Image.open('logo.jpeg')


def cont_point_polygon(df_point, polygons):
    pts = df_point.copy()
    pts_in_polys = []
    for i, poly in polygons.iterrows():

        pts_in_this_poly = []

        for j, pt in pts.iterrows():
            if poly.geometry.contains(pt.geometry):
                pts_in_this_poly.append(pt.geometry)
                pts = pts.drop([j])

        pts_in_polys.append(len(pts_in_this_poly))
    polygons['number of points'] = pts_in_polys
    return polygons


def plot_map_cloropleth(contagem, legenda):
    mapa = folium.Map(location=[-25.5, -49.3], tiles='OpenStreetMap', zoom_start=12)
    bins = list(contagem['number of points'].quantile([0, 0.25, 0.5, 0.75, 1]))
    folium.Choropleth(geo_data=contagem, name=legenda, columns=['OBJECTID', 'number of points'],
                      data=contagem, key_on='feature.properties.OBJECTID', fill_color='YlGn',
                      legend_name=legenda, bins=bins, reset=True).add_to(mapa)
    return mapa


def plot_map_point(nome_camada, camada):
    mapa = folium.Map(location=[-25.5, -49.3], tiles='OpenStreetMap', zoom_start=10)
    folium.GeoJson(camada, name=nome_camada, style_function=lambda x: style).add_to(mapa)
    folium.LayerControl().add_to(mapa)
    return mapa


def plot_map_heat(camada):
    mapa = folium.Map(location=[-25.5, -49.3], tiles='OpenStreetMap', zoom_start=12)
    locations = []
    for idx, row in camada.iterrows():
        locations.append([row['geometry'].y, row['geometry'].x])
    HeatMap(locations, name='Mapa de calor').add_to(mapa)
    folium.LayerControl().add_to(mapa)
    return mapa


def plot_grafic(contagem):
    resultado = contagem.groupby(["NOME"])['number of points'].aggregate(np.median).reset_index().sort_values('number '
                                                                                                              'of '
                                                                                                              'points')
    grafico = plt.figure(figsize=(10, 15))
    sns.barplot(y='NOME', x='number of points', data=resultado)
    plt.xlabel('Quantidade')
    plt.ylabel('Bairros')
    st.write(grafico)


# Menu lateral
st.sidebar.image(image, caption=None, width=300)
st.sidebar.title('**Bem vindo**!')
option = st.sidebar.selectbox('Selecione a página desejada', ['Início', 'Escolas Municipais', 'Hospitais',
                                                              'Unidades de Saúde', 'Ocupação Irregular', 'Sobre'])

if option == 'Início':
    # Página inicial
    st.header('**Página Inicial**')
    st.markdown('Navegue pela plataforma e veja mapas. Utilizar a caixa de seleção ao '
                'lado esquerdo para ver opções.')
    st.sidebar.markdown('                °                 ')
    botao = st.sidebar.button('Saiba mais')
    if botao == 1:
        st.sidebar.markdown('**Autor:** Leonardo de Oliveira Melo')
        st.sidebar.markdown('**Projeto:** Desenvolver plataforma com mapas interativos de Curitiba.')
        st.sidebar.markdown('**Status:** Em desenvolvimento.')
        st.sidebar.markdown('Maiores informações na aba "Sobre"')

if option == 'Escolas Municipais':
    st.header('**Escolas Municipais**')
    st.subheader('Aqui se encontram mapas referentes as Escolas Municipais da Região de Curitiba')
    st.markdown('A fonte dos dados utilizados foi : ')
    st.markdown('**Camada de Escolas Municipais:** IPPUC')
    escola_munic = gpd.read_file('escola_munic.geojson')
    nome = 'Escolas Municipais'
    campos_esc = ['NOME_COMPL', 'BAIRRO']
    conta = cont_point_polygon(escola_munic, layer_bairros)
    choice1 = st.checkbox('Marque para visualizar localização das escolas municipais')
    if choice1 == 1:
        escolas_munic = plot_map_point(nome, escola_munic)
        folium_static(escolas_munic)
    choice2 = st.checkbox('Marque para visualizar mapa de calor para as escolas municipais')
    if choice2 == 1:
        escolas_calor = plot_map_heat(escola_munic)
        folium_static(escolas_calor)
    choice3 = st.checkbox('Marque para visualizar mapa coroplético')
    if choice3 == 1:
        legend = 'Escolas Municipais por bairro'
        map_coropleth = plot_map_cloropleth(conta, legend)
        folium_static(map_coropleth)
    choice4 = st.checkbox('Marque para visualizar gráfico')
    if choice4 == 1:
        plot_grafic(conta)


if option == 'Hospitais':
    hospital = gpd.read_file('hospitais.geojson')
    nome = 'Hospitais'
    campos_hosp = ['NOME_COMPL', 'BAIRRO']
    conta = cont_point_polygon(hospital, layer_bairros)
    legend = 'Hospitais por bairro'
    st.header('**Hospitais**')
    st.subheader('Aqui se encontram mapas referentes aos Hospitais da Região de Curitiba')
    st.markdown('A fonte dos dados utilizados foi : ')
    st.markdown('**Camada de hospitais:** IPPUC')
    choice5 = st.checkbox('Marque para visualizar a localização dos Hospitais')
    if choice5 == 1:
        hospitais = plot_map_point(nome, hospital)
        folium_static(hospitais)
    choice6 = st.checkbox('Marque para visualizar o Mapa de calor dos Hospitais')
    if choice6 == 1:
        hospitais_calor = plot_map_heat(hospital)
        folium_static(hospitais_calor)
    choice7 = st.checkbox('Marque para visualizar mapa coroplético')
    if choice7 == 1:
        map_coropleth = plot_map_cloropleth(conta, legend)
        folium_static(map_coropleth)
    choice8 = st.checkbox('Marque para visualizar gráfico')
    if choice8 == 1:
        plot_grafic(conta)


if option == 'Unidades de Saúde':
    unid_saude = gpd.read_file('unidade_saude.geojson')
    nome = 'Unidade de Saúde'
    campos_unid = ['NOME_COMPL', 'BAIRRO']
    conta = cont_point_polygon(unid_saude, layer_bairros)
    legend = 'Unidades de Saúde por bairro'
    st.header('**Unidades de Saúde**')
    st.subheader('Aqui se encontram mapas referentes as Unidades de Saúde da Região de Curitiba')
    st.markdown('A fonte dos dados utilizados foi : ')
    st.markdown('**Camada de Unidades de Saúde:** IPPUC')
    choice9 = st.checkbox('Marque para visualizar a localização das Unidade de Saúde')
    if choice9 == 1:
        unidade_saude = plot_map_point(nome, unid_saude)
        folium_static(unidade_saude)
    choice10 = st.checkbox('Marque para visualizar o Mapa de calor das Unidade de Saúde')
    if choice10 == 1:
        unid_calor = plot_map_heat(unid_saude)
        folium_static(unid_calor)
    choice11 = st.checkbox('Marque para visualizar mapa coroplético')
    if choice11 == 1:
        map_coropleth = plot_map_cloropleth(conta, legend)
        folium_static(map_coropleth)
    choice12 = st.checkbox('Marque para visualizar gráfico')
    if choice12 == 1:
        plot_grafic(conta)


if option == 'Ocupação Irregular':
    st.header('**Areas de Ocupação Irregular**')
    st.subheader('Aqui se encontram mapas referentes as Areas de Ocupação Irregular da Região de Curitiba')
    st.markdown('A fonte dos dados utilizados foi : ')
    st.markdown('**Camada de Areas de Ocupação Irregular:** IPPUC')
    style = {'fillColor': '#FF0000', 'color': '#660000'}
    oc_irr = gpd.read_file('oc_irr.geojson')
    nome = 'Ocupações Irregulares'
    fields = ['NOME', 'FONTE']
    choice7 = st.checkbox('Marque para visualizar as Áreas de Ocupação Irregular')
    if choice7 == 1:
        ocupacoes = plot_map(nome, oc_irr, style, fields)
        folium_static(ocupacoes)

if option == 'Sobre':
    st.markdown('**Autor:** Leonardo de Oliveira Melo')
    st.markdown('**Formação:** Graduando em Eng. Cartógrafica e de Agrimensura')
    st.markdown('**Instituição:** Universidade Federal do Paraná')
    st.markdown('**Linkedin:** https://www.linkedin.com/in/leonardo-oliveira-melo-287593164/')
    st.markdown('**Projeto:** Desenvolver plataforma com mapas interativos de Curitiba.')
    st.markdown('**Status:** Em desenvolvimento.')
