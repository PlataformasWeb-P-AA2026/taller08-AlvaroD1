from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from db import get_engine
from models import Base, Continente, Jugador, Pais

PROJECT_ROOT = Path(__file__).resolve().parent
CSV_PATH = PROJECT_ROOT / "data" / "jugadores_futbol.csv"

CONTINENTE_POR_PAIS = {
    "Ecuador": "América del Sur",
    "Brasil": "América del Sur",
    "Argentina": "América del Sur",
    "Estados Unidos": "América del Norte",
    "México": "América del Norte",
    "Japón": "Asia",
    "Alemania": "Europa",
    "España": "Europa",
    "Portugal": "Europa",
    "Francia": "Europa",
    "Inglaterra": "Europa",
    "Marruecos": "África",
    "Senegal": "África",
    "Nigeria": "África",
    "Australia": "Oceanía",
}


def validate_countries(df: pd.DataFrame) -> None:
    countries = set(df["pais_nacimiento"].unique()) | set(
        df["pais_donde_juega"].unique()
    )
    missing = sorted(countries - set(CONTINENTE_POR_PAIS))
    if missing:
        raise ValueError(
            "Faltan países en el mapeo de continentes: " + ", ".join(missing)
        )


def main() -> int:
    if not CSV_PATH.exists():
        print(f"No se encontró el archivo CSV en {CSV_PATH}", file=sys.stderr)
        return 1

    df = pd.read_csv(CSV_PATH)
    validate_countries(df)

    engine = get_engine()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        continentes: dict[str, Continente] = {}
        paises: dict[str, Pais] = {}

        for pais, continente in CONTINENTE_POR_PAIS.items():
            if continente not in continentes:
                continentes[continente] = Continente(nombre=continente)
                session.add(continentes[continente])

        session.flush()

        for pais, continente in CONTINENTE_POR_PAIS.items():
            pais_obj = Pais(nombre=pais, continente=continentes[continente])
            session.add(pais_obj)
            paises[pais] = pais_obj

        session.flush()

        for row in df.to_dict(orient="records"):
            jugador = Jugador(
                nombre=row["nombre_jugador"],
                pais_nacimiento=paises[row["pais_nacimiento"]],
                pais_donde_juega=paises[row["pais_donde_juega"]],
                posicion=row["posicion"],
                edad=int(row["edad"]),
                numero_partidos_seleccion=int(row["numero_partidos_seleccion"]),
                goles_seleccion=int(row["goles_seleccion"]),
            )
            session.add(jugador)

        session.commit()

    print("Carga completada. Base de datos creada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
