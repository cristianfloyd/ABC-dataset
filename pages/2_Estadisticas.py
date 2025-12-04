"""
Dashboard de estadísticas y análisis de datos
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_ofertas

st.set_page_config(page_title="Estadísticas", page_icon="📊", layout="wide")

st.title("📊 Dashboard de Estadísticas")
st.markdown("Análisis y visualización de datos de ofertas docentes")

# Cargar datos
archivo_ofertas = st.session_state.get('archivo_ofertas', 'ofertas_muestra.json')
df, metadata = load_ofertas(archivo_ofertas)

if df.empty:
    st.error("No se pudieron cargar las ofertas")
    st.stop()

# Métricas principales
st.markdown("## 📈 Métricas Principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Ofertas", f"{len(df):,}")

with col2:
    n_distritos = df['descdistrito'].nunique() if 'descdistrito' in df.columns else 0
    st.metric("Distritos", n_distritos)

with col3:
    n_modalidades = df['descnivelmodalidad'].nunique() if 'descnivelmodalidad' in df.columns else 0
    st.metric("Modalidades", n_modalidades)

with col4:
    total_hs = df['hsmodulos'].sum() if 'hsmodulos' in df.columns else 0
    st.metric("Total Horas/Módulos", f"{total_hs:,.0f}")

st.markdown("---")

# Tabs para diferentes visualizaciones
tab1, tab2, tab3, tab4 = st.tabs(["📍 Por Distrito", "🎓 Por Modalidad", "📋 Por Cargo", "📅 Temporal"])

# TAB 1: Por Distrito
with tab1:
    st.markdown("### Ofertas por Distrito")

    if 'descdistrito' in df.columns:
        # Top 10 distritos
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Top 10 Distritos")
            distrito_counts = df['descdistrito'].value_counts().head(10)

            fig = px.bar(
                x=distrito_counts.values,
                y=distrito_counts.index,
                orientation='h',
                title="Distritos con más ofertas",
                labels={'x': 'Número de ofertas', 'y': 'Distrito'},
                color=distrito_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False, height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Horas/Módulos por Distrito (Top 10)")
            if 'hsmodulos' in df.columns:
                hs_por_distrito = df.groupby('descdistrito')['hsmodulos'].sum().sort_values(ascending=False).head(10)

                fig = px.bar(
                    x=hs_por_distrito.values,
                    y=hs_por_distrito.index,
                    orientation='h',
                    title="Total de horas/módulos por distrito",
                    labels={'x': 'Horas/Módulos', 'y': 'Distrito'},
                    color=hs_por_distrito.values,
                    color_continuous_scale='Greens'
                )
                fig.update_layout(showlegend=False, height=500)
                st.plotly_chart(fig, use_container_width=True)

        # Tabla completa
        st.markdown("#### Tabla Completa por Distrito")
        distrito_stats = df.groupby('descdistrito').agg({
            'idoferta': 'count',
            'hsmodulos': 'sum'
        }).rename(columns={'idoferta': 'Total Ofertas', 'hsmodulos': 'Total Horas/Módulos'})
        distrito_stats = distrito_stats.sort_values('Total Ofertas', ascending=False)

        st.dataframe(distrito_stats, use_container_width=True)

# TAB 2: Por Modalidad
with tab2:
    st.markdown("### Ofertas por Modalidad")

    if 'descnivelmodalidad' in df.columns:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Distribución por Modalidad")
            modalidad_counts = df['descnivelmodalidad'].value_counts()

            fig = px.pie(
                values=modalidad_counts.values,
                names=modalidad_counts.index,
                title="Proporción de ofertas por modalidad",
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Ofertas por Modalidad")
            fig = px.bar(
                x=modalidad_counts.index,
                y=modalidad_counts.values,
                title="Cantidad de ofertas por modalidad",
                labels={'x': 'Modalidad', 'y': 'Número de ofertas'},
                color=modalidad_counts.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        # Cruce Modalidad x Distrito (Top 5 de cada)
        st.markdown("#### Cruce: Modalidad x Distrito")

        top_modalidades = df['descnivelmodalidad'].value_counts().head(5).index
        top_distritos = df['descdistrito'].value_counts().head(10).index

        df_filtered = df[
            (df['descnivelmodalidad'].isin(top_modalidades)) &
            (df['descdistrito'].isin(top_distritos))
        ]

        heatmap_data = pd.crosstab(df_filtered['descdistrito'], df_filtered['descnivelmodalidad'])

        fig = px.imshow(
            heatmap_data,
            title="Mapa de calor: Top 10 Distritos x Top 5 Modalidades",
            labels=dict(x="Modalidad", y="Distrito", color="Ofertas"),
            color_continuous_scale='YlOrRd',
            aspect="auto"
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: Por Cargo
with tab3:
    st.markdown("### Ofertas por Cargo/Área")

    if 'areaincumbencia' in df.columns:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Top 15 Cargos Más Demandados")
            cargo_counts = df['areaincumbencia'].value_counts().head(15)

            fig = px.bar(
                x=cargo_counts.values,
                y=cargo_counts.index,
                orientation='h',
                title="Áreas de incumbencia más ofertadas",
                labels={'x': 'Número de ofertas', 'y': 'Cargo'},
                color=cargo_counts.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(showlegend=False, height=600)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Cargo Completo (Top 15)")
            if 'cargo' in df.columns:
                cargo_completo_counts = df['cargo'].value_counts().head(15)

                fig = px.bar(
                    x=cargo_completo_counts.values,
                    y=cargo_completo_counts.index,
                    orientation='h',
                    title="Cargos completos más ofertados",
                    labels={'x': 'Número de ofertas', 'y': 'Cargo'},
                    color=cargo_completo_counts.values,
                    color_continuous_scale='Purples'
                )
                fig.update_layout(showlegend=False, height=600)
                st.plotly_chart(fig, use_container_width=True)

        # Tabla de cargos
        st.markdown("#### Tabla de Cargos")
        cargo_stats = df.groupby('areaincumbencia').agg({
            'idoferta': 'count',
            'hsmodulos': 'sum'
        }).rename(columns={'idoferta': 'Total Ofertas', 'hsmodulos': 'Total Horas/Módulos'})
        cargo_stats = cargo_stats.sort_values('Total Ofertas', ascending=False)

        st.dataframe(cargo_stats.head(20), use_container_width=True)

# TAB 4: Análisis Temporal
with tab4:
    st.markdown("### Análisis Temporal")

    if 'finoferta' in df.columns:
        df['finoferta_date'] = pd.to_datetime(df['finoferta'], errors='coerce')
        df_temporal = df.dropna(subset=['finoferta_date'])

        if not df_temporal.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Ofertas por Mes")
                df_temporal['mes'] = df_temporal['finoferta_date'].dt.to_period('M').astype(str)
                ofertas_por_mes = df_temporal.groupby('mes').size()

                fig = px.line(
                    x=ofertas_por_mes.index,
                    y=ofertas_por_mes.values,
                    title="Timeline de ofertas por mes",
                    labels={'x': 'Mes', 'y': 'Número de ofertas'},
                    markers=True
                )
                fig.update_traces(line_color='#1f77b4', line_width=3)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### Ofertas por Día de la Semana")
                df_temporal['dia_semana'] = df_temporal['finoferta_date'].dt.day_name()
                dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

                ofertas_por_dia = df_temporal['dia_semana'].value_counts()

                # Reordenar y traducir
                ofertas_por_dia = ofertas_por_dia.reindex(dias_orden)
                ofertas_por_dia.index = dias_es

                fig = px.bar(
                    x=ofertas_por_dia.index,
                    y=ofertas_por_dia.values,
                    title="Distribución por día de la semana",
                    labels={'x': 'Día', 'y': 'Número de ofertas'},
                    color=ofertas_por_dia.values,
                    color_continuous_scale='Teal'
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            # Timeline completo
            st.markdown("#### Timeline Completo")
            df_temporal['fecha'] = df_temporal['finoferta_date'].dt.date
            ofertas_por_fecha = df_temporal.groupby('fecha').size().reset_index(name='ofertas')

            fig = px.area(
                ofertas_por_fecha,
                x='fecha',
                y='ofertas',
                title="Evolución temporal de ofertas",
                labels={'fecha': 'Fecha', 'ofertas': 'Número de ofertas'}
            )
            fig.update_traces(fill='tozeroy', fillcolor='rgba(31,119,180,0.3)', line_color='#1f77b4')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay datos temporales válidos para mostrar")

st.markdown("---")

# Filtros interactivos
st.markdown("## 🎯 Análisis Personalizado")

col1, col2 = st.columns(2)

with col1:
    if 'descnivelmodalidad' in df.columns:
        modalidad_seleccionada = st.selectbox(
            "Filtrar por modalidad",
            ['Todas'] + sorted(df['descnivelmodalidad'].unique().tolist())
        )
    else:
        modalidad_seleccionada = 'Todas'

with col2:
    if 'descdistrito' in df.columns:
        distrito_seleccionado = st.selectbox(
            "Filtrar por distrito",
            ['Todos'] + sorted(df['descdistrito'].unique().tolist())
        )
    else:
        distrito_seleccionado = 'Todos'

# Aplicar filtros
df_custom = df.copy()
if modalidad_seleccionada != 'Todas':
    df_custom = df_custom[df_custom['descnivelmodalidad'] == modalidad_seleccionada]
if distrito_seleccionado != 'Todos':
    df_custom = df_custom[df_custom['descdistrito'] == distrito_seleccionado]

if not df_custom.empty:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Ofertas filtradas", f"{len(df_custom):,}")

    with col2:
        if 'hsmodulos' in df_custom.columns:
            st.metric("Total horas/módulos", f"{df_custom['hsmodulos'].sum():,.0f}")

    with col3:
        if 'areaincumbencia' in df_custom.columns:
            st.metric("Cargos únicos", df_custom['areaincumbencia'].nunique())

    # Gráfico personalizado
    if 'areaincumbencia' in df_custom.columns:
        st.markdown("#### Top Cargos en la selección")
        top_cargos = df_custom['areaincumbencia'].value_counts().head(10)

        fig = px.bar(
            x=top_cargos.values,
            y=top_cargos.index,
            orientation='h',
            labels={'x': 'Ofertas', 'y': 'Cargo'},
            color=top_cargos.values,
            color_continuous_scale='Rainbow'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No hay datos con los filtros seleccionados")
