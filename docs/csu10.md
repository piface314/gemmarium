## CSU10: Fundir Gemas

**Sumário:** O Usuário tenta realizar uma fusão entre as gemas sendo trocadas.

**Ator primário:** Usuário.

**Ator secundário:** Forja.

**Precondições:** Existe(m) troca(s) pendente(s) para o Usuário.

### Fluxo Principal:
1. O Usuário está visualizando uma troca em aberto.
2. O Usuário decide tentar uma fusão entre as gemas que estão sendo oferecidas na proposta de troca.
3. O sistema notifica ao outro usuário que uma fusão está sendo tentada.
4. O sistema envia a solicitação de fusão à Forja, informando com quem a fusão está sendo tentada, e enviando os dados das gemas que está oferecendo.
5. _Include_ [CSU13: Autenticar Usuário](#csu13-autenticar-usuário).
6. A Forja recebe a solicitação e aguarda a mesma solicitação do outro usuário.
7. Caso ambas as solicitações estejam presentes, a Forja verifica a autencidade de todas as gemas envolvidas.
8. A Forja escolhe uma fusão disponível entre as gemas fornecidas pelos usuários, e envia os dados da gema resultante da fusão (caso haja), além das gemas trocadas pelos usuários aos seus respectivos destinatários.
9. O sistema recebe as gemas e encerra a proposta de troca como aceita.
10. O sistema encerra o caso de uso.

### Fluxo de exceção (8): Gemas fraudadas.
- Caso a Forja detecte que há gemas fraudadas na troca, um erro é enviado aos usuários.
- O sistema apresenta o erro ao Usuário e encerra o caso de uso, concluindo a troca como rejeitada.

**Pós-condições:** A troca foi aceita e as gemas foram devidamente trocadas, incluindo a gema resultante da fusão, se houver.