"""
Página de información de cargos habilitantes y bonificantes
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_cargos

st.set_page_config(page_title="Cargos", page_icon="📋", layout="wide")

st.title("Información de Cargos")
st.markdown("Consulta cargos habilitantes y bonificantes con sus puntajes")

# Cargar datos
archivo_cargos = st.session_state.get('archivo_cargos', 'cargos_ejemplo.json')
df, metadata = load_cargos(archivo_cargos)

if df.empty:
    st.warning("No se pudieron cargar los cargos")
    st.stop()

# Información general
if metadata:
    col1, col2, col3 = st.columns(3)

    with col1:
        total_hab = metadata.get('total_habilitantes', 0)
        st.metric("Cargos Habilitantes", total_hab)

    with col2:
        total_bon = metadata.get('total_bonificantes', 0)
        st.metric("Cargos Bonificantes", total_bon)

    with col3:
        st.metric("Total Cargos", len(df))

    if metadata.get('descripcion'):
        st.info(f"**Descripción:** {metadata['descripcion']}")

st.markdown("---")

# Filtros
col1, col2, col3 = st.columns(3)

with col1:
    if 'tipo' in df.columns:
        tipo_filtro = st.selectbox(
            "Tipo de cargo",
            ['Todos', 'habilitante', 'bonificante']
        )
    else:
        tipo_filtro = 'Todos'

with col2:
    if 'modalidad' in df.columns:
        modalidades = ['Todas'] + sorted(df['modalidad'].unique().tolist())
        modalidad_filtro = st.selectbox("Modalidad", modalidades)
    else:
        modalidad_filtro = 'Todas'

with col3:
    busqueda = st.text_input("Buscar cargo", placeholder="Ej: danza, música...")

# Aplicar filtros
df_filtrado = df.copy()

if tipo_filtro != 'Todos' and 'tipo' in df.columns:
    df_filtrado = df_filtrado[df_filtrado['tipo'] == tipo_filtro]

if modalidad_filtro != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['modalidad'] == modalidad_filtro]

if busqueda:
    mask = (
        df_filtrado['area'].str.contains(busqueda, case=False, na=False) |
        df_filtrado['codigo'].str.contains(busqueda, case=False, na=False)
    )
    df_filtrado = df_filtrado[mask]

# Mostrar resultados
st.markdown(f"### Resultados: {len(df_filtrado)} cargos")

if len(df_filtrado) == 0:
    st.warning("No se encontraron cargos con los filtros seleccionados")
else:
    # Tabs por tipo
    if 'tipo' in df_filtrado.columns:
        tab1, tab2 = st.tabs(["Habilitantes", "Bonificantes"])

        with tab1:
            df_hab = df_filtrado[df_filtrado['tipo'] == 'habilitante']
            if not df_hab.empty:
                st.markdown(f"**{len(df_hab)} cargos habilitantes**")

                # Agrupar por modalidad
                for modalidad in sorted(df_hab['modalidad'].unique()):
                    with st.expander(f"{modalidad} ({len(df_hab[df_hab['modalidad']==modalidad])} cargos)"):
                        df_mod = df_hab[df_hab['modalidad'] == modalidad]
                        st.dataframe(
                            df_mod[['codigo', 'area', 'valor']],
                            use_container_width=True,
                            hide_index=True
                        )
            else:
                st.info("No hay cargos habilitantes con estos filtros")

        with tab2:
            df_bon = df_filtrado[df_filtrado['tipo'] == 'bonificante']
            if not df_bon.empty:
                st.markdown(f"**{len(df_bon)} cargos bonificantes**")

                # Agrupar por modalidad
                for modalidad in sorted(df_bon['modalidad'].unique()):
                    with st.expander(f"{modalidad} ({len(df_bon[df_bon['modalidad']==modalidad])} cargos)"):
                        df_mod = df_bon[df_bon['modalidad'] == modalidad]
                        st.dataframe(
                            df_mod[['codigo', 'area', 'valor']],
                            use_container_width=True,
                            hide_index=True
                        )
            else:
                st.info("No hay cargos bonificantes con estos filtros")
    else:
        # Sin separación por tipo
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

st.markdown("---")

# Estadísticas de cargos
st.markdown("### Estadísticas")

col1, col2 = st.columns(2)

with col1:
    if 'modalidad' in df.columns:
        st.markdown("#### Cargos por Modalidad")
        modalidad_counts = df['modalidad'].value_counts()
        st.bar_chart(modalidad_counts)

with col2:
    if 'valor' in df.columns:
        st.markdown("#### Distribución de Puntajes")
        valor_counts = df['valor'].value_counts().sort_index()
        st.bar_chart(valor_counts)

# Exportar
st.markdown("---")
st.markdown("### Exportar Datos")

col1, col2 = st.columns(2)

with col1:
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name="cargos_filtrados.csv",
        mime="text/csv"
    )

with col2:
    json_data = df_filtrado.to_json(orient='records', force_ascii=False, indent=2)
    st.download_button(
        label="Descargar JSON",
        data=json_data,
        file_name="cargos_filtrados.json",
        mime="application/json"
    )
