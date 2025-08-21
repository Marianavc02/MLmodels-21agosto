import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

# -------------------------
# FUNCIONES
# -------------------------

def generar_datos(n_muestras, n_columnas):
    deportes = ["Fútbol", "Baloncesto", "Tenis", "Natación", "Ciclismo", "Atletismo"]
    paises = ["Colombia", "Argentina", "Brasil", "España", "EE.UU", "México"]
    categorias = ["Masculino", "Femenino"]

    data = {
        "Deporte": np.random.choice(deportes, n_muestras),
        "País": np.random.choice(paises, n_muestras),
        "Categoría": np.random.choice(categorias, n_muestras),
        "Edad": np.random.randint(15, 40, n_muestras),
        "Puntaje": np.random.randint(0, 100, n_muestras),
        "Duración_min": np.random.randint(30, 180, n_muestras),
    }

    df = pd.DataFrame(data)
    return df.iloc[:, :n_columnas]  # Se queda con las columnas elegidas


def graficar(df, tipo_grafico, col_x, col_y=None):
    fig, ax = plt.subplots()

    if tipo_grafico == "Tendencia (línea)":
        if col_y:
            sns.lineplot(data=df, x=col_x, y=col_y, ax=ax, marker="o")
        else:
            st.warning("Selecciona una columna Y para este gráfico.")

    elif tipo_grafico == "Barras":
        sns.countplot(data=df, x=col_x, ax=ax)

    elif tipo_grafico == "Dispersión":
        if col_y:
            sns.scatterplot(data=df, x=col_x, y=col_y, ax=ax)
        else:
            st.warning("Selecciona una columna Y para este gráfico.")

    elif tipo_grafico == "Histograma":
        sns.histplot(df[col_x], kde=True, ax=ax)

    elif tipo_grafico == "Pastel":
        valores = df[col_x].value_counts()
        ax.pie(valores, labels=valores.index, autopct="%1.1f%%")
        ax.axis("equal")

    st.pyplot(fig)


# -------------------------
# INTERFAZ STREAMLIT
# -------------------------

st.title("📊 Exploración de Datos Deportivos")
st.write("Genera un conjunto de datos sintético y explora gráficas interactivas.")

# Parámetros de generación
n_muestras = st.slider("Número de muestras", 50, 500, 100, step=50)
n_columnas = st.slider("Número de columnas", 2, 6, 4)

df = generar_datos(n_muestras, n_columnas)

# Mostrar tabla
if st.checkbox("Mostrar tabla de datos"):
    st.dataframe(df)

# Selección de columnas múltiples
columnas = df.columns.tolist()
cols_seleccionadas = st.multiselect("Selecciona las columnas que quieras analizar", columnas, default=columnas[:2])

# Para gráficos específicos X e Y
col_x = st.selectbox("Selecciona columna X", columnas)
col_y = None
if st.checkbox("¿Usar columna Y?"):
    col_y = st.selectbox("Selecciona columna Y", columnas)

# Selección de tipo de gráfico
tipo_grafico = st.radio(
    "Selecciona el tipo de gráfico",
    ["Tendencia (línea)", "Barras", "Dispersión", "Histograma", "Pastel"]
)

# Generar gráfico
if st.button("Generar gráfico"):
    graficar(df, tipo_grafico, col_x, col_y)
