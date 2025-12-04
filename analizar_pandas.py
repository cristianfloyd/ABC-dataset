"""
Análisis de ofertas usando Pandas
"""

import pandas as pd
import json

# Cargar el JSON
print("Cargando datos...")
with open("ofertas_muestra.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convertir a DataFrame
df = pd.DataFrame(data["ofertas"])

print("=" * 70)
print("INFORMACIÓN DEL DATASET")
print("=" * 70)
print(f"\nTotal de registros: {len(df):,}")
print(f"Total de columnas: {len(df.columns)}")
print(f"\nDimensiones: {df.shape}")

print("\n" + "=" * 70)
print("PRIMERAS 5 OFERTAS")
print("=" * 70)
# Mostrar solo columnas clave
columnas_clave = [
    "estado",
    "cargo",
    "descdistrito",
    "escuela",
    "descnivelmodalidad",
    "ige",
]
print(df[columnas_clave].head())

print("\n" + "=" * 70)
print("TIPOS DE DATOS")
print("=" * 70)
print(df.dtypes)

print("\n" + "=" * 70)
print("ESTADÍSTICAS POR ESTADO")
print("=" * 70)
print(df["estado"].value_counts())
print(f"\nPorcentajes:")
print(df["estado"].value_counts(normalize=True) * 100)

print("\n" + "=" * 70)
print("TOP 10 DISTRITOS")
print("=" * 70)
print(df["descdistrito"].value_counts().head(10))

print("\n" + "=" * 70)
print("TOP 10 CARGOS")
print("=" * 70)
print(df["cargo"].value_counts().head(10))

print("\n" + "=" * 70)
print("DISTRIBUCIÓN POR NIVEL/MODALIDAD")
print("=" * 70)
print(df["descnivelmodalidad"].value_counts())

print("\n" + "=" * 70)
print("ESTADÍSTICAS DE HORAS/MÓDULOS")
print("=" * 70)
print(df["hsmodulos"].describe())

print("\n" + "=" * 70)
print("DATOS FALTANTES (NULLS)")
print("=" * 70)
nulls = df.isnull().sum()
print(nulls[nulls > 0].sort_values(ascending=False))

# Guardar el DataFrame procesado
print("\n" + "=" * 70)
print("GUARDANDO ARCHIVOS...")
print("=" * 70)

# Exportar a CSV
df.to_csv("ofertas_muestra.csv", index=False, encoding="utf-8-sig")
print("✓ Guardado: ofertas_muestra.csv")

# Exportar a Excel (requiere openpyxl)
try:
    df.to_excel("ofertas_muestra.xlsx", index=False, engine="openpyxl")
    print("✓ Guardado: ofertas_muestra.xlsx")
except ImportError:
    print("✗ No se pudo guardar Excel (instala: pip install openpyxl)")

# Exportar a Parquet (más eficiente)
try:
    df.to_parquet("ofertas_muestra.parquet", index=False)
    print("✓ Guardado: ofertas_muestra.parquet")
except ImportError:
    print("✗ No se pudo guardar Parquet (instala: pip install pyarrow)")

print("\n" + "=" * 70)
print("INFORMACIÓN DE COLUMNAS")
print("=" * 70)
print("\nColumnas disponibles:")
for i, col in enumerate(sorted(df.columns), 1):
    print(f"{i:2}. {col}")

print("\n" + "=" * 70)
print("EJEMPLOS DE CONSULTAS CON PANDAS")
print("=" * 70)
print("""
# Filtrar ofertas publicadas
df_publicadas = df[df['estado'] == 'Publicada']

# Filtrar por distrito
df_tigre = df[df['descdistrito'] == 'TIGRE']

# Filtrar por nivel
df_primaria = df[df['descnivelmodalidad'] == 'PRIMARIA']

# Múltiples filtros
df_filtrado = df[
    (df['estado'] == 'Publicada') &
    (df['descdistrito'] == 'TIGRE') &
    (df['descnivelmodalidad'] == 'PRIMARIA')
]

# Agrupar por distrito y contar
df.groupby('descdistrito')['ige'].count().sort_values(ascending=False)

# Agrupar por distrito y cargo
df.groupby(['descdistrito', 'cargo']).size().sort_values(ascending=False)

# Buscar texto en cargo
df[df['cargo'].str.contains('INGLES', na=False)]

# Ofertas con más horas
df.nlargest(10, 'hsmodulos')[['cargo', 'descdistrito', 'hsmodulos']]
""")

print(
    "\n¡Listo! Ya puedes trabajar con el DataFrame en Python o cargar los archivos CSV/Excel"
)
