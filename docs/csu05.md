## CSU05: Editar Galeria

**Sumário:** o Usuário edita suas gemas possuídas e de interesse na Galeria.

**Ator primário:** Usuário.

**Ator secundário:** Galeria.

### Fluxo Principal:
1. O sistema apresenta a tela principal.
2. O Usuário solicita editar seus dados na Galeria.
3. _Include_ [CSU13: Autenticar Usuário](#csu13-autenticar-usuário).
4. O sistema solicita o estado atual da Galeria.
5. A Galeria informa os nomes das gemas que constam para aquele usuário.
6. O sistema apresenta o estado atual da Galeria ao Usuário, permitindo-o marcar ou desmarcar suas gemas possuídas, e também permitindo-o alterar a listagem das gemas de interesse.
7. O Usuário faz as alterações desejadas.
8. O sistema envia à Galeria a nova listagem de nomes de gemas.
9. A Galeria atualiza as informações, registrando também o IP daquele usuário.
10. O sistema encerra o caso de uso.

**Pós-condições:** a Galeria foi atualizada com base nas alterações feitas.
