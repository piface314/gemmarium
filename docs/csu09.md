## CSU09: Concluir Troca

**Sumário:** O Usuário A utiliza o sistema para encerrar uma troca rejeitada ou aceita pelo Usuário B.

**Ator primário:** Usuário A.

**Ator secundário:** Usuário B.

### Fluxo Principal
1. Na tela principal, o sistema apresenta as solicitações de troca rejeitadas ou aceitas para o Usuário A.
2. O Usuário A seleciona uma solicitação de troca.
3. Caso a troca tenha sido aceita, o sistema apresenta as gemas enviadas pelo Usuário B, a listagem de gemas que Usuário B deseja, e a coleção do Usuário A.
4. O Usuário A escolhe as gemas de sua coleção para enviar ao Usuário B.
5. O sistema envia as gemas para o Usuário B.
6. O sistema encerra o caso de uso.

### Fluxo Alternativo (3): Troca rejeitada
- Caso a troca tenha sido rejeitada, o sistema exibe um aviso e apaga a solicitação de troca, encerrando o caso de uso.

**Pós-condições:** A solicitação de troca rejeitada foi removida das propostas pendentes, ou a troca aceita foi respondida, e as gemas foram devidamente enviadas ao Usuário B.