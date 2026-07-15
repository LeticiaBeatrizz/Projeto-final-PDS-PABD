from dados.banco import SessionLocal
from dados.usuario_repository import UsuarioRepository

class Login:
    def __init__(self, usuario=None, senha=None):
        self.usuario = usuario
        self.senha = senha

    #1. Autenticação do usuário, verificando no banco de dados e no administrador padrão
    def autenticar(self, usuario, senha):
        session = SessionLocal()
        banco_disponivel = True
        nenhum_usuario_cadastrado = False
        try:
            repositorio = UsuarioRepository(session)
            usuarios = repositorio.listar_todos()

            for u in usuarios:
                if u.login == usuario and u.senha == senha:
                    return {"id": u.id, "login": u.login, "nome_completo": u.nome_completo}

            nenhum_usuario_cadastrado = len(usuarios) == 0

        except Exception as e:
            banco_disponivel = False
            print(f"Aviso: Banco indisponível, testando administrador padrão local. Erro: {e}")
        finally:
            session.close()

        # O admin/1234 local so e um fallback valido em dois casos:
        # 1) o banco esta REALMENTE indisponivel (excecao acima); ou
        # 2) o banco esta no ar mas a tabela 'usuario' ainda esta vazia
        #    (primeiro acesso, logo apos as migrations -- sem isso ninguem
        #    conseguiria logar para cadastrar o primeiro usuario).
        # Assim que existir pelo menos um usuario real cadastrado, esse
        # fallback deixa de valer e uma credencial que nao bate com nenhum
        # usuario do banco sempre retorna None.
        if (not banco_disponivel or nenhum_usuario_cadastrado) and usuario == "admin" and senha == "1234":
            return {"id": None, "login": "admin", "nome_completo": "Administrador Padrão"}

        return None