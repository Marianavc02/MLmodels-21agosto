import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🌱 EDA para Dataset de Agricultura")

# ------------------------------
# Subir archivo
# ------------------------------
archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo is not None:
    # Leer CSV
    df = pd.read_csv(archivo)

    st.subheader("Vista previa de los datos (original)")
    st.write(df.head())

    # ------------------------------
    # Limpieza de datos
    # ------------------------------
    st.subheader("🔧 Limpieza de datos")

    # Reemplazar "error" con NaN
    df.replace("error", np.nan, inplace=True)

    # Columnas numéricas (todas menos "Cultivo")
    cols_numericas = [c for c in df.columns if c != "Cultivo"]

    # Convertir a numérico
    for col in cols_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Rellenar NaN con la media de la columna
    df[cols_numericas] = df[cols_numericas].fillna(df[cols_numericas].mean())

    st.success("Datos limpiados correctamente ✅")
    st.write(df.head())

    # ------------------------------
    # Estadísticas
    # ------------------------------
    st.subheader("📊 Resumen estadístico")
    st.write(df.describe(include="all").transpose())

    # ------------------------------
    # Gráficas interactivas
    # ------------------------------
    st.subheader("📈 Visualización")

    columnas = df.columns.tolist()

    grafico = st.radio(
        "Selecciona el tipo de gráfico",
        ["Histograma", "Dispersión", "Barras", "Pastel"]
    )

    if grafico == "Histograma":
        col = st.selectbox("Selecciona la columna", cols_numericas)
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        st.pyplot(fig)

    elif grafico == "Dispersión":
        col_x = st.selectbox("Columna X", cols_numericas)
        col_y = st.selectbox("Columna Y", cols_numericas)
        fig, ax = plt.subplots()
        sns.scatterplot(x=df[col_x], y=df[col_y], hue=df["Cultivo"], ax=ax)
        st.pyplot(fig)

    elif grafico == "Barras":
        col = st.selectbox("Selecciona columna categórica", ["Cultivo"])
        fig, ax = plt.subplots()
        sns.countplot(x=df[col], ax=ax)
        st.pyplot(fig)

    elif grafico == "Pastel":
        col = st.selectbox("Selecciona columna categórica", ["Cultivo"])
        valores = df[col].value_counts()
        fig, ax = plt.subplots()
        ax.pie(valores, labels=valores.index, autopct="%1.1f%%")
        ax.axis("equal")
        st.pyplot(fig)
