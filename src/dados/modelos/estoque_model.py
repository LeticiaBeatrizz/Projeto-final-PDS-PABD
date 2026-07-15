from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dados.banco import Base


class EstoqueModel(Base):
    __tablename__ = "estoque"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    album_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("album.id"), nullable=False
    )
    vendido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    album: Mapped["AlbumModel"] = relationship(back_populates="estoques")
