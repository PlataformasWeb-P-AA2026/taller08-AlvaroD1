from __future__ import annotations

import pandas as pd
import streamlit as st
from sqlalchemy import func, select
from sqlalchemy.orm import Session, aliased

from db import get_engine
from models import Continente, Jugador, Pais

st.set_page_config(page_title="Jugadores y continentes", layout="wide")

st.title("Integración de datos y ORM")

engine = get_engine()


def fetch_dataframe(stmt) -> pd.DataFrame:
    with Session(engine) as session:
        rows = session.execute(stmt).mappings().all()
    return pd.DataFrame(rows)


birth = aliased(Pais)
club = aliased(Pais)

jugadores_stmt = (
    select(
        Jugador.nombre.label("nombre_jugador"),
        birth.nombre.label("pais_nacimiento"),
        club.nombre.label("pais_donde_juega"),
        Jugador.posicion.label("posicion"),
        Jugador.edad.label("edad"),
        Jugador.numero_partidos_seleccion.label("numero_partidos_seleccion"),
        Jugador.goles_seleccion.label("goles_seleccion"),
        Continente.nombre.label("continente"),
    )
    .join(birth, Jugador.pais_nacimiento)
    .join(club, Jugador.pais_donde_juega)
    .join(Continente, birth.continente)
    .order_by(Jugador.nombre)
)

continentes_stmt = (
    select(
        Continente.nombre.label("continente"),
        func.count(Jugador.id).label("numero_jugadores"),
        func.sum(Jugador.goles_seleccion).label("goles_total"),
    )
    .join(Pais, Pais.continente_id == Continente.id)
    .join(Jugador, Jugador.pais_nacimiento_id == Pais.id)
    .group_by(Continente.nombre)
    .order_by(Continente.nombre)
)

paises_stmt = (
    select(
        Pais.nombre.label("pais"),
        func.count(Jugador.id).label("numero_jugadores"),
        func.sum(Jugador.goles_seleccion).label("goles_total"),
    )
    .join(Jugador, Jugador.pais_nacimiento_id == Pais.id)
    .group_by(Pais.nombre)
    .order_by(Pais.nombre)
)

try:
    st.subheader("Jugadores")
    st.dataframe(fetch_dataframe(jugadores_stmt), use_container_width=True)

    st.subheader("Resumen por continente (país de nacimiento)")
    st.dataframe(fetch_dataframe(continentes_stmt), use_container_width=True)

    st.subheader("Resumen por país (país de nacimiento)")
    st.dataframe(fetch_dataframe(paises_stmt), use_container_width=True)
except Exception as exc:  # pragma: no cover - UI feedback
    st.error(
        "No se pudo consultar la base de datos. "
        "Ejecuta primero `python load_data.py` y verifica el `DATABASE_URL` si usas MySQL/MariaDB."
    )
    st.exception(exc)
