# Clase con los cargos disponibles para el titulo de docente
# que se utilizaran para filtrar las ofertas

import json
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass(frozen=True)
class Cargo:
    modalidad: str
    codigo: str
    area: str
    valor: float = 1.0

    def contiene(self, palabra: str) -> bool:
        """Devuelve True si la palabra está en el área."""
        return palabra.lower() in self.area.lower()

    def es_modalidad(self, modalidad: str) -> bool:
        return self.modalidad.lower() == modalidad.lower()

    def es_codigo(self, codigo: str) -> bool:
        return self.codigo.lower() == codigo.lower()

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Cargo":
        return Cargo(
            modalidad=data["modalidad"],
            codigo=data["codigo"],
            area=data["area"],
            valor=data.get("valor", 1.0),
        )


class CargoRepository:
    """
    Repositorio para manejar una colección de cargos.
    Provee métodos de filtrado y búsqueda.
    Persistencia en JSON.
    """

    def __init__(self, cargos: List[Cargo], filepath: Optional[str] = None):
        self.cargos = cargos
        self.filepath = filepath

    # ------------------------------------------------
    # Métodos de Persistencia
    # ------------------------------------------------

    def save(self) -> None:
        """Guarda la lista completa de cargos en un archivo JSON."""
        data = [c.to_dict() for c in self.cargos]

        if not self.filepath:
            raise ValueError("No se especificó filepath")

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self) -> List[Cargo]:
        """Carga los cargos desde un archivo JSON."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Cargo.from_dict(item) for item in data]
        except FileNotFoundError:
            return []

    @staticmethod
    def load_from_file(filepath: str) -> "CargoRepository":
        """
        Carga cargos desde un archivo JSON.
        Soporta tanto el formato plano (lista) como el nuevo formato (con metadata).
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        cargos = []

        # Detectar formato
        if isinstance(data, list):
            # Formato antiguo: lista plana de cargos
            cargos = [Cargo.from_dict(item) for item in data]
        elif isinstance(data, dict):
            # Formato nuevo: con metadata, habilitantes y bonificantes
            if "habilitantes" in data:
                cargos.extend([Cargo.from_dict(item) for item in data["habilitantes"]])
            if "bonificantes" in data:
                cargos.extend([Cargo.from_dict(item) for item in data["bonificantes"]])

        return CargoRepository(cargos, filepath)

    # ------------------------------------------------
    # Métodos de Búsqueda / Filtro
    # ------------------------------------------------

    def buscar_por_palabra(self, palabra: str) -> List[Cargo]:
        palabra_lower = palabra.lower()
        return [c for c in self.cargos if
                palabra_lower in c.area.lower() or
                palabra_lower in c.codigo.lower() or
                palabra_lower in c.modalidad.lower()]

    def buscar_por_modalidad(self, modalidad: str) -> List[Cargo]:
        return [c for c in self.cargos if c.es_modalidad(modalidad)]

    def buscar_por_codigo(self, codigo: str) -> Optional[Cargo]:
        for c in self.cargos:
            if c.es_codigo(codigo):
                return c
        return None  # No encontrado

    def listar_modalidades(self) -> List[str]:
        return sorted(set(c.modalidad for c in self.cargos))

    def listar_codigos(self) -> List[str]:
        return sorted(c.codigo for c in self.cargos)

    def buscar_area_exacta(self, area: str) -> Optional[Cargo]:
        area_lower = area.lower()
        for c in self.cargos:
            if c.area.lower() == area_lower:
                return c
        return None

    # ------------------------------------------------
    # Utilidades
    # ------------------------------------------------

    def as_dict(self) -> List[dict]:
        return [c.__dict__ for c in self.cargos]

    def __len__(self):
        return len(self.cargos)

    def __iter__(self):
        return iter(self.cargos)
