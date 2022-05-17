## CSU10: Tentar Fusão de Gemas

**Sumário:** O Usuário A tenta realizar uma fusão entre as gemas sendo trocadas.

**Ator primário:** Usuário A.

**Atores secundários:** Usuário B e Forja.

### Fluxo Principal:
1. O Usuário A está respondendo uma proposta de troca de gemas.
2. O Usuário A decide tentar uma fusão entre as gemas que estão sendo oferecidas na proposta de troca.
3. O sistema envia uma negociação da proposta ao Usuário B, inserindo automaticamente uma mensagem que informa que Usuário A solicitou uma fusão.
3. O sistema envia a solicitação de fusão à Forja, informando com quem a fusão está sendo tentada, e enviando os dados das gemas que está oferecendo.
4. _Include_ [CSU13: Autenticar Usuário](#csu13-autenticar-usuário).
5. A Forja recebe a solicitação e aguarda a mesma solicitação do Usuário B.
6. Caso ambas as solicitações estejam presentes, a Forja verifica a autencidade de todas as gemas envolvidas.
7. A Forja escolhe uma fusão disponível entre as gemas fornecidas pelos Usuários, e envia os dados da gema resultante da fusão (caso haja), além das gemas trocadas pelos usuários aos seus respectivos destinatários.
8. O sistema recebe as gemas e encerra a proposta de troca como aceita.
4. O sistema encerra o caso de uso.

### Fluxo de exceção (7): Gemas fraudadas.
- Caso a Forja detecte que há gemas fraudadas na troca, um erro é enviado aos Usuários A e B.
- O sistema apresenta o erro ao Usuário A e encerra o caso de uso.

**Pós-condições:** as gemas foram devidamente trocadas, inclusive a gema resultante da fusão, se houver.