"""
Módulo para cargar y cachear datos de ofertas y cargos.
"""
import json
import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Dict, Tuple


@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_ofertas(archivo: str = "ofertas_muestra.json") -> Tuple[pd.DataFrame, Dict]:
    """
    Carga ofertas desde JSON y convierte a DataFrame.

    Args:
        archivo: Path al archivo JSON de ofertas

    Returns:
        Tuple con (DataFrame de ofertas, metadata)
    """
    filepath = Path(archivo)

    if not filepath.exists():
        st.error(f"No se encontró el archivo: {archivo}")
        return pd.DataFrame(), {}

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convertir a DataFrame
    df = pd.DataFrame(data.get('ofertas', []))
    metadata = data.get('metadata', {})

    # Convertir fechas a datetime
    date_columns = ['iniciooferta', 'finoferta', 'tomaposesion', 'supl_desde', 'supl_hasta']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Convertir tipos numéricos
    if 'hsmodulos' in df.columns:
        df['hsmodulos'] = pd.to_numeric(df['hsmodulos'], errors='coerce')
    if 'numdistrito' in df.columns:
        df['numdistrito'] = pd.to_numeric(df['numdistrito'], errors='coerce')

    return df, metadata


@st.cache_data(ttl=3600)
def load_cargos(archivo: str = "cargos_ejemplo.json") -> Tuple[pd.DataFrame, Dict]:
    """
    Carga cargos desde JSON y convierte a DataFrame.

    Args:
        archivo: Path al archivo JSON de cargos

    Returns:
        Tuple con (DataFrame de cargos, metadata)
    """
    filepath = Path(archivo)

    if not filepath.exists():
        st.warning(f"No se encontró el archivo: {archivo}")
        return pd.DataFrame(), {}

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    metadata = data.get('metadata', {})

    # Detectar formato
    if isinstance(data, list):
        # Formato plano
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        # Formato con habilitantes/bonificantes
        cargos = []

        if 'habilitantes' in data:
            for cargo in data['habilitantes']:
                cargo['tipo'] = 'habilitante'
                cargos.append(cargo)

        if 'bonificantes' in data:
            for cargo in data['bonificantes']:
                cargo['tipo'] = 'bonificante'
                cargos.append(cargo)

        df = pd.DataFrame(cargos)
    else:
        df = pd.DataFrame()

    return df, metadata


@st.cache_data
def get_available_files() -> Dict[str, list]:
    """
    Detecta archivos JSON disponibles en el directorio.

    Returns:
        Dict con listas de archivos de ofertas y cargos
    """
    base_path = Path(".")

    # Buscar archivos de ofertas
    ofertas_files = [
        f.name for f in base_path.glob("ofertas_*.json")
    ]

    # Buscar archivos de cargos
    cargos_files = [
        f.name for f in base_path.glob("cargos_*.json")
    ]

    return {
        'ofertas': sorted(ofertas_files),
        'cargos': sorted(cargos_files)
    }


def filtrar_ofertas(df: pd.DataFrame, **filtros) -> pd.DataFrame:
    """
    Filtra el DataFrame de ofertas según los parámetros.

    Args:
        df: DataFrame de ofertas
        **filtros: Filtros a aplicar

    Returns:
        DataFrame filtrado
    """
    df_filtered = df.copy()

    # Filtro por modalidad
    if filtros.get('modalidad') and filtros['modalidad'] != 'Todas':
        df_filtered = df_filtered[df_filtered['descnivelmodalidad'] == filtros['modalidad']]

    # Filtro por distrito
    if filtros.get('distrito') and filtros['distrito'] != 'Todos':
        df_filtered = df_filtered[df_filtered['descdistrito'] == filtros['distrito']]

    # Filtro por área de incumbencia
    if filtros.get('areaincumbencia') and filtros['areaincumbencia'] != 'Todas':
        df_filtered = df_filtered[df_filtered['areaincumbencia'] == filtros['areaincumbencia']]

    # Filtro por estado
    if filtros.get('estado') and filtros['estado'] != 'Todos':
        df_filtered = df_filtered[df_filtered['estado'] == filtros['estado']]

    # Búsqueda por texto
    if filtros.get('busqueda'):
        texto = filtros['busqueda'].lower()
        mask = (
            df_filtered['cargo'].str.lower().str.contains(texto, na=False) |
            df_filtered['descripcionarea'].str.lower().str.contains(texto, na=False) |
            df_filtered['descdistrito'].str.lower().str.contains(texto, na=False)
        )
        df_filtered = df_filtered[mask]

    # Filtro por rango de fechas
    if filtros.get('fecha_inicio') and 'finoferta' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['finoferta'] >= pd.Timestamp(filtros['fecha_inicio'])]

    if filtros.get('fecha_fin') and 'finoferta' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['finoferta'] <= pd.Timestamp(filtros['fecha_fin'])]

    return df_filtered


def format_oferta_detalle(oferta: pd.Series) -> Dict:
    """
    Formatea una oferta para mostrar en detalle.

    Args:
        oferta: Serie de Pandas con los datos de la oferta

    Returns:
        Dict con datos formateados
    """
    return {
        'Cargo': oferta.get('cargo', 'N/A'),
        'Descripción': oferta.get('descripcionarea', 'N/A'),
        'Modalidad': oferta.get('descnivelmodalidad', 'N/A'),
        'Distrito': oferta.get('descdistrito', 'N/A'),
        'Escuela': oferta.get('escuela', 'N/A'),
        'Domicilio': oferta.get('domiciliodesempeno', 'N/A'),
        'Turno': oferta.get('turno', 'N/A'),
        'Jornada': oferta.get('jornada', 'N/A'),
        'Horas/Módulos': oferta.get('hsmodulos', 'N/A'),
        'Estado': oferta.get('estado', 'N/A'),
        'Inicio oferta': oferta.get('iniciooferta', 'N/A'),
        'Fin oferta': oferta.get('finoferta', 'N/A'),
        'Toma de posesión': oferta.get('tomaposesion', 'N/A'),
        'Tipo oferta': oferta.get('tipooferta', 'N/A'),
        'Observaciones': oferta.get('observaciones', 'N/A'),
    }
