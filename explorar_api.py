"""
Script para explorar la API de APD y entender los datos disponibles
"""

import requests
import json
from collections import Counter
import urllib3
import ssl
from requests.adapters import HTTPAdapter
from config import API_ENDPOINT

# Deshabilitar advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TLSAdapter(HTTPAdapter):
    """Adapter que fuerza TLS 1.0/1.1/1.2 para servidores con SSL antiguo"""
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        # Permitir TLS 1.0 y superiores
        ctx.minimum_version = ssl.TLSVersion.TLSv1
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)


def explorar_api():
    """Explora la estructura de la API y muestra estadísticas"""

    url = API_ENDPOINT

    # Obtener una muestra grande para análisis
    params = {
        "q": "*:*",
        "rows": 500,  # Muestra de 500 ofertas
        "start": 0,
        "wt": "json",
        "json.nl": "map",
        "sort": "finoferta desc",
    }

    print("Explorando la API de Actos Publicos Digitales...\n")

    # Crear sesión con adapter personalizado para SSL antiguo
    session = requests.Session()
    session.mount('https://', TLSAdapter())

    response = session.get(url, params=params, verify=False)
    data = response.json()

    total = data["response"]["numFound"]
    docs = data["response"]["docs"]

    print("ESTADÍSTICAS GENERALES")
    print(f"{'=' * 50}")
    print(f"Total de ofertas en la base: {total:,}")
    print(f"Muestra analizada: {len(docs)} ofertas\n")

    # Analizar campos disponibles
    print("CAMPOS DISPONIBLES EN CADA OFERTA")
    print(f"{'=' * 50}")
    if docs:
        campos = list(docs[0].keys())
        print(f"Total de campos: {len(campos)}")
        for i, campo in enumerate(sorted(campos), 1):
            ejemplo = docs[0][campo]
            if isinstance(ejemplo, str) and len(ejemplo) > 50:
                ejemplo = ejemplo[:50] + "..."
            print(f"{i:2}. {campo:30} -> {ejemplo}")

    # Estadísticas de estados
    print("\n>> DISTRIBUCION POR ESTADO")
    print(f"{'=' * 50}")
    estados = Counter(doc.get("estado", "Sin estado") for doc in docs)
    for estado, cantidad in estados.most_common():
        porcentaje = (cantidad / len(docs)) * 100
        print(f"{estado:20} -> {cantidad:4} ({porcentaje:5.1f}%)")

    # Estadísticas de distritos
    print("\n>> TOP 10 DISTRITOS CON MAS OFERTAS")
    print(f"{'=' * 50}")
    distritos = Counter(doc.get("descdistrito", "Sin distrito") for doc in docs)
    for distrito, cantidad in distritos.most_common(10):
        print(f"{distrito:30} -> {cantidad:4}")

    # Estadísticas de cargos
    print("\n>> TOP 10 CARGOS MAS OFERTADOS")
    print(f"{'=' * 50}")
    cargos = Counter(doc.get("cargo", "Sin cargo") for doc in docs)
    for cargo, cantidad in cargos.most_common(10):
        cargo_corto = cargo[:45] + "..." if len(cargo) > 45 else cargo
        print(f"{cargo_corto:48} -> {cantidad:4}")

    # Estadísticas de niveles
    print("\n>> DISTRIBUCION POR NIVEL/MODALIDAD")
    print(f"{'=' * 50}")
    niveles = Counter(doc.get("descnivelmodalidad", "Sin nivel") for doc in docs)
    for nivel, cantidad in niveles.most_common():
        porcentaje = (cantidad / len(docs)) * 100
        print(f"{nivel:30} -> {cantidad:4} ({porcentaje:5.1f}%)")

    # Tipos de oferta
    print("\n>> TIPOS DE OFERTA")
    print(f"{'=' * 50}")
    tipos = Counter(doc.get("tipooferta", "Sin tipo") for doc in docs)
    for tipo, cantidad in tipos.most_common():
        porcentaje = (cantidad / len(docs)) * 100
        print(f"{tipo:30} -> {cantidad:4} ({porcentaje:5.1f}%)")

    # Guardar un ejemplo completo
    print("\n>> Guardando ejemplo de oferta completa en 'ejemplo_oferta.json'")
    with open("ejemplo_oferta.json", "w", encoding="utf-8") as f:
        json.dump(docs[0], f, ensure_ascii=False, indent=2)

    print("\n>> Exploracion completada!")
    print("\n>> CONSEJOS PARA SCRAPING:")
    print("   * Usa filtros con fq= para consultas especificas")
    print('   * Ejemplo: fq=estado:"Activa" para solo ofertas activas')
    print("   * Aumenta 'rows' hasta 1000 para extraer mas rapido")
    print(f"   * Total estimado: {total:,} ofertas disponibles")


def buscar_ofertas_activas():
    """Busca solo ofertas activas"""

    url = API_ENDPOINT

    params = {
        "q": "*:*",
        "fq": 'estado:"Activa"',  # Filtro por estado activa
        "rows": 10,
        "start": 0,
        "wt": "json",
        "json.nl": "map",
        "sort": "finoferta asc",  # Ordenar por las que cierran antes
    }

    print("\n>> OFERTAS ACTIVAS (proximas a cerrar)")
    print(f"{'=' * 50}")

    # Crear sesión con adapter personalizado para SSL antiguo
    session = requests.Session()
    session.mount('https://', TLSAdapter())

    response = session.get(url, params=params, verify=False)
    data = response.json()

    total_activas = data["response"]["numFound"]
    docs = data["response"]["docs"]

    print(f"Total de ofertas activas: {total_activas:,}\n")

    for i, doc in enumerate(docs, 1):
        print(f"{i}. {doc.get('cargo', 'Sin cargo')[:50]}")
        print(f"   Distrito: {doc.get('descdistrito', 'N/A')}")
        print(f"   Escuela: {doc.get('escuela', 'N/A')}")
        print(f"   Cierre: {doc.get('finoferta', 'N/A')}")
        print()


if __name__ == "__main__":
    explorar_api()
    buscar_ofertas_activas()
