from typing import Optional

from dados.usuario_repository import UsuarioRepository
from dados.venda_repository import VendaRepository
from dominio.usuario import Usuario


class UsuarioService:
    """Camada de negócio: aplica validações e regras simples."""

    TAMANHO_MINIMO_SENHA = 6

    def __init__(self, repositorio: UsuarioRepository, repo_venda: Optional[VendaRepository] = None) -> None:
        self.repositorio = repositorio
        self.repo_venda = repo_venda

    def cadastrar_usuario(self, login: str, senha: str, nome_completo: str) -> Usuario:
        login_limpo = login.strip()
        if not login_limpo:
            raise ValueError("O login nao pode ficar vazio.")

        nome_limpo = nome_completo.strip()
        if not nome_limpo:
            raise ValueError("O nome completo nao pode ficar vazio.")

        if len(senha) < self.TAMANHO_MINIMO_SENHA:
            raise ValueError(f"A senha deve ter pelo menos {self.TAMANHO_MINIMO_SENHA} caracteres.")

        if self.repositorio.buscar_por_login(login_limpo) is not None:
            raise ValueError(f"Já existe um usuário cadastrado com o login '{login_limpo}'.")

        usuario = Usuario(id=None, login=login_limpo, senha=senha, nome_completo=nome_limpo)
        novo_id = self.repositorio.adicionar(usuario)
        usuario.id = novo_id
        return usuario

    def listar_usuarios(self) -> list[Usuario]:
        return self.repositorio.listar_todos()

    def buscar_usuarios_por_texto(self, texto: str) -> list[Usuario]:
        return self.repositorio.buscar_por_texto(texto)

    def buscar_usuario_por_id(self, id_usuario: int) -> Optional[Usuario]:
        if id_usuario <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")
        return self.repositorio.buscar_por_id(id_usuario)

    def atualizar_usuario(self, id_usuario: int, login: str, senha: str, nome_completo: str) -> bool:
        if id_usuario <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")

        login_limpo = login.strip()
        if not login_limpo:
            raise ValueError("O login nao pode ficar vazio.")

        nome_limpo = nome_completo.strip()
        if not nome_limpo:
            raise ValueError("O nome completo nao pode ficar vazio.")

        if len(senha) < self.TAMANHO_MINIMO_SENHA:
            raise ValueError(f"A senha deve ter pelo menos {self.TAMANHO_MINIMO_SENHA} caracteres.")

        usuario_com_login = self.repositorio.buscar_por_login(login_limpo)
        if usuario_com_login is not None and usuario_com_login.id != id_usuario:
            raise ValueError(f"Já existe um usuário cadastrado com o login '{login_limpo}'.")

        usuario = Usuario(id=id_usuario, login=login_limpo, senha=senha, nome_completo=nome_limpo)
        return self.repositorio.atualizar(usuario)

    def remover_usuario(self, id_usuario: int, usuario_logado_id: Optional[int] = None) -> bool:
        if id_usuario <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")

        if usuario_logado_id is not None and id_usuario == usuario_logado_id:
            raise ValueError("Você não pode remover o próprio usuário logado.")

        if self.repo_venda is not None and self.repo_venda.existe_venda_para_vendedor(id_usuario):
            raise ValueError("Não é possível remover um usuário que possui vendas registradas.")

        return self.repositorio.remover(id_usuario)
