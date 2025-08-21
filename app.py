import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración inicial de la página
st.set_page_config(page_title="EDA en Deportes", layout="wide")

st.title("📊 Exploratory Data Analysis (EDA) - Deportes")

# --- Generador de dataset sintético ---
st.sidebar.header("Generar Datos Sintéticos")

# Opciones de configuración
num_muestras = st.sidebar.slider("Número de muestras", min_value=50, max_value=500, value=200, step=50)
num_columnas = st.sidebar.slider("Número de columnas", min_value=2, max_value=6, value=4)

# Variables posibles (cuantitativas y cualitativas)
cuantitativas = {
    "Edad": lambda n: np.random.randint(15, 40, n),
    "Puntaje": lambda n: np.random.normal(70, 15, n).astype(int),
    "Altura (cm)": lambda n: np.random.normal(175, 10, n).astype(int),
    "Peso (kg)": lambda n: np.random.normal(70, 12, n).astype(int),
    "Años de experiencia": lambda n: np.random.randint(0, 20, n)
}

cualitativas = {
    "Deporte": lambda n: np.random.choice(["Fútbol", "Baloncesto", "Tenis", "Natación", "Atletismo"], n),
    "Género": lambda n: np.random.choice(["Masculino", "Femenino"], n),
    "País": lambda n: np.random.choice(["Colombia", "Argentina", "España", "EEUU", "Brasil"], n),
    "Categoría": lambda n: np.random.choice(["Junior", "Amateur", "Profesional"], n)
}

# Combinar todas las posibles
todas_columnas = {**cuantitativas, **cualitativas}

# Selección de columnas por parte del usuario
columnas_seleccionadas = st.sidebar.multiselect(
    "Selecciona las columnas",
    options=list(todas_columnas.keys()),
    default=list(todas_columnas.keys())[:num_columnas]
)

# Crear el DataFrame
data = {}
for col in columnas_seleccionadas:
    data[col] = todas_columnas[col](num_muestras)

df = pd.DataFrame(data)

st.subheader("📋 Vista previa de los datos generados")
st.dataframe(df.head())

# --- Exploración de datos ---
st.sidebar.header("Visualizaciones")

tipo_grafico = st.sidebar.selectbox(
    "Selecciona el tipo de gráfico",
    ["Histograma", "Gráfico de barras", "Gráfico de dispersión", "Gráfico de pastel", "Tendencia (línea)"]
)

st.subheader(f"📈 {tipo_grafico}")

if tipo_grafico == "Histograma":
    columna = st.selectbox("Selecciona columna numérica", df.select_dtypes(include=np.number).columns)
    fig, ax = plt.subplots()
    sns.histplot(df[columna], kde=True, ax=ax)
    st.pyplot(fig)

elif tipo_grafico == "Gráfico de barras":
    columna = st.selectbox("Selecciona columna categórica", df.select_dtypes(exclude=np.number).columns)
    fig, ax = plt.subplots()
    df[columna].value_counts().plot(kind="bar", ax=ax, color="skyblue")
    st.pyplot(fig)

elif tipo_grafico == "Gráfico de dispersión":
    columnas_num = df.select_dtypes(include=np.number).columns
    if len(columnas_num) >= 2:
        x = st.selectbox("Eje X", columnas_num, index=0)
        y = st.selectbox("Eje Y", columnas_num, index=1)
        fig, ax = plt.subplots()
        sns.scatterplot(x=df[x], y=df[y], ax=ax, hue=df.select_dtypes(exclude=np.number).iloc[:,0] if not df.select_dtypes(exclude=np.number).empty else None)
        st.pyplot(fig)
    else:
        st.warning("Necesitas al menos 2 columnas numéricas.")

elif tipo_grafico == "Gráfico de pastel":
    columna = st.selectbox("Selecciona columna categórica", df.select_dtypes(exclude=np.number).columns)
    fig, ax = plt.subplots()
    df[columna].value_counts().plot(kind="pie", autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)

elif tipo_grafico == "Tendencia (línea)":
    columnas_num = df.select_dtypes(include=np.number).columns
    columna = st.selectbox("Selecciona columna numérica", columnas_num)
    fig, ax = plt.subplots()
    df[columna].plot(kind="line", ax=ax, color="orange")
    st.pyplot(fig)

st.sidebar.success("Configura los gráficos y explora tus datos dinámicamente 🚀")
