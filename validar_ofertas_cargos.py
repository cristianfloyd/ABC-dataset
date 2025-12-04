"""
Script para validar ofertas contra la lista de cargos conocidos
"""
import json
import pandas as pd
from cargos import CargoRepository


def validar_ofertas_con_cargos(
    archivo_ofertas='ofertas_muestra.json',
    archivo_cargos='cargos_ejemplo.json'
):
    """
    Valida las ofertas contra los cargos conocidos y genera un reporte.
    """

    print("Cargando datos...")

    # Cargar ofertas
    with open(archivo_ofertas, 'r', encoding='utf-8') as f:
        data_ofertas = json.load(f)

    df_ofertas = pd.DataFrame(data_ofertas['ofertas'])
    print(f"Total ofertas: {len(df_ofertas):,}")

    # Cargar cargos
    repo = CargoRepository.load_from_file(archivo_cargos)
    print(f"Total cargos conocidos: {len(repo)}")

    # Validar cada oferta
    print("\n" + "="*70)
    print("VALIDANDO OFERTAS")
    print("="*70)

    resultados = []

    for idx, row in df_ofertas.iterrows():
        cargo_oferta = row['cargo']
        area_incumbencia = row.get('areaincumbencia', '')

        # Buscar coincidencia exacta por área
        cargo_encontrado = repo.buscar_area_exacta(cargo_oferta)

        # Si no se encuentra, buscar por código
        if not cargo_encontrado and area_incumbencia:
            cargo_encontrado = repo.buscar_por_codigo(area_incumbencia)

        resultado = {
            'ige': row['ige'],
            'cargo_oferta': cargo_oferta,
            'codigo_oferta': area_incumbencia,
            'distrito': row['descdistrito'],
            'modalidad': row['descnivelmodalidad'],
            'validado': cargo_encontrado is not None,
            'cargo_conocido': cargo_encontrado.to_dict() if cargo_encontrado else None
        }

        resultados.append(resultado)

    df_resultados = pd.DataFrame(resultados)

    # Estadísticas
    print("\n" + "="*70)
    print("ESTADÍSTICAS DE VALIDACIÓN")
    print("="*70)

    total = len(df_resultados)
    validadas = df_resultados['validado'].sum()
    no_validadas = total - validadas

    print(f"\nTotal ofertas: {total:,}")
    print(f"Ofertas validadas: {validadas:,} ({(validadas/total)*100:.1f}%)")
    print(f"Ofertas NO validadas: {no_validadas:,} ({(no_validadas/total)*100:.1f}%)")

    # Cargos más frecuentes no validados
    if no_validadas > 0:
        print("\n>> TOP 10 CARGOS NO VALIDADOS:")
        cargos_no_validados = df_resultados[~df_resultados['validado']]['cargo_oferta']
        print(cargos_no_validados.value_counts().head(10))

    # Modalidades de ofertas no validadas
    if no_validadas > 0:
        print("\n>> DISTRIBUCIÓN POR MODALIDAD (No validadas):")
        modalidades_no_val = df_resultados[~df_resultados['validado']]['modalidad']
        print(modalidades_no_val.value_counts())

    # Guardar resultados
    archivo_reporte = 'reporte_validacion_cargos.json'
    print(f"\nGuardando reporte en {archivo_reporte}...")

    reporte = {
        'metadata': {
            'total_ofertas': total,
            'ofertas_validadas': int(validadas),
            'ofertas_no_validadas': int(no_validadas),
            'porcentaje_validadas': round((validadas/total)*100, 2)
        },
        'resultados': resultados
    }

    with open(archivo_reporte, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    # Exportar CSV
    df_resultados.to_csv('reporte_validacion_cargos.csv', index=False, encoding='utf-8-sig')
    print("✓ Reporte guardado: reporte_validacion_cargos.json")
    print("✓ CSV exportado: reporte_validacion_cargos.csv")

    return df_resultados


def sugerir_cargos_faltantes(
    archivo_ofertas='ofertas_muestra.json',
    archivo_cargos='cargos_ejemplo.json'
):
    """
    Sugiere qué cargos faltan agregar basándose en las ofertas.
    """

    df_resultados = validar_ofertas_con_cargos(archivo_ofertas, archivo_cargos)

    # Cargos únicos no validados
    cargos_faltantes = df_resultados[~df_resultados['validado']][
        ['cargo_oferta', 'codigo_oferta', 'modalidad']
    ].drop_duplicates()

    print("\n" + "="*70)
    print("SUGERENCIAS DE CARGOS A AGREGAR")
    print("="*70)
    print(f"\nTotal cargos únicos faltantes: {len(cargos_faltantes)}")

    # Generar JSON de sugerencias
    sugerencias = []
    for _, row in cargos_faltantes.iterrows():
        sugerencia = {
            'modalidad': row['modalidad'],
            'codigo': row['codigo_oferta'] if row['codigo_oferta'] else 'DESCONOCIDO',
            'area': row['cargo_oferta'],
            'valor': 1.0
        }
        sugerencias.append(sugerencia)

    # Guardar sugerencias
    with open('cargos_sugeridos.json', 'w', encoding='utf-8') as f:
        json.dump(sugerencias, f, ensure_ascii=False, indent=2)

    print("\n✓ Sugerencias guardadas en: cargos_sugeridos.json")
    print("\nPuedes revisar este archivo y agregar los cargos válidos a cargos_ejemplo.json")


if __name__ == "__main__":
    # Validar ofertas
    validar_ofertas_con_cargos()

    # Generar sugerencias de cargos faltantes
    # sugerir_cargos_faltantes()
