# Casos de Uso

Todos os casos de uso serão descritos do ponto de vista da aplicação Cliente, tendo o usuário como ator primário e as partes do sistema (Cofre, Forja e Galeria) como atores secundários, para facilitar o entendimento.

## CSU01: Cadastrar Usuário

**Sumário:** O usuário utiliza o sistema para realizar cadastro.

**Ator primário:** Usuário.

**Atores secundários:** Cofre, Forja e Galeria.

### Fluxo principal:
1. O sistema apresenta uma página inicial com os campos de entrada para nome de usuário e senha.
2. O Usuário insere as credenciais escolhidas.
3. O sistema cria um par de chaves e envia ao Cofre as credenciais e sua chave pública.
4. O Cofre notifica a Forja e a Galeria do registro de um novo usuário, enviando a chave pública do mesmo.
4. O sistema redireciona para a tela de autenticação.
5. O sistema encerra o caso de uso.

**Pós-condições:** o Usuário foi cadastrado no Cofre.
