# CSU02: Autenticação de Usuário

**Sumário:** Usuário utiliza o sistema para fazer a autenticação e ter acesso à aplicação.

**Ator primário:** Usuário.

## Fluxo principal:
1. O sistema apresenta uma página inicial dando boas vindas e caixas de entrada para inserir nome de usuário e senha.
2. O Usuário insere o nome de usuário e a senha.
3. O sistema informa que a autenticação foi realizada com sucesso e redireciona para a tela principal.
4. O sistema encerra o caso de uso.

## Fluxo de Exceção (3): Credenciais incorretas
- Caso as credenciais informadas não estejam cadastradas, o sistema apresenta um aviso de erro e encerra o caso de uso.

**Pós-condições:** o Usuário foi autenticado no sistema.