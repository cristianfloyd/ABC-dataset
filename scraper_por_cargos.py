"""
Script para extraer ofertas filtradas por cargos específicos
"""

from scraper_apd import APDScraper
from cargos import CargoRepository
import json
from config import API_ENDPOINT


def extraer_ofertas_por_cargos(
    archivo_cargos="cargos_ejemplo.json",
    archivo_salida="ofertas_por_cargos.json",
    max_por_cargo=150,
):
    """
    Extrae ofertas para cada cargo en el archivo de cargos.

    Args:
        archivo_cargos: Ruta al JSON con los cargos
        archivo_salida: Donde guardar las ofertas
        max_por_cargo: Máximo de ofertas por cargo (None = todas)
    """

    # Cargar cargos
    print("Cargando cargos...")
    repo = CargoRepository.load_from_file(archivo_cargos)
    cargos = list(repo.cargos)
    print(f"Total de cargos: {len(cargos)}")

    # Crear scraper
    scraper = APDScraper()

    # Diccionario para almacenar ofertas por cargo
    ofertas_por_cargo = {}

    # Extraer ofertas para cada cargo
    for i, cargo in enumerate(cargos, 1):
        print(f"\n[{i}/{len(cargos)}] Buscando ofertas para: {cargo.area}")
        print(f"   Modalidad: {cargo.modalidad} | Código: {cargo.codigo}")

        ofertas = []

        # Iterar sobre las ofertas
        try:
            for oferta in scraper.get_all_ofertas(
                filtros={"areaincumbencia": cargo.codigo, "estado": "Publicada"}, max_ofertas=max_por_cargo
            ):
                ofertas.append(oferta)

            if ofertas:
                ofertas_por_cargo[cargo.codigo] = {
                    "cargo": cargo.to_dict(),
                    "total_ofertas": len(ofertas),
                    "ofertas": ofertas,
                }
                print(f"   [OK] Encontradas: {len(ofertas)} ofertas")
            else:
                print("   - Sin ofertas")

        except Exception as e:
            print(f"   [ERROR] {e}")
            continue

    # Guardar resultados
    print(f"\n\nGuardando resultados en {archivo_salida}...")

    # Aplanar la estructura: convertir a lista plana
    todas_ofertas = []
    for info in ofertas_por_cargo.values():
        todas_ofertas.extend(info["ofertas"])

    total_ofertas = len(todas_ofertas)

    # Estructura plana para análisis con Pandas
    from datetime import datetime
    resultado = {
        "metadata": {
            "total_cargos_buscados": len(cargos),
            "cargos_con_ofertas": len(ofertas_por_cargo),
            "total_ofertas": total_ofertas,
            "fecha_extraccion": datetime.now().isoformat()
        },
        "ofertas": todas_ofertas
    }

    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print("\n[OK] Completado!")
    print(f"  Cargos con ofertas: {len(ofertas_por_cargo)}/{len(cargos)}")
    print(f"  Total ofertas: {total_ofertas:,}")


def buscar_ofertas_por_modalidad(
    modalidad="ARTISTICA", archivo_cargos="cargos_ejemplo.json", archivo_salida=None
):
    """
    Extrae ofertas solo para cargos de una modalidad específica.
    """

    if archivo_salida is None:
        archivo_salida = f"ofertas_{modalidad.lower()}.json"

    # Cargar y filtrar cargos
    repo = CargoRepository.load_from_file(archivo_cargos)
    cargos_filtrados = repo.buscar_por_modalidad(modalidad)

    print(f"Cargos de modalidad {modalidad}: {len(cargos_filtrados)}")

    # Crear archivo temporal
    temp_file = "temp_cargos.json"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(
            [c.to_dict() for c in cargos_filtrados], f, ensure_ascii=False, indent=2
        )

    # Extraer
    extraer_ofertas_por_cargos(temp_file, archivo_salida)


if __name__ == "__main__":
    # Opción 1: Extraer para TODOS los cargos (limitando a 50 por cargo)
    # extraer_ofertas_por_cargos(max_por_cargo=50)

    # Opción 2: Solo cargos de ARTISTICA
    buscar_ofertas_por_modalidad("ARTISTICA")

    # Opción 3: Solo cargos de SECUNDARIA
    # buscar_ofertas_por_modalidad('SECUNDARIA')
