"""
Script para enriquecer ofertas con información de cargos
"""
import json
from cargos import CargoRepository


def enriquecer_ofertas(archivo_ofertas='ofertas_muestra.json',
                       archivo_cargos='cargos_ejemplo.json',
                       archivo_salida='ofertas_enriquecidas.json'):
    """
    Enriquece cada oferta con información del cargo correspondiente.
    """

    print("Cargando datos...")

    # Cargar ofertas
    with open(archivo_ofertas, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Cargar cargos
    repo = CargoRepository.load_from_file(archivo_cargos)

    print(f"Ofertas: {len(data['ofertas']):,}")
    print(f"Cargos: {len(repo)}")

    # Enriquecer cada oferta
    ofertas_enriquecidas = []
    match_count = 0

    for oferta in data['ofertas']:
        # Buscar cargo
        cargo_encontrado = repo.buscar_area_exacta(oferta['cargo'])

        if not cargo_encontrado:
            # Intentar por código
            cargo_encontrado = repo.buscar_por_codigo(oferta.get('areaincumbencia', ''))

        # Agregar información del cargo
        oferta_enriquecida = oferta.copy()

        if cargo_encontrado:
            oferta_enriquecida['cargo_info'] = {
                'validado': True,
                'modalidad_cargo': cargo_encontrado.modalidad,
                'codigo_cargo': cargo_encontrado.codigo,
                'valor': cargo_encontrado.valor
            }
            match_count += 1
        else:
            oferta_enriquecida['cargo_info'] = {
                'validado': False,
                'modalidad_cargo': None,
                'codigo_cargo': None,
                'valor': 0.0
            }

        ofertas_enriquecidas.append(oferta_enriquecida)

    # Guardar
    resultado = {
        'metadata': {
            **data['metadata'],
            'ofertas_validadas': match_count,
            'porcentaje_validacion': round((match_count / len(ofertas_enriquecidas)) * 100, 2)
        },
        'ofertas': ofertas_enriquecidas
    }

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Ofertas enriquecidas guardadas en: {archivo_salida}")
    print(f"  Validadas: {match_count}/{len(ofertas_enriquecidas)} ({resultado['metadata']['porcentaje_validacion']}%)")


if __name__ == "__main__":
    enriquecer_ofertas()
