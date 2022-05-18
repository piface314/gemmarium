## CSU09: Concluir Troca

**Sumário:** O Usuário aceita ou rejeita uma troca com outro usuário, encerrando-a.

**Ator primário:** Usuário.

**Precondições:** Existe(m) troca(s) pendente(s) para o Usuário.

### Fluxo Principal
1. O Usuário está visualizando uma troca em aberto.
2. O Usuário aceita a troca.
3. O sistema envia todos os dados das gemas oferecidas para o outro usuário.
4. O sistema encerra o caso de uso.

### Fluxo Alternativo (2): Usuario rejeita a troca.
- Caso o Usuário rejeite a troca, o sistema notifica o outro usuário da rejeição, apaga a proposta de troca e encerra o caso de uso.

**Pós-condições:** A troca foi rejeitada ou aceita, e no segundo caso, as gemas oferecidas foram enviadas ao outro usuário.