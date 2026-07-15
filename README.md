# Titan — Loja de mídia física para música

Aplicação desktop (Tkinter) organizada em três camadas (apresentação, negócio
e dados). A camada de dados usa SQLAlchemy como ORM para conversar com o
MySQL (através do driver `mysql-connector-python`), e o Alembic para
versionar e aplicar mudanças na estrutura do banco por meio de migrations.

## Telas disponíveis

- **Login** — autentica contra a tabela `usuario`. O login local
  `admin` / `1234` funciona apenas em dois casos: banco indisponível, ou
  banco disponível mas ainda sem nenhum usuário cadastrado (primeiro
  acesso, para dar conta de cadastrar o primeiro usuário real). Assim que
  existir ao menos um usuário no banco, esse fallback deixa de valer e
  qualquer credencial que não bata com um usuário real é rejeitada. A
  tela tem um botão "Sair" para encerrar a aplicação sem fazer login.
- **Início** — resumo com total de álbuns, total de vendas e últimas
  atualizações.
- **Álbuns** — cadastrar, buscar, atualizar e excluir álbuns do catálogo
  (não é possível excluir um álbum que tenha itens no estoque ou associados
  a alguma venda).
- **Estoque e catálogo** — ver quantas unidades de cada álbum ainda estão
  disponíveis, dar entrada de novas unidades em estoque e remover unidades
  ainda não vendidas (uma unidade já vendida não pode ser removida do
  estoque).
- **Usuários** — cadastrar, buscar, atualizar e excluir usuários do sistema
  (não é possível excluir o próprio usuário logado nem um usuário que já
  tenha vendas registradas).
- **Vendas** — montar uma venda (o vendedor é sempre o usuário logado,
  associado automaticamente; CPF do cliente é opcional; produtos são
  buscados e adicionados ao carrinho), calcular o total automaticamente e
  finalizar: a venda, a baixa de estoque e a criação dos itens de venda
  acontecem em uma única transação no banco (tudo ou nada).

## Estrutura de pastas

```text
projeto_exemplo_3_camadas/
├── alembic.ini
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 20260714_190000_cria_tabelas_iniciais.py
├── banco_de_dados/
│   └── init.sql
├── docker-compose.yml
├── README.md
├── requirements.txt
└── src/
    ├── main.py
    ├── apresentacao/          # Tkinter: uma pasta por tela
    │   ├── __init__.py
    │   ├── janela_login.py
    │   ├── login.py
    │   ├── album/
    |   |   ├── __init__.py
    |   |   ├── janela_album.py      # classe principal, só monta tudo e faz __init__
    |   |   ├── imagens.py            # carregar_imagem
    |   |   ├── desenho.py             # desenhar_fundo_arredondado
    |   |   ├── modais_base.py         # criar_modal_rolavel, configurar_scrollbar_fina criar_lista_rolavel
    |   |   ├── layout.py              # criar_layout
    |   |   ├── cadastro.py            # abrir_modal_cadastro, confirmar_cadastro
    |   |   ├── atualizacao.py         # abrir_modal_atualizacao
    |   |   ├── exclusao.py            # abrir_modal_confirmacao_exclusao, excluir_album
    |   |   └── listagem.py            # obter_albuns, buscar_albuns, limpar_filtros, atualizar_listagem, parsers
    │   ├── estoque/
    │   │   └── janela_estoque.py
    │   ├── icones/
    │   │   ├── logo.png
    │   │   └── usuario.png
    │   ├── telainicial/
    │   │   └── janela_inicial.py
    │   ├── usuarios/
    │   │   └── janela_usuarios.py
    │   └── vendas/
    │       └── janela_vendas.py
    ├── negocio/               # validações e regras de negócio
    │   ├── album_service.py
    │   ├── estoque_service.py
    │   ├── item_venda_service.py
    │   ├── usuario_service.py
    │   └── venda_service.py
    ├── dados/                 # acesso ao banco via SQLAlchemy (ORM)
    │   ├── banco.py           # engine, SessionLocal, Base
    │   ├── modelos/           # modelos ORM (uma classe por tabela)
    │   │   ├── album_model.py
    │   │   ├── estoque_model.py
    │   │   ├── usuario_model.py
    │   │   ├── venda_model.py
    │   │   └── item_venda_model.py
    │   ├── album_repository.py
    │   ├── estoque_repository.py
    │   ├── item_venda_repository.py
    │   ├── usuario_repository.py
    │   └── venda_repository.py
    └── dominio/               # entidades (dataclasses)
        ├── album.py
        ├── estoque.py
        ├── item_venda.py
        ├── usuario.py
        └── venda.py
```

## Pré-requisitos

- Python 3.10 ou superior;
- Docker e Docker Compose;
- opcionalmente o DBeaver para acessar o MySQL.

## Subir o MySQL

```bash
docker compose up -d
```

O container sobe com:

- host: `127.0.0.1`
- porta: `3306`
- usuário: `root`
- senha: `labinfo`
- banco: `aplicacao`

> O `init.sql` só é executado automaticamente na **primeira** subida do
> container (volume vazio) e cria apenas o banco `aplicacao` vazio. As
> tabelas (`album`, `estoque`, `usuario`, `venda`, `item_venda`) **não**
> são criadas pelo `init.sql` — elas são criadas pela migration do Alembic
> (veja a seção "Instalar dependências e executar o projeto" abaixo).

## Instalar dependências e executar o projeto

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
python src/main.py
```

### Windows Prompt de Comando

```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
alembic upgrade head
python src/main.py
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python src/main.py
```

> `alembic upgrade head` aplica todas as migrations pendentes e cria as
> tabelas do sistema. Rode esse comando sempre que houver uma migration
> nova (por exemplo, após um `git pull`).

## Conexão no DBeaver

- host: `localhost`
- porta: `3306`
- database: `aplicacao`
- username: `root`
- password: `labinfo`

## Como o projeto se organiza

### `src/apresentacao`
Camada de interface gráfica (Tkinter). Cada tela conversa **apenas** com a
camada de negócio (serviços), nunca diretamente com os repositórios.

### `src/negocio`
Camada de regras de negócio. Valida campos obrigatórios, tipos e IDs antes
de acionar a camada de dados. É também aqui que a venda "completa"
(`VendaService.registrar_venda_completa`) orquestra a baixa de estoque e a
criação dos itens de venda.

### `src/dados`
Camada de acesso a dados. `banco.py` cria a `engine` e a `SessionLocal` do
SQLAlchemy; `modelos/` guarda os modelos ORM (uma classe por tabela); os
repositórios recebem uma `Session` e usam o ORM para consultar, inserir,
atualizar e remover registros.

### `src/dominio`
Entidades do domínio da aplicação (dataclasses).

## Alembic e SQLAlchemy

### SQLAlchemy
Biblioteca usada como ORM: em vez de escrever SQL manualmente em cada
repositório, a aplicação trabalha com objetos Python (os modelos em
`src/dados/modelos/`) que representam as tabelas do banco. `src/dados/banco.py`
concentra a configuração: `engine` (conexão com o MySQL), `SessionLocal`
(fábrica de sessões) e `Base` (classe base dos modelos ORM).

### Alembic
Ferramenta de migrations: cada alteração na estrutura do banco (criar
tabela, adicionar coluna, etc.) vira um arquivo versionado dentro de
`alembic/versions/`. Comandos úteis:

```bash
alembic upgrade head                              # aplica as migrations pendentes
alembic revision --autogenerate -m "mensagem"      # gera uma nova migration a partir dos modelos
alembic downgrade -1                               # desfaz a última migration
```

O Alembic mantém no banco uma tabela `alembic_version`, que guarda qual foi
a última migration aplicada.

## Observações

- A camada de dados usa SQLAlchemy (ORM) e Alembic (migrations); a criação
  das tabelas deixou de ser feita em `init.sql` ou em código Python e passou
  a ser responsabilidade das migrations do Alembic.
- O modal de "Nova venda" busca álbuns pelo nome/gênero, mostra a
  disponibilidade em estoque e desabilita o botão "Adicionar" quando não
  há unidades disponíveis.
