"""
Script para parsear HTML de cargos y generar JSON
"""
from bs4 import BeautifulSoup
import json
import re


def parse_cargos_html(html_content):
    """
    Parsea el HTML de cargos y extrae habilitantes y bonificantes.

    Returns:
        tuple: (cargos_habilitantes, cargos_bonificantes)
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Encontrar las dos tablas (habilitantes y bonificantes)
    tablas = soup.find_all('table', {'style': lambda x: x and 'background-color: #ECF8D9' in x})

    cargos_habilitantes = []
    cargos_bonificantes = []

    # Procesar tabla de habilitantes (primera tabla)
    if len(tablas) > 0:
        rows = tablas[0].find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                modalidad = cols[0].get_text(strip=True)
                area_text = cols[1].get_text(strip=True)
                puntaje = cols[2].get_text(strip=True)

                # Extraer código del área (está en azul)
                codigo_match = re.search(r'\(([^)]+)\)', area_text)
                codigo = codigo_match.group(1) if codigo_match else ''

                # Limpiar área (quitar el código)
                area = re.sub(r'\([^)]+\)\s*', '', area_text).strip()

                cargo = {
                    'modalidad': modalidad,
                    'codigo': codigo,
                    'area': area,
                    'valor': float(puntaje)
                }
                cargos_habilitantes.append(cargo)

    # Procesar tabla de bonificantes (segunda tabla)
    if len(tablas) > 1:
        rows = tablas[1].find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                modalidad = cols[0].get_text(strip=True)
                area_text = cols[1].get_text(strip=True)
                puntaje = cols[2].get_text(strip=True)

                # Extraer código del área
                codigo_match = re.search(r'\(([^)]+)\)', area_text)
                codigo = codigo_match.group(1) if codigo_match else ''

                # Limpiar área
                area = re.sub(r'\([^)]+\)\s*', '', area_text).strip()

                cargo = {
                    'modalidad': modalidad,
                    'codigo': codigo,
                    'area': area,
                    'valor': float(puntaje)
                }
                cargos_bonificantes.append(cargo)

    return cargos_habilitantes, cargos_bonificantes


def generar_json_cargos(html_file, output_file='cargos_completos.json'):
    """
    Lee el HTML y genera el JSON de cargos.
    """
    print(f"Leyendo HTML desde: {html_file}")

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    habilitantes, bonificantes = parse_cargos_html(html_content)

    print(f"\nCargos habilitantes: {len(habilitantes)}")
    print(f"Cargos bonificantes: {len(bonificantes)}")

    # Crear estructura del JSON
    resultado = {
        'metadata': {
            'total_habilitantes': len(habilitantes),
            'total_bonificantes': len(bonificantes),
            'descripcion': 'Cargos docentes - Titulo de Danza'
        },
        'habilitantes': habilitantes,
        'bonificantes': bonificantes
    }

    # Guardar JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)

    print(f"\n[OK] JSON generado: {output_file}")

    # Mostrar resumen
    print("\n=== RESUMEN HABILITANTES ===")
    modalidades_h = {}
    for cargo in habilitantes:
        modalidades_h[cargo['modalidad']] = modalidades_h.get(cargo['modalidad'], 0) + 1

    for mod, count in sorted(modalidades_h.items()):
        print(f"  {mod:30} {count:3} cargos")

    print("\n=== RESUMEN BONIFICANTES ===")
    modalidades_b = {}
    for cargo in bonificantes:
        modalidades_b[cargo['modalidad']] = modalidades_b.get(cargo['modalidad'], 0) + 1

    for mod, count in sorted(modalidades_b.items()):
        print(f"  {mod:30} {count:3} cargos")


def parse_desde_string(html_string):
    """
    Parsea directamente desde un string HTML.
    Útil para copiar/pegar el HTML.
    """
    habilitantes, bonificantes = parse_cargos_html(html_string)

    # Combinar todos en un solo array (formato cargos_ejemplo.json)
    todos_cargos = []

    # Agregar habilitantes
    for cargo in habilitantes:
        todos_cargos.append(cargo)

    # Guardar
    with open('cargos_generados.json', 'w', encoding='utf-8') as f:
        json.dump(todos_cargos, f, ensure_ascii=False, indent=4)

    print(f"[OK] Generados {len(todos_cargos)} cargos en cargos_generados.json")

    return todos_cargos


if __name__ == "__main__":
    # Generar JSON desde el archivo HTML guardado
    generar_json_cargos('cargos_tabla.html', 'cargos_ejemplo.json')
