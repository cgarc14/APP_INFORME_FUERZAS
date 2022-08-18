# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 19:58:22 2022

@author: Cesar
"""
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import datetime
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Cm

st.set_page_config(page_title='Análisis de Fuerzas', 
                   page_icon= r'C:/Users/Cesar/Desktop/YJB/Miscelaneo/YJB Logo.png')


st.title('Análisis de datos obtenidos')
st.write('Etapa previa a informe de fuerzas final')
st.write('Por ahora, sólo puedes trabajar con un archivo CSV a la vez.')


data_csv = st.file_uploader('Sube el/los archivo/s aquí', type=['csv'], accept_multiple_files= False)

          # PARA UN SOLO CSV A LA VEZ

if data_csv is not None:
    st.title('Visualización de Archivos')
    st.write('Para facilitar la visualización, juntaremos las fuerzas de los archivos que subiste!')
    csv = pd.read_csv(data_csv)
    csv.columns = ['Id', 'Fuerza']
    st.write(csv)
    fmax = max(csv['Fuerza'])
    st.write(f"Fuerza máxima es de :  **{fmax} N**")

    idx = csv[['Id']].to_numpy()
    fuerza = csv[['Fuerza']].to_numpy()
    fig = plt.figure(figsize=(10, 4))
    plt.scatter(idx, fuerza, color = '#F36F59')
    plt.xlabel('Puntos de Medición')
    plt.ylabel('Fuerza Obtenida [N]')
    nombre_grafico = st.text_input('Ingresa el nombre del gráfico')
    plt.title(nombre_grafico)
    arch_grafico = plt.savefig(f"{nombre_grafico}.png")        
        
    b_grafico = st.button('Graficar Datos')
    
    if b_grafico and data_csv is not None:
        st.pyplot(fig)

    
    st.write('Si quieres, puedes descarga tu gráfico!')    
    st.download_button('Descargar', data = f"{nombre_grafico}.png", 
                        file_name = f"{nombre_grafico}.png"
                        )
    
    st.title('Creación del Informe')
    st.write('Acá haremos el informe con los datos que subiste!')
    
    data_plantilla = st.file_uploader('Primero, sube la plantilla que llenaremos. Es un archivo de Word!!'
                                      , type = ['docx'], accept_multiple_files= False)
    
    
    
    if data_plantilla is not None:
        st.title('Edición del Informe')
        st.write('Ahora pondremos los datos del paciente.')
        informe = DocxTemplate(data_plantilla)
        
        # Edicion del Word
          
        npaciente = st.text_input('Ingresa el nombre del paciente:', key='nombre_paciente')
        epaciente = st.text_input('Ingresa la edad del paciente:', key='edad_paciente')
        fpaciente = st.date_input('Ingresa la fecha de evaluación del paciente:', key='fecha_paciente')
        mpaciente = st.text_input('Ingresa el mail del paciente:', key='mail_paciente')
        comentario = st.text_area('Si tienes alguna observación adicional, escríbela aquí:', key='comentario')
        
        context = {
        'nombre_paciente' : npaciente,
        'edad_paciente' : epaciente,
        'mail_paciente' : mpaciente,
        'fecha_paciente' : fpaciente,
        'fmax1': fmax,
        # 'fmax2': f_cc_izq,
        # 'fmax3': f_iqt_der,
        # 'fmax4': f_cc_der,
        # 'frel_izq': frel_izq,
        # 'frel_der': frel_der,
        'grafico_iqt_izq': InlineImage(informe, f"{nombre_grafico}.png", height=Cm(5.83), width=Cm(8.16)),
        # 'grafico_cc_izq': InlineImage(informe, r'C:\Users\Cesar\Desktop\YJB\grafico_cc_izq.png', height=Cm(5.83), width=Cm(8.16)),
        # 'grafico_iqt_der': InlineImage(informe, r'C:\Users\Cesar\Desktop\YJB\grafico_iqt_der.png', height=Cm(5.83), width=Cm(8.16)),
        # 'grafico_cc_der': InlineImage(informe, r'C:\Users\Cesar\Desktop\YJB\grafico_cc_der.png', height=Cm(5.83), width=Cm(8.16)),
        }
        
        informe.render(context)
        arch_informe = informe.save(f"Evaluación {npaciente}.docx")
        
        st.write('Como todavía no estamos trabajando con todos los archivos CSV a la vez, entonces hay ciertos espacios en la plantilla que no se llenarán correctamente. '
                 'No te preocupes, eso se arreglará en la siguiente iteración de la app! \U0001F60A')
        st.download_button('Descarga el informe final!', data = f"Evaluación {npaciente}.docx",
                                file_name= f"Evaluación {npaciente}.docx")