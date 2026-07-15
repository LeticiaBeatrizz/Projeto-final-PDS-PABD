"""cria tabelas iniciais (album, estoque, usuario, venda, item_venda)

Revision ID: 20260714_190000
Revises:
Create Date: 2026-07-14 19:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260714_190000"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "album",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("genero", sa.String(length=100), nullable=False),
        sa.Column("artista", sa.String(length=255), nullable=False),
        sa.Column("tamanho", sa.Integer(), nullable=False),
        sa.Column("preco", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "usuario",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome_completo", sa.String(length=255), nullable=False),
        sa.Column("login", sa.String(length=100), nullable=False),
        sa.Column("senha", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("login"),
    )

    op.create_table(
        "estoque",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("album_id", sa.Integer(), nullable=False),
        sa.Column("vendido", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["album_id"], ["album.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "venda",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("vendedor_id", sa.Integer(), nullable=False),
        sa.Column("data", sa.DateTime(), nullable=True),
        sa.Column("cpf_cliente", sa.String(length=11), nullable=True),
        sa.ForeignKeyConstraint(["vendedor_id"], ["usuario.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "item_venda",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("venda_id", sa.Integer(), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["venda_id"], ["venda.id"]),
        sa.ForeignKeyConstraint(["item_id"], ["estoque.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("item_venda")
    op.drop_table("venda")
    op.drop_table("estoque")
    op.drop_table("usuario")
    op.drop_table("album")
