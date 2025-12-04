# ABC Dataset - Actos Públicos Digitales

Scraper y herramientas para extraer datos de ofertas laborales docentes de la Provincia de Buenos Aires.

## Descripción

Este proyecto permite extraer y analizar datos de **Actos Públicos Digitales** del sitio de la Dirección General de Cultura y Educación de la Provincia de Buenos Aires.

## API Descubierta

**Endpoint:** API_ENDPOINT

**Tecnología:** Apache Solr (motor de búsqueda)

**Total de ofertas:** ~721,000 registros (según última consulta)

## Datos Disponibles

Cada oferta contiene:

- **Información básica:** estado, tipo de oferta, cargo
- **Ubicación:** distrito, escuela, domicilio de desempeño
- **Fechas:** inicio y cierre de oferta, toma de posesión
- **Horarios:** turno, jornada, días y horarios específicos
- **Detalles:** horas/módulos, curso/división, nivel/modalidad
- **Reemplazo:** nombre, CUIL y motivo del reemplazado
- **IDs:** IGE, CUPOF, ID SUNA, etc.

## Inicio Rápido

### 1. Instalar dependencias

```bash
pip install requests pandas
# Opcional para notebooks:
pip install jupyter matplotlib seaborn
```

### 2. Explorar la API

```bash
python explorar_api.py
```

Esto te mostrará:
- Total de ofertas disponibles (~722,000)
- Campos disponibles en cada registro (47 campos)
- Estadísticas por estado, distrito, cargo, nivel
- Top 10 de distritos y cargos
- Ejemplos de ofertas activas

### 3. Extraer datos básico

```python
from scraper_apd import APDScraper

scraper = APDScraper()

# Extraer muestra de 1000 ofertas
scraper.save_to_json('ofertas_muestra.json', max_ofertas=1000)

# Extraer TODAS las ofertas (¡puede tomar tiempo!)
scraper.save_to_json('ofertas_completas.json')

# Extraer con filtros específicos
scraper.save_to_json(
    'ofertas_activas.json',
    filtros={'estado': 'Publicada'},
    max_ofertas=10000
)
```

### 4. Análisis con Pandas

```python
import pandas as pd
import json

# Cargar datos
with open('ofertas_muestra.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data['ofertas'])

# Análisis básico
print(df['estado'].value_counts())
print(df['descdistrito'].value_counts().head(10))
print(df['cargo'].value_counts().head(10))

# Exportar a CSV
df.to_csv('ofertas.csv', index=False, encoding='utf-8-sig')
```

O usa el notebook incluido:
```bash
jupyter notebook analisis.ipynb
```

## Parámetros de la API

### Parámetros básicos

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `q` | Query de búsqueda | `*:*` (todos) |
| `rows` | Registros por página | `100` |
| `start` | Offset de paginación | `0`, `100`, `200`... |
| `sort` | Ordenamiento | `finoferta desc` |
| `wt` | Formato respuesta | `json` |

### Filtros disponibles (parámetro `fq`)

```python
# Por estado
fq='estado:"Activa"'

# Por distrito
fq='descdistrito:"LA PLATA"'

# Por cargo
fq='cargo:"MAESTRO DE GRADO (/MG)"'

# Por nivel
fq='descnivelmodalidad:"PRIMARIA"'

# Múltiples filtros (separados por &)
fq='estado:"Activa"&fq=numdistrito:1'
```

## Estructura del JSON generado

```json
{
  "metadata": {
    "total_ofertas": 1000,
    "fecha_extraccion": "2025-12-03T14:39:32",
    "filtros": {"estado": "Activa"}
  },
  "ofertas": [
    {
      "id": "1596618",
      "ige": 1609437,
      "estado": "Anulada",
      "tipooferta": "DESIGNACIONES DOCENTES",
      "cargo": "PLASTICA - VISUAL (APV)",
      "descdistrito": "GENERAL SAN MARTIN",
      "escuela": "0045MS0047",
      "numdistrito": 45,
      "descnivelmodalidad": "ARTISTICA",
      "turno": "M",
      "jornada": "JS",
      "hsmodulos": 2,
      "iniciooferta": "2023-04-18T00:00:00Z",
      "finoferta": "5023-04-19T10:30:00Z",
      "tomaposesion": "2023-04-19T00:00:00Z",
      "domiciliodesempeno": "CALLE EJEMPLO 123",
      "reemp_apeynom": "APELLIDO NOMBRE",
      "reemp_cuil": "20123456789",
      "reemp_motivo": "Licencia no medica por ARTICULO 114",
      ...
    }
  ]
}
```

## 🔧 Instalación

```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias básicas
pip install requests pandas

# Dependencias opcionales para análisis y notebooks
pip install jupyter matplotlib seaborn openpyxl pyarrow
```

## Estructura del Proyecto

```
ABC-dataset/
├── README.md                           # Este archivo
├── scraper_apd.py                      # Scraper principal
├── explorar_api.py                     # Explorador de API
├── cargos.py                           # Gestión de cargos docentes
├── cargos_ejemplo.json                 # Base de datos de cargos
│
├── scraper_por_cargos.py              # Extraer por cargos específicos
├── validar_ofertas_cargos.py          # Validar ofertas contra cargos
├── enriquecer_ofertas.py              # Enriquecer ofertas con info de cargos
│
├── analizar_pandas.py                  # Análisis con Pandas
├── ver_muestra.py                      # Ver resumen de datos
│
├── analisis.ipynb                      # Notebook básico
├── analisis_ofertas.ipynb             # Notebook completo con gráficos
│
└── ofertas_muestra.json               # Datos extraídos (ejemplo)
```

## Ejemplos de Consultas

### Ofertas activas de un distrito específico

```python
scraper = APDScraper()

for oferta in scraper.get_all_ofertas(
    filtros={'estado': 'Activa', 'distrito': 'LA PLATA'},
    max_ofertas=100
):
    print(f"{oferta['cargo']} - {oferta['escuela']}")
```

### Ofertas de Nivel Primario

```python
scraper.save_to_json(
    'ofertas_primaria.json',
    filtros={'descnivelmodalidad': 'PRIMARIA'}
)
```

### Ofertas que cierran próximamente

```python
import requests

url = API_ENDPOINT
params = {
    'q': '*:*',
    'fq': 'estado:"Activa"',
    'rows': 20,
    'sort': 'finoferta asc',  # Ordenar por cierre ascendente
    'wt': 'json'
}

response = requests.get(url, params=params)
data = response.json()

for doc in data['response']['docs']:
    print(f"{doc['cargo']} - Cierre: {doc['finoferta']}")
```

## Funcionalidades Avanzadas

### Gestión de Cargos

El proyecto incluye un sistema de gestión de cargos docentes:

```python
from cargos import Cargo, CargoRepository

# Cargar repositorio de cargos
repo = CargoRepository.load('cargos_ejemplo.json')

# Buscar cargos
ingles = repo.buscar_por_codigo('IGS')
primaria = repo.buscar_por_modalidad('PRIMARIA')
maestros = repo.buscar_por_palabra('maestro')
```

### Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `explorar_api.py` | Explora la API y muestra estadísticas |
| `scraper_apd.py` | Scraper principal con clase `APDScraper` |
| `scraper_por_cargos.py` | Extrae ofertas filtradas por cargos específicos |
| `validar_ofertas_cargos.py` | Valida ofertas contra cargos conocidos |
| `enriquecer_ofertas.py` | Enriquece ofertas con información de cargos |
| `analizar_pandas.py` | Análisis con Pandas (estadísticas y exports) |
| `ver_muestra.py` | Ver resumen rápido de ofertas extraídas |

### Extraer ofertas por cargos específicos

```bash
python scraper_por_cargos.py
```

Este script:
- Lee los cargos de `cargos_ejemplo.json`
- Busca ofertas para cada cargo
- Genera un JSON organizado por código de cargo

### Validar ofertas contra cargos conocidos

```bash
python validar_ofertas_cargos.py
```

Genera:
- `reporte_validacion_cargos.json` - Reporte completo
- `reporte_validacion_cargos.csv` - Exportación CSV
- `cargos_sugeridos.json` - Nuevos cargos encontrados

### Enriquecer ofertas

```bash
python enriquecer_ofertas.py
```

Agrega información del cargo a cada oferta:
```json
{
  "cargo": "MAESTRO DE GRADO (/MG)",
  "cargo_info": {
    "validado": true,
    "modalidad_cargo": "PRIMARIA",
    "codigo_cargo": "/MG",
    "valor": 1.0
  }
}
```

## Análisis en Jupyter Notebooks

### Notebooks incluidos:

- **`analisis.ipynb`** - Análisis exploratorio básico
- **`analisis_ofertas.ipynb`** - Análisis completo con visualizaciones

### Abrir notebook:

```bash
jupyter notebook analisis.ipynb
```

El notebook incluye:
- Carga de datos JSON
- Análisis estadístico
- Gráficos con matplotlib/seaborn
- Ejemplos de filtrado
- Exportación a CSV/Excel

## Consideraciones

1. **Encoding:** El servidor envía datos en ISO-8859-1 (Latin-1). El scraper está configurado para manejarlo correctamente
2. **SSL:** El servidor usa TLS 1.0 (antiguo). El scraper incluye adaptador SSL compatible
3. **Velocidad de extracción:** El scraper incluye pausas (`time.sleep`) para no saturar el servidor
4. **Volumen de datos:** ~722,000 ofertas × 47 campos = archivo JSON grande (~500MB estimado)
5. **CORS:** La API tiene `access-control-allow-origin: *`, por lo que es accesible desde cualquier origen
6. **Rate limiting:** No se detectó límite de peticiones, pero es recomendable ser respetuoso

## 📊 Campos Principales

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | string | ID único de detalle |
| `ige` | int | Identificador IGE |
| `idoferta` | int | ID de la oferta |
| `estado` | string | "Activa", "Anulada", etc. |
| `tipooferta` | string | "APD", "DESIGNACIONES DOCENTES" |
| `cargo` | string | Descripción del cargo |
| `descdistrito` | string | Nombre del distrito |
| `numdistrito` | int | Número de distrito |
| `escuela` | string | Código de establecimiento |
| `descnivelmodalidad` | string | Nivel educativo |
| `turno` | string | "M", "T", "V" (Mañana, Tarde, Vespertino) |
| `jornada` | string | Tipo de jornada |
| `hsmodulos` | int | Horas o módulos |
| `iniciooferta` | datetime | Fecha de inicio |
| `finoferta` | datetime | Fecha de cierre |
| `tomaposesion` | datetime | Fecha de toma de posesión |
| `domiciliodesempeno` | string | Dirección de la escuela |
| `reemp_apeynom` | string | Nombre del reemplazado |
| `reemp_cuil` | string | CUIL del reemplazado |
| `reemp_motivo` | string | Motivo del reemplazo |
| `supl_desde` | datetime | Desde (suplencia) |
| `supl_hasta` | datetime | Hasta (suplencia) |
| `lunes` a `sabado` | string | Horarios por día |

## 🎓 Valores de Referencia

### Estados posibles
- `Activa`
- `Anulada`
- `Cubierta`
- (otros por confirmar)

### Niveles/Modalidades
- `PRIMARIA`
- `SECUNDARIA`
- `INICIAL`
- `ARTISTICA`
- `EDUCACION FISICA`
- `TECNICO PROFESIONAL`
- (y más)

### Tipos de Oferta
- `APD` (Actos Públicos Digitales)
- `DESIGNACIONES DOCENTES`

## 🚀 Flujo de Trabajo Completo

```bash
# 1. Explorar la API
python explorar_api.py

# 2. Extraer muestra de ofertas
python scraper_apd.py

# 3. Validar contra cargos conocidos
python validar_ofertas_cargos.py

# 4. Revisar cargos sugeridos y actualizar cargos_ejemplo.json

# 5. Extraer ofertas por cargos específicos
python scraper_por_cargos.py

# 6. Enriquecer ofertas con información de cargos
python enriquecer_ofertas.py

# 7. Analizar en Pandas o Jupyter
python analizar_pandas.py
# o
jupyter notebook analisis.ipynb
```

## Solución de Problemas

### Error de SSL
El servidor usa TLS 1.0 antiguo. El scraper ya incluye el adaptador necesario.

### Caracteres especiales mal codificados
El scraper está configurado para manejar ISO-8859-1 (Latin-1) correctamente.

### Error de encoding en Windows
Si ves caracteres `�`, asegúrate de usar `encoding='utf-8-sig'` al exportar CSV.

## Datos de Ejemplo

Los datos están organizados en archivos JSON con la siguiente estructura:

**ofertas_muestra.json** - Muestra general de ofertas
**ofertas_por_cargos.json** - Ofertas agrupadas por código de cargo
**ofertas_enriquecidas.json** - Ofertas con información adicional de cargos

## Contacto

Para consultas sobre el uso de esta API, contactar a la DGCyE de Buenos Aires.

## Licencia

Este proyecto es solo para fines educativos y de investigación. Los datos pertenecen a la Dirección General de Cultura y Educación de la Provincia de Buenos Aires.

---

**Última actualización:** Diciembre 2025

**Tecnologías:** Python 3.12+ | Requests | Pandas | Jupyter | Apache Solr
