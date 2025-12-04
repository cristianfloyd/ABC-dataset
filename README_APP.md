# ABC Dataset - Aplicación Streamlit

Aplicación web para buscar y analizar ofertas de Actos Públicos Digitales de la Provincia de Buenos Aires.

## Características

### Búsqueda de Ofertas
- Filtros avanzados por modalidad, distrito y cargo
- Búsqueda por texto libre
- Filtros por rango de fechas
- Vista detallada de cada oferta
- Paginación de resultados
- Exportación a CSV y JSON

### Dashboard de Estadísticas
- Métricas principales (total ofertas, distritos, modalidades)
- Análisis por distrito con gráficos interactivos
- Análisis por modalidad (gráficos de torta y barras)
- Top cargos más demandados
- Análisis temporal (por mes, por día de la semana)
- Filtros personalizados

### Información de Cargos
- Lista de cargos habilitantes y bonificantes
- Filtros por tipo y modalidad
- Búsqueda de cargos
- Estadísticas de puntajes
- Exportación de datos

## Instalación

### Requisitos
- Python 3.8 o superior
- pip

### Pasos

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Verificar que existan los archivos de datos:
   - `ofertas_muestra.json` o `ofertas_artistica.json`
   - `cargos_ejemplo.json`

## Uso

### Ejecutar la aplicación localmente

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Cambiar archivos de datos

En el sidebar de la aplicación puedes seleccionar diferentes archivos JSON de ofertas y cargos.

### Navegación

La aplicación tiene 4 páginas:

1. **Inicio**: Página principal con información general y estadísticas rápidas
2. **Búsqueda**: Buscar y filtrar ofertas
3. **Estadísticas**: Dashboard con gráficos interactivos
4. **Cargos**: Información de cargos habilitantes y bonificantes

## Estructura del Proyecto

```
ABC-dataset/
├── app.py                      # Página principal
├── pages/
│   ├── 1_Busqueda.py          # Página de búsqueda
│   ├── 2_Estadisticas.py      # Dashboard de estadísticas
│   └── 3_Cargos.py            # Información de cargos
├── utils/
│   ├── __init__.py
│   └── data_loader.py         # Funciones para cargar datos
├── .streamlit/
│   └── config.toml            # Configuración de Streamlit
├── requirements.txt           # Dependencias
├── ofertas_muestra.json       # Datos de ofertas
├── cargos_ejemplo.json        # Datos de cargos
└── README_APP.md             # Este archivo
```

## Funcionalidades Técnicas

### Cache
La aplicación utiliza `@st.cache_data` para cachear los datos cargados, mejorando el rendimiento.

### Filtrado
Sistema de filtrado robusto que permite combinar múltiples criterios:
- Modalidad
- Distrito
- Área de incumbencia
- Estado
- Búsqueda por texto
- Rango de fechas

### Visualizaciones
Gráficos interactivos con Plotly:
- Gráficos de barras
- Gráficos de torta
- Gráficos de línea temporal
- Mapas de calor
- Gráficos de área

## Deploy

### Streamlit Cloud (Recomendado para Fase 1)

1. Sube el proyecto a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio de GitHub
4. Selecciona el archivo `app.py`
5. Deploy!

Tu aplicación estará disponible en: `https://[tu-usuario]-abc-dataset.streamlit.app`

### Otras opciones

- **Heroku**: Usar Procfile con el comando streamlit
- **Railway**: Deploy automático desde GitHub
- **Docker**: Crear Dockerfile con streamlit

## Próximos Pasos (Fase 2)

Ver [ROADMAP.md](ROADMAP.md) para el plan de migración a FastAPI + React.

## Troubleshooting

### Error: No se encuentra el archivo de datos
Asegúrate de que los archivos JSON estén en el directorio raíz del proyecto.

### Error: ModuleNotFoundError
Instala las dependencias:
```bash
pip install -r requirements.txt
```

### La aplicación no carga
Verifica que el puerto 8501 no esté en uso:
```bash
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # Linux/Mac
```

## Contacto y Contribuciones

Este es un proyecto educativo y de código abierto. Contribuciones son bienvenidas.
