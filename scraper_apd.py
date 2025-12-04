import requests
import json
import time
from datetime import datetime
import urllib3
import ssl
from requests.adapters import HTTPAdapter
import re
from config import API_ENDPOINT

# Deshabilitar advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TLSAdapter(HTTPAdapter):
    """Adapter que fuerza TLS 1.0/1.1/1.2 para servidores con SSL antiguo"""

    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        # Permitir TLS 1.0 y superiores
        ctx.minimum_version = ssl.TLSVersion.TLSv1
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)


class APDScraper:
    """Scraper para Actos Públicos Digitales de ABC Buenos Aires"""

    def __init__(self):
        self.base_url = API_ENDPOINT
        self.session = requests.Session()
        self.session.mount("https://", TLSAdapter())
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "Referer": "http://servicios.abc.gob.ar/",
            }
        )

    def get_ofertas(self, start=0, rows=100, filtros=None):
        """
        Obtiene ofertas de la API

        Args:
            start: Índice de inicio (paginación)
            rows: Cantidad de resultados por página
            filtros: Dict con filtros adicionales

        Returns:
            Dict con la respuesta JSON
        """
        params = {
            "q": "*:*",  # Query básica: todos los registros
            "rows": rows,
            "start": start,
            "wt": "json",
            "json.nl": "map",
            "sort": "finoferta desc",  # Ordenar por fecha de cierre
        }

        # Agregar filtros si existen
        if filtros:
            fq_filters = []
            if "distrito" in filtros:
                fq_filters.append(f'descdistrito:"{filtros["distrito"]}"')
            if "estado" in filtros:
                fq_filters.append(f'estado:"{filtros["estado"]}"')
            if "cargo" in filtros:
                fq_filters.append(f'cargo:"{filtros["cargo"]}"')
            if "areaincumbencia" in filtros:
                fq_filters.append(f'areaincumbencia:"{filtros["areaincumbencia"]}"')
            if 'idoferta' in filtros:
                fq_filters.append(f'idoferta:"{filtros["idoferta"]}"')

            # Unir todos los filtros con AND
            if fq_filters:
                params["fq"] = " AND ".join(fq_filters)

        try:
            response = self.session.get(
                self.base_url, params=params, timeout=30, verify=False
            )
            response.raise_for_status()

            # El servidor envía los datos en ISO-8859-1 (Latin-1)
            response.encoding = 'ISO-8859-1'

            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            print(f"Error en la petición: {e}")
            return None

    def get_all_ofertas(self, batch_size=100, max_ofertas=None, filtros=None):
        """
        Obtiene todas las ofertas disponibles

        Args:
            batch_size: Cantidad de registros por petición
            max_ofertas: Límite máximo de ofertas a extraer (None = todas)
            filtros: Dict con filtros adicionales

        Yields:
            Dict con cada oferta
        """
        start = 0
        total_found = None
        ofertas_extraidas = 0

        while True:
            print(f"Extrayendo ofertas desde {start}...")

            data = self.get_ofertas(start=start, rows=batch_size, filtros=filtros)

            if not data or "response" not in data:
                print("No se pudo obtener datos o fin de resultados")
                break

            response = data["response"]

            # Primera vez: obtener total de registros
            if total_found is None:
                total_found = response["numFound"]
                print(f"Total de ofertas encontradas: {total_found:,}")

            docs = response.get("docs", [])

            if not docs:
                print("No hay más ofertas")
                break

            for doc in docs:
                yield doc
                ofertas_extraidas += 1

                # Verificar límite máximo
                if max_ofertas and ofertas_extraidas >= max_ofertas:
                    print(f"Alcanzado límite de {max_ofertas} ofertas")
                    return

            start += batch_size

            # Verificar si ya extrajimos todo
            if start >= total_found:
                print("Todas las ofertas extraídas")
                break

            # Pausa para no saturar el servidor
            time.sleep(0.5)

    def save_to_json(self, filename, filtros=None, max_ofertas=None):
        """
        Guarda todas las ofertas en un archivo JSON

        Args:
            filename: Nombre del archivo de salida
            filtros: Dict con filtros adicionales
            max_ofertas: Límite máximo de ofertas
        """
        ofertas = []

        print("Iniciando extracción de ofertas...")
        start_time = time.time()

        for i, oferta in enumerate(
            self.get_all_ofertas(max_ofertas=max_ofertas, filtros=filtros), 1
        ):
            ofertas.append(oferta)

            if i % 1000 == 0:
                print(f"Extraídas {i:,} ofertas...")

        # Guardar en archivo
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "metadata": {
                        "total_ofertas": len(ofertas),
                        "fecha_extraccion": datetime.now().isoformat(),
                        "filtros": filtros,
                    },
                    "ofertas": ofertas,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        elapsed = time.time() - start_time
        print("\n>> Extraccion completada!")
        print(f"Total ofertas: {len(ofertas):,}")
        print(f"Tiempo: {elapsed:.2f} segundos")
        print(f"Archivo guardado: {filename}")

    def get_filtros_disponibles(self):
        """
        Obtiene valores únicos para usar como filtros
        """
        # Obtener una muestra para ver qué filtros están disponibles
        data = self.get_ofertas(start=0, rows=0)

        if data and "response" in data:
            print(f"Total de ofertas en la base: {data['response']['numFound']:,}")

            # Puedes agregar facets para obtener valores únicos
            # Esto requeriría modificar la query


# Ejemplo de uso
if __name__ == "__main__":
    scraper = APDScraper()

    # Opción 1: Extraer TODAS las ofertas (puede ser ~721,000 según tu respuesta)
    # scraper.save_to_json('ofertas_completas.json')

    # Opción 2: Extraer solo las primeras 1000 ofertas (para pruebas)
    scraper.save_to_json(
        "ofertas_muestra.json", max_ofertas=1000, filtros={"estado": "Publicada"}
    )

    # Opción 3: Extraer con filtros específicos
    # scraper.save_to_json(
    #     'ofertas_activas_la_plata.json',
    #     filtros={'estado': 'Publicada', 'distrito': 'LA PLATA'},
    #     max_ofertas=5000
    # )

    print("\n>> Datos disponibles en cada oferta:")
    print("- Estado, tipo de oferta, cargo")
    print("- Distrito, escuela, IGE")
    print("- Fechas de inicio y cierre")
    print("- Horarios, turnos, jornadas")
    print("- Informacion del reemplazado")
    print("- Y mas...")
