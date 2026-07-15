from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dados.banco import Base


class VendaModel(Base):
    __tablename__ = "venda"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vendedor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuario.id"), nullable=False
    )
    data: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    cpf_cliente: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)

    vendedor: Mapped["UsuarioModel"] = relationship(back_populates="vendas")
