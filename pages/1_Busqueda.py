"""
Página de búsqueda de ofertas de cargos docentes
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_ofertas, filtrar_ofertas, format_oferta_detalle

st.set_page_config(page_title="Búsqueda de Ofertas", page_icon="🔎", layout="wide")

st.title("Búsqueda de Ofertas")
st.markdown("Encuentra ofertas de cargos docentes con filtros avanzados")

# Cargar datos
archivo_ofertas = st.session_state.get('archivo_ofertas', 'ofertas_muestra.json')
df, metadata = load_ofertas(archivo_ofertas)

if df.empty:
    st.error("No se pudieron cargar las ofertas. Verifica que el archivo exista.")
    st.stop()

# Sidebar con filtros
st.sidebar.markdown("## 🎯 Filtros")

# Filtro por modalidad
modalidades = ['Todas'] + sorted(df['descnivelmodalidad'].dropna().unique().tolist())
filtro_modalidad = st.sidebar.selectbox("Modalidad", modalidades)

# Filtro por distrito
distritos = ['Todos'] + sorted(df['descdistrito'].dropna().unique().tolist())
filtro_distrito = st.sidebar.selectbox("Distrito", distritos)

# Filtro por área de incumbencia
if 'areaincumbencia' in df.columns:
    areas = ['Todas'] + sorted(df['areaincumbencia'].dropna().unique().tolist())
    filtro_area = st.sidebar.selectbox("Área de incumbencia", areas)
else:
    filtro_area = 'Todas'

# Filtro por estado
if 'estado' in df.columns:
    estados = ['Todos'] + sorted(df['estado'].dropna().unique().tolist())
    filtro_estado = st.sidebar.selectbox("Estado", estados)
else:
    filtro_estado = 'Todos'

# Búsqueda por texto
st.sidebar.markdown("---")
busqueda_texto = st.sidebar.text_input("🔎 Buscar por texto", placeholder="Ej: música, danza, inglés...")

# Filtro por fechas
st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Rango de fechas")

usar_filtro_fecha = st.sidebar.checkbox("Filtrar por fecha de cierre")

filtro_fecha_inicio = None
filtro_fecha_fin = None

if usar_filtro_fecha and 'finoferta' in df.columns:
    fecha_min = df['finoferta'].min()
    fecha_max = df['finoferta'].max()

    if pd.notna(fecha_min) and pd.notna(fecha_max):
        filtro_fecha_inicio = st.sidebar.date_input(
            "Desde",
            value=fecha_min.date() if pd.notna(fecha_min) else None,
            min_value=fecha_min.date() if pd.notna(fecha_min) else None,
            max_value=fecha_max.date() if pd.notna(fecha_max) else None
        )

        filtro_fecha_fin = st.sidebar.date_input(
            "Hasta",
            value=fecha_max.date() if pd.notna(fecha_max) else None,
            min_value=fecha_min.date() if pd.notna(fecha_min) else None,
            max_value=fecha_max.date() if pd.notna(fecha_max) else None
        )

# Aplicar filtros
df_filtrado = filtrar_ofertas(
    df,
    modalidad=filtro_modalidad,
    distrito=filtro_distrito,
    areaincumbencia=filtro_area,
    estado=filtro_estado,
    busqueda=busqueda_texto,
    fecha_inicio=filtro_fecha_inicio,
    fecha_fin=filtro_fecha_fin
)

# Mostrar resultados
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de ofertas", f"{len(df):,}")

with col2:
    st.metric("Ofertas filtradas", f"{len(df_filtrado):,}")

with col3:
    porcentaje = (len(df_filtrado) / len(df) * 100) if len(df) > 0 else 0
    st.metric("Porcentaje", f"{porcentaje:.1f}%")

st.markdown("---")

if len(df_filtrado) == 0:
    st.warning("No se encontraron ofertas con los filtros seleccionados")
    st.stop()

# Configuración de columnas a mostrar
columnas_disponibles = df_filtrado.columns.tolist()
columnas_default = ['cargo', 'descnivelmodalidad', 'descdistrito', 'escuela', 'hsmodulos', 'estado', 'finoferta']
columnas_mostrar = [col for col in columnas_default if col in columnas_disponibles]

with st.expander("⚙️ Configurar columnas a mostrar"):
    columnas_seleccionadas = st.multiselect(
        "Selecciona las columnas",
        columnas_disponibles,
        default=columnas_mostrar
    )
    if columnas_seleccionadas:
        columnas_mostrar = columnas_seleccionadas

# Paginación
items_per_page = st.selectbox("Resultados por página", [10, 25, 50, 100], index=1)

total_pages = (len(df_filtrado) - 1) // items_per_page + 1

if 'page_number' not in st.session_state:
    st.session_state.page_number = 0

col_prev, col_info, col_next = st.columns([1, 2, 1])

with col_prev:
    if st.button("⬅️ Anterior") and st.session_state.page_number > 0:
        st.session_state.page_number -= 1
        st.rerun()

with col_info:
    st.markdown(f"<div style='text-align: center'>Página {st.session_state.page_number + 1} de {total_pages}</div>", unsafe_allow_html=True)

with col_next:
    if st.button("Siguiente ➡️") and st.session_state.page_number < total_pages - 1:
        st.session_state.page_number += 1
        st.rerun()

# Mostrar datos paginados
start_idx = st.session_state.page_number * items_per_page
end_idx = start_idx + items_per_page
df_pagina = df_filtrado.iloc[start_idx:end_idx]

# Tabla de resultados
st.dataframe(
    df_pagina[columnas_mostrar],
    use_container_width=True,
    hide_index=True
)

# Expandir para ver detalles
st.markdown("---")
st.markdown("### 📋 Ver Detalles de Oferta")

# Selector de oferta por ID
if 'idoferta' in df_pagina.columns:
    ofertas_ids = df_pagina['idoferta'].tolist()
    ofertas_display = [f"{row['cargo']} - {row['descdistrito']} (ID: {row['idoferta']})" for _, row in df_pagina.iterrows()]

    oferta_seleccionada_idx = st.selectbox(
        "Selecciona una oferta para ver detalles completos",
        range(len(ofertas_display)),
        format_func=lambda x: ofertas_display[x]
    )

    if oferta_seleccionada_idx is not None:
        oferta = df_pagina.iloc[oferta_seleccionada_idx]

        with st.expander("👁️ Ver detalles completos", expanded=True):
            detalle = format_oferta_detalle(oferta)

            col1, col2 = st.columns(2)

            with col1:
                for i, (key, value) in enumerate(list(detalle.items())[:len(detalle)//2]):
                    st.markdown(f"**{key}:** {value}")

            with col2:
                for key, value in list(detalle.items())[len(detalle)//2:]:
                    st.markdown(f"**{key}:** {value}")

# Exportar resultados
st.markdown("---")
st.markdown("### 💾 Exportar Resultados")

col1, col2 = st.columns(2)

with col1:
    # Exportar a CSV
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name="ofertas_filtradas.csv",
        mime="text/csv"
    )

with col2:
    # Exportar a JSON
    json_data = df_filtrado.to_json(orient='records', force_ascii=False, indent=2)
    st.download_button(
        label="📥 Descargar JSON",
        data=json_data,
        file_name="ofertas_filtradas.json",
        mime="application/json"
    )
