import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Título de la aplicación
st.title('Ejercicio 01 - Análisis Exploratorio de Datos (EDA) Dinámico')

st.markdown("""
Esta aplicación permite generar un conjunto de datos sintético sobre deportes
y realizar un análisis exploratorio de datos de manera interactiva.
""")

# --- Generación de datos simulados ---
st.header('1. Generación del Conjunto de Datos')
st.markdown("Utiliza los controles deslizables para configurar el conjunto de datos.")

# Controles deslizables para la configuración del dataset
num_muestras = st.slider('Número de muestras (filas)', 10, 500, 100)
num_columnas = st.slider('Número de columnas', 2, 6, 4)

# Definición de las variables
deportes_populares = [
    'Fútbol', 'Baloncesto', 'Tenis', 'Béisbol', 'Natación', 'Atletismo',
    'Voleibol', 'Boxeo', 'Golf', 'Ciclismo', 'Gimnasia', 'Rugby'
]
ciudades = [
    'Madrid', 'Barcelona', 'Londres', 'París', 'Roma', 'Nueva York',
    'Tokio', 'Río de Janeiro', 'Sídney', 'Ciudad de México'
]
nombres_masculinos = ['Juan', 'Pedro', 'Luis', 'Carlos', 'Miguel', 'José', 'Andrés', 'David']
nombres_femeninos = ['Ana', 'María', 'Laura', 'Sofía', 'Lucía', 'Isabel', 'Elena', 'Carla']
paises = ['España', 'Estados Unidos', 'Brasil', 'Japón', 'Francia', 'Alemania', 'Australia', 'Canadá']

# Tipos de datos para las columnas
columnas_disponibles = {
    'Edad': 'cuantitativa',
    'Estatura (cm)': 'cuantitativa',
    'Peso (kg)': 'cuantitativa',
    'Nivel': 'cualitativa',
    'Deporte': 'cualitativa',
    'Ciudad': 'cualitativa',
    'País': 'cualitativa',
    'Sexo': 'cualitativa',
    'Puntaje': 'cuantitativa',
    'Tiempo (s)': 'cuantitativa',
    'Nombre': 'cualitativa'
}

# Generar un conjunto de datos basado en los controles deslizables
@st.cache_data
def generar_dataframe(num_muestras, num_columnas):
    data = {}
    
    # Asegurarse de que la columna 'Deporte' esté siempre presente
    columnas_elegidas = ['Deporte']
    
    # Seleccionar las columnas restantes de forma aleatoria
    otras_columnas = [col for col in columnas_disponibles.keys() if col != 'Deporte']
    if num_columnas > 1:
        columnas_elegidas.extend(random.sample(otras_columnas, num_columnas - 1))

    for col in columnas_elegidas:
        tipo = columnas_disponibles[col]
        if tipo == 'cuantitativa':
            if col == 'Edad':
                data[col] = np.random.randint(18, 40, num_muestras)
            elif col == 'Estatura (cm)':
                data[col] = np.random.normal(175, 10, num_muestras).astype(int)
            elif col == 'Peso (kg)':
                data[col] = np.random.normal(75, 8, num_muestras).astype(int)
            elif col == 'Puntaje':
                data[col] = np.random.randint(50, 100, num_muestras)
            elif col == 'Tiempo (s)':
                data[col] = np.random.randint(10, 60, num_muestras)
        else: # Tipo cualitativa o categórica
            if col == 'Deporte':
                data[col] = np.random.choice(deportes_populares, num_muestras)
            elif col == 'Ciudad':
                data[col] = np.random.choice(ciudades, num_muestras)
            elif col == 'Nivel':
                data[col] = np.random.choice(['Principiante', 'Intermedio', 'Avanzado'], num_muestras)
            elif col == 'Sexo':
                data[col] = np.random.choice(['Masculino', 'Femenino'], num_muestras)
            elif col == 'País':
                data[col] = np.random.choice(paises, num_muestras)
            elif col == 'Nombre':
                nombres = [random.choice(nombres_masculinos) if sex == 'Masculino' else random.choice(nombres_femeninos) for sex in np.random.choice(['Masculino', 'Femenino'], num_muestras)]
                data[col] = nombres

    df = pd.DataFrame(data)
    return df

df = generar_dataframe(num_muestras, num_columnas)

st.subheader('Visualización del Conjunto de Datos')
st.write(f"El conjunto de datos generado tiene {df.shape[0]} filas y {df.shape[1]} columnas.")
if st.checkbox('Mostrar datos'):
    st.dataframe(df)

# --- 2. Análisis y Visualización ---
st.header('2. Análisis y Visualización de Datos')

# Seleccionar tipo de gráfico
tipo_grafico = st.selectbox(
    "Selecciona el tipo de gráfico:",
    ['Gráfico de Barras', 'Histograma', 'Gráfico de Dispersión', 'Gráfico de Pastel', 'Mapa de Calor']
)

# Seleccionar columnas para el gráfico
columnas = list(df.columns)

# Lógica para mostrar los gráficos basados en la selección
if tipo_grafico == 'Gráfico de Barras':
    st.subheader("Gráfico de Barras")
    columna_barra = st.selectbox("Selecciona una columna categórica:", [col for col in columnas if df[col].dtype == 'object'])
    if columna_barra:
        conteo = df[columna_barra].value_counts()
        fig, ax = plt.subplots()
        conteo.plot(kind='bar', ax=ax)
        ax.set_title(f'Conteo por {columna_barra}')
        ax.set_xlabel(columna_barra)
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

elif tipo_grafico == 'Histograma':
    st.subheader("Histograma")
    columna_hist = st.selectbox("Selecciona una columna numérica:", [col for col in columnas if np.issubdtype(df[col].dtype, np.number)])
    if columna_hist:
        fig, ax = plt.subplots()
        df[columna_hist].hist(ax=ax)
        ax.set_title(f'Histograma de {columna_hist}')
        ax.set_xlabel(columna_hist)
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

elif tipo_grafico == 'Gráfico de Dispersión':
    st.subheader("Gráfico de Dispersión")
    columna_x = st.selectbox("Selecciona la columna del eje X:", [col for col in columnas if np.issubdtype(df[col].dtype, np.number)])
    columna_y = st.selectbox("Selecciona la columna del eje Y:", [col for col in columnas if np.issubdtype(df[col].dtype, np.number)])
    if columna_x and columna_y:
        fig, ax = plt.subplots()
        ax.scatter(df[columna_x], df[columna_y])
        ax.set_title(f'Gráfico de Dispersión de {columna_x} vs {columna_y}')
        ax.set_xlabel(columna_x)
        ax.set_ylabel(columna_y)
        st.pyplot(fig)

elif tipo_grafico == 'Gráfico de Pastel':
    st.subheader("Gráfico de Pastel")
    columna_pastel = st.selectbox("Selecciona una columna categórica:", [col for col in columnas if df[col].dtype == 'object'])
    if columna_pastel:
        conteo = df[columna_pastel].value_counts()
        fig, ax = plt.subplots()
        ax.pie(conteo, labels=conteo.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal') # Para asegurar que el gráfico sea circular
        ax.set_title(f'Distribución de {columna_pastel}')
        st.pyplot(fig)

elif tipo_grafico == 'Mapa de Calor':
    st.subheader("Mapa de Calor (Correlación)")
    numericas = df.select_dtypes(include=np.number)
    if not numericas.empty and len(numericas.columns) >= 2:
        corr_matrix = numericas.corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Mapa de Calor de la Matriz de Correlación')
        st.pyplot(fig)
    else:
        st.warning("No hay suficientes columnas numéricas para crear un mapa de calor.")

st.markdown("---")
st.markdown("Desarrollado con Streamlit, Pandas y Matplotlib.")

