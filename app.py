"""
ABC Dataset - Actos Públicos Digitales
Aplicación web para buscar y analizar ofertas de cargos docentes
"""
import streamlit as st
from utils.data_loader import load_ofertas, load_cargos, get_available_files

# Configuración de la página
st.set_page_config(
    page_title="ABC Dataset - Actos Públicos Digitales",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📚 ABC Dataset</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Actos Públicos Digitales - Provincia de Buenos Aires</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=ABC+Dataset", use_container_width=True)
    st.markdown("---")

    st.markdown("### 🎯 Navegación")
    st.markdown("""
    - **🏠 Inicio**: Información general
    - **🔍 Búsqueda**: Buscar ofertas de cargos
    - **📊 Estadísticas**: Análisis de datos
    - **📋 Cargos**: Información de cargos
    """)

    st.markdown("---")

    # Selector de archivo de datos
    st.markdown("### ⚙️ Configuración")

    available_files = get_available_files()

    if available_files['ofertas']:
        archivo_ofertas = st.selectbox(
            "Archivo de ofertas",
            available_files['ofertas'],
            index=0 if 'ofertas_muestra.json' in available_files['ofertas'] else 0
        )
        st.session_state['archivo_ofertas'] = archivo_ofertas
    else:
        st.warning("No se encontraron archivos de ofertas")
        st.session_state['archivo_ofertas'] = "ofertas_muestra.json"

    if available_files['cargos']:
        archivo_cargos = st.selectbox(
            "Archivo de cargos",
            available_files['cargos'],
            index=0 if 'cargos_ejemplo.json' in available_files['cargos'] else 0
        )
        st.session_state['archivo_cargos'] = archivo_cargos
    else:
        st.warning("No se encontraron archivos de cargos")
        st.session_state['archivo_cargos'] = "cargos_ejemplo.json"

    if st.button("🔄 Recargar datos"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("### 📖 Acerca de")
    st.markdown("""
    Esta aplicación permite buscar y analizar ofertas de cargos docentes
    de la provincia de Buenos Aires.

    **Desarrollado con:**
    - Python
    - Streamlit
    - Pandas
    - Plotly
    """)

# Contenido principal
st.markdown("## 👋 Bienvenido")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 ¿Qué puedes hacer aquí?")
    st.markdown("""
    **🔍 Búsqueda de Ofertas**
    - Filtrar por modalidad, distrito y cargo
    - Búsqueda por texto libre
    - Ver detalles completos de cada oferta
    - Exportar resultados a CSV/Excel

    **📊 Análisis Estadístico**
    - Visualizar distribución de ofertas
    - Analizar por distrito y modalidad
    - Identificar cargos más demandados
    - Gráficos interactivos

    **📋 Información de Cargos**
    - Lista completa de cargos habilitantes
    - Cargos bonificantes
    - Puntajes y modalidades
    """)

with col2:
    st.markdown("### 📊 Estadísticas Rápidas")

    # Cargar datos
    try:
        df_ofertas, metadata_ofertas = load_ofertas(st.session_state.get('archivo_ofertas', 'ofertas_muestra.json'))
        df_cargos, metadata_cargos = load_cargos(st.session_state.get('archivo_cargos', 'cargos_ejemplo.json'))

        if not df_ofertas.empty:
            # Métricas
            col_m1, col_m2, col_m3 = st.columns(3)

            with col_m1:
                st.metric("Total Ofertas", f"{len(df_ofertas):,}")

            with col_m2:
                n_distritos = df_ofertas['descdistrito'].nunique() if 'descdistrito' in df_ofertas.columns else 0
                st.metric("Distritos", n_distritos)

            with col_m3:
                n_modalidades = df_ofertas['descnivelmodalidad'].nunique() if 'descnivelmodalidad' in df_ofertas.columns else 0
                st.metric("Modalidades", n_modalidades)

            st.markdown("---")

            # Top 5 distritos
            if 'descdistrito' in df_ofertas.columns:
                st.markdown("**Top 5 Distritos con más ofertas:**")
                top_distritos = df_ofertas['descdistrito'].value_counts().head(5)
                for distrito, count in top_distritos.items():
                    st.markdown(f"- **{distrito}**: {count:,} ofertas")

            st.markdown("---")

            # Fecha de última actualización
            if metadata_ofertas.get('fecha_extraccion'):
                st.info(f"📅 Última actualización: {metadata_ofertas['fecha_extraccion']}")

        else:
            st.warning("No hay datos de ofertas disponibles")

    except Exception as e:
        st.error(f"Error al cargar datos: {e}")

st.markdown("---")

# Instrucciones
st.markdown("## 🚀 Comenzar")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 1️⃣ Explorar Ofertas")
    st.markdown("""
    Ve a la página **🔍 Búsqueda** en el sidebar para:
    - Filtrar ofertas por tus criterios
    - Ver detalles completos
    - Exportar resultados
    """)

with col2:
    st.markdown("### 2️⃣ Analizar Datos")
    st.markdown("""
    Visita **📊 Estadísticas** para:
    - Ver gráficos interactivos
    - Analizar tendencias
    - Comparar distritos
    """)

with col3:
    st.markdown("### 3️⃣ Consultar Cargos")
    st.markdown("""
    En **📋 Cargos** encontrarás:
    - Lista de cargos habilitantes
    - Cargos bonificantes
    - Puntajes y modalidades
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>ABC Dataset - Proyecto de análisis de Actos Públicos Digitales</p>
    <p>Desarrollado con Streamlit | Datos de la Provincia de Buenos Aires</p>
</div>
""", unsafe_allow_html=True)
