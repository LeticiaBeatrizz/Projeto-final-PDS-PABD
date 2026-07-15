# Histórias de Usuário

Sistema de gerenciamento de estoque de música em mídia física.

## US01 — Login e Autenticação

Como usuário do sistema, quero informar meu login e senha para acessar o sistema, para que eu possa utilizar as funcionalidades de acordo com meu perfil.

**Regras de negócio:**
- O login deve ser único no banco.
- O sistema deve redirecionar para a interface relacionada ao usuário.

**Critérios de aceitação:**
- Tela inicial solicitando login e senha.
- Mensagem de erro clara para credenciais inválidas.
- Opção de sair (encerrar).

**Done criteria:**
- Teste que verifica login válido e retorna o usuário correto.
- Teste que verifica login inválido retorna 'None'.
- Fluxo completo funcional na interface.


## US02 — Gerenciar Álbuns

Como usuário, quero cadastrar, listar, editar e remover álbuns, para manter o acervo de mídia física organizado.

**Regras de negócio:**
- Os campos nome, gênero, artista, tamanho (faixas) e valor são obrigatórios.
- O tamanho (faixas) deve ser um inteiro maior que zero.
- Só é permitido remover um álbum que não tenha nenhum item no estoque ou que não esteja associado a nenhuma compra.

**Critérios de aceitação:**
- Tela de cadastro com campos: nome, artista(s), gênero, tamanho e valor.
- Tela de listagem exibindo os campos nome, artista(s), gênero, tamanho, valor e estoque (este último relacionado a funcionalidade de estoque).
- Tela de edição com dados preenchidos e possibilidade de alterar.
- Confirmação antes de remover um álbum.
- Mensagens de sucesso/erro.

**Done criteria:**
- Teste que impede cadastro sem campos obrigatórios preenchidos.
- Teste que impede remoção de álbum com estoque ou associado a uma compra.
- Interface funcional.

## US03 — Gerenciar Usuários

Como usuário, quero cadastrar, listar, editar e remover usuários do sistema, para controlar quem pode acessar o sistema.

**Regras de negócio:**
- Login deve ser único.
- A senha deve ter no mínimo 6 caracteres.
- Não é possível remover o próprio usuário logado.
- Não é possível remover um usuário que possua vendas registradas.

**Critérios de aceitação:**
- Tela de cadastro com campos: nome completo, login e senha.
- Tela de listagem com todos os usuários.
- Tela de edição com dados preenchidos.
- Confirmação antes de remover.
- Mensagens de sucesso/erro.

**Done criteria:**
- Testes de banco para CRUD de usuário.
- Teste que impede login duplicado.
- Teste que impede remoção de usuário com vendas.
- Interface funcional.


## US04 — Gerenciar Estoque

Como usuário, quero adicionar e remover unidades (itens individuais) de álbuns no estoque, para controlar a quantidade física disponível de cada álbum.

**Regras de negócio:**
- Só é possível adicionar ao estoque um álbum que exista no catálogo.
- Cada registro na tabela 'estoque' representa uma unidade física individual.
- Não é possível remover um item de estoque que já foi vendido (vinculado a um 'item_venda').

**Critérios de aceitação:**
- Tela com campo de busca/seleção de álbum e botões "Adicionar ao estoque" e “Remover do estoque”.
- Tela de consulta de estoque mostrando álbuns e suas quantidades.
- Opção de remover item individual (com confirmação).

**Done criteria:**
- Testes de banco para inserir e remover itens de estoque.
- Teste que verifica a contagem de itens por álbum.
- Teste que impede remoção de item já vendido.
- Teste de integridade referencial.
- Interface funcional.


## US05 — Realizar Venda

Como vendedor, quero registrar uma venda informando o cliente (CPF opcional) e os itens (discos) comprados,  para dar baixa no estoque e manter o histórico de vendas.

**Regras de negócio:**
- A venda deve ter pelo menos um item.
- O vendedor é automaticamente associado à venda (seleção de usuário).
- A data da venda é gerada automaticamente no momento do registro.
- O CPF do cliente, caso informado, deve ter 11 dígitos.
- Só podem ser vendidos itens que existam no estoque e não tenham sido vendidos antes.
- Ao confirmar a venda, todos os itens devem ser inseridos em 'item_venda' (em uma transação).

**Critérios de aceitação:**
- Tela para iniciar uma nova venda.
- Campo opcional para CPF do cliente.
- Campo de busca para adicionar itens do estoque à venda.
- Listagem dos itens adicionados na venda atual com opção de remover.
- Botão "Finalizar venda" que persiste tudo no banco.
- Mensagem de resumo ao finalizar (vendedor associado, CPF do cliente, itens, total de itens, data).

**Done criteria:**
- Testes de banco para inserir venda + itens_venda em transação.
- Teste que verifica CPF inválido (se informado).
- Teste que impede venda sem itens.
- Teste que verifica se item já vendido não pode ser vendido novamente.
- Interface funcional para o fluxo completo de venda.


## US06 — Consultar Catálogo e Estoque

Como vendedor, quero pesquisar álbuns por nome, artista ou gênero, para consultar o catálogo e verificar a disponibilidade em estoque rapidamente.

**Regras de negócio:**
- A busca deve ser case insensitive.
- Deve ser possível filtrar por nome do álbum, nome do artista ou nome do gênero.
- Deve ser possível refinar por estoque, valor e/ou faixas.
- O resultado deve exibir: nome do álbum, artista(s), gênero, tamanho, valor e quantidade disponível em estoque.
- Se a quantidade disponível for zero, ainda assim o álbum deve aparecer (apenas indicando "Sem estoque ou o numeral ‘0’").

**Critérios de aceitação:**
- Tela com campo de texto para busca.
- Resultados exibidos em formato de lista/tabela com as informações mencionadas.

**Done criteria:**
- Testes de banco para a query de busca (com JOINs).
- Teste que verifica busca por nome retorna resultados corretos.
- Teste que verifica busca sem resultados retorna lista vazia.
- Teste que verifica a contagem de estoque disponível.
- Interface funcional.
