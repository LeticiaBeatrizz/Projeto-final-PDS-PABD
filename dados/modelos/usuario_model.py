from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dados.banco import Base


class UsuarioModel(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_completo: Mapped[str] = mapped_column(String(255), nullable=False)
    login: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)

    vendas: Mapped[list["VendaModel"]] = relationship(back_populates="vendedor")
