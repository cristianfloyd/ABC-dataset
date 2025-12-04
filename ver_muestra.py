"""
Script simple para ver un resumen de las ofertas extraidas
"""
import json
from collections import Counter

with open('ofertas_muestra.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ofertas = data['ofertas']
metadata = data['metadata']

print("="*60)
print("RESUMEN DE OFERTAS EXTRAIDAS")
print("="*60)
print(f"Total: {metadata['total_ofertas']:,} ofertas")
print(f"Fecha extraccion: {metadata['fecha_extraccion']}")
print()

# Ver primeras 3 ofertas resumidas
print(">> PRIMERAS 3 OFERTAS:")
print("-"*60)
for i, oferta in enumerate(ofertas[:3], 1):
    print(f"\n{i}. {oferta.get('cargo', 'Sin cargo')}")
    print(f"   Estado: {oferta.get('estado', 'N/A')}")
    print(f"   Distrito: {oferta.get('descdistrito', 'N/A')}")
    print(f"   Escuela: {oferta.get('escuela', 'N/A')}")
    print(f"   Nivel: {oferta.get('descnivelmodalidad', 'N/A')}")
    print(f"   Cierre: {oferta.get('finoferta', 'N/A')}")
    print(f"   IGE: {oferta.get('ige', 'N/A')}")

# Estadisticas
print("\n" + "="*60)
print("ESTADISTICAS")
print("="*60)

estados = Counter(o.get('estado') for o in ofertas)
print("\nPor Estado:")
for estado, cant in estados.most_common():
    pct = (cant/len(ofertas))*100
    print(f"  {estado:20} {cant:5} ({pct:5.1f}%)")

print("\nTop 10 Distritos:")
distritos = Counter(o.get('descdistrito') for o in ofertas)
for distrito, cant in distritos.most_common(10):
    print(f"  {distrito:30} {cant:4}")

print("\nTop 10 Cargos:")
cargos = Counter(o.get('cargo') for o in ofertas)
for cargo, cant in cargos.most_common(10):
    cargo_txt = (cargo[:40] + '...') if len(cargo) > 40 else cargo
    print(f"  {cargo_txt:43} {cant:4}")
