import pandas as pd
import numpy as np

# Cargar el dataset
df = pd.read_csv("dataset_agricultura.csv")

# Reemplazar valores "error" por NaN
df.replace("error", np.nan, inplace=True)

# Convertir todas las columnas numéricas a float (excepto "Cultivo")
cols_numericas = [c for c in df.columns if c != "Cultivo"]
for col in cols_numericas:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Manejar valores nulos: rellenar con la media de cada columna
df[cols_numericas] = df[cols_numericas].fillna(df[cols_numericas].mean())

# Verificar resultado
print("\nTipos de datos:")
print(df.dtypes)

print("\nValores nulos después de limpieza:")
print(df.isnull().sum())

print("\nEstadísticas descriptivas:")
print(df.describe())

print("\nDistribución de la variable categórica 'Cultivo':")
print(df["Cultivo"].value_counts())
