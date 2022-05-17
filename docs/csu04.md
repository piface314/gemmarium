## CSU04: Obter Gemas Sorteadas

**Sumário:** O Usuário utiliza o sistema para obter novas gemas sorteadas.

**Ator primário:** Usuário.

**Ator secundário:** Forja.

### Fluxo Principal:
1. O sistema apresenta a tela principal.
2. O Usuário solicita novas gemas sorteadas.
3. _Include_ [CSU13: Autenticar Usuário](#csu13-autenticar-usuário).
4. A Forja sorteia novas gemas e as assina para o usuário, enviando seus dados.
5. O sistema armazena os dados recebidos localmente e os apresenta para o Usuário.
6. O sistema encerra o caso de uso.

### Fluxo de Exceção (4) - Cota excedida:
- Caso o Usuário tenha excedido a cota de solicitações de novas gemas, a Forja informa essa violação, além do tempo deve ser esperado para realizar uma nova solicitação.
- O sistema apresenta o erro, redireciona para a tela principal, e encerra o caso de uso.

**Pós-condições:** novas gemas aleatórias foram adicionadas à coleção do Usuário.
