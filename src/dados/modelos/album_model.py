from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dados.banco import Base


class AlbumModel(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    genero: Mapped[str] = mapped_column(String(100), nullable=False)
    artista: Mapped[str] = mapped_column(String(255), nullable=False)
    tamanho: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))

    estoques: Mapped[list["EstoqueModel"]] = relationship(back_populates="album")
