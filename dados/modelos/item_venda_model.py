from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dados.banco import Base


class ItemVendaModel(Base):
    __tablename__ = "item_venda"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    venda_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("venda.id"), nullable=False
    )
    item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoque.id"), nullable=False
    )

    venda: Mapped["VendaModel"] = relationship()
    item: Mapped["EstoqueModel"] = relationship()
