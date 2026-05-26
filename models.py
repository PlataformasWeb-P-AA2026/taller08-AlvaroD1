from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Continente(Base):
    __tablename__ = "continentes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    paises: Mapped[list["Pais"]] = relationship(
        back_populates="continente", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Continente(id={self.id}, nombre={self.nombre!r})"


class Pais(Base):
    __tablename__ = "paises"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    continente_id: Mapped[int] = mapped_column(
        ForeignKey("continentes.id"), nullable=False
    )

    continente: Mapped[Continente] = relationship(back_populates="paises")

    jugadores_nacimiento: Mapped[list["Jugador"]] = relationship(
        back_populates="pais_nacimiento",
        foreign_keys="Jugador.pais_nacimiento_id",
    )
    jugadores_club: Mapped[list["Jugador"]] = relationship(
        back_populates="pais_donde_juega",
        foreign_keys="Jugador.pais_donde_juega_id",
    )

    def __repr__(self) -> str:
        return f"Pais(id={self.id}, nombre={self.nombre!r})"


class Jugador(Base):
    __tablename__ = "jugadores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    posicion: Mapped[str] = mapped_column(String(60), nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    numero_partidos_seleccion: Mapped[int] = mapped_column(Integer, nullable=False)
    goles_seleccion: Mapped[int] = mapped_column(Integer, nullable=False)

    pais_nacimiento_id: Mapped[int] = mapped_column(
        ForeignKey("paises.id"), nullable=False
    )
    pais_donde_juega_id: Mapped[int] = mapped_column(
        ForeignKey("paises.id"), nullable=False
    )

    pais_nacimiento: Mapped[Pais] = relationship(
        back_populates="jugadores_nacimiento",
        foreign_keys=[pais_nacimiento_id],
    )
    pais_donde_juega: Mapped[Pais] = relationship(
        back_populates="jugadores_club",
        foreign_keys=[pais_donde_juega_id],
    )

    def __repr__(self) -> str:
        return f"Jugador(id={self.id}, nombre={self.nombre!r})"
