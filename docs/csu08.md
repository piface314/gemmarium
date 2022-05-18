## CSU08: Negociar Troca

**Sumário:** O Usuário dá prosseguimento à negociação da troca com outro usuário.

**Ator primário:** Usuário.

**Precondições:** Existe(m) troca(s) pendente(s) para o Usuário.

### Fluxo Principal
1. Na tela principal, o sistema apresenta as solicitações de troca pendentes para o Usuário A.
2. O Usuário seleciona uma solicitação de troca.
3. O sistema apresenta o estado atual da negociação, exibindo as mensagens trocadas entre os usuários, e as listas de nomes de gemas que cada um está disposto a oferecer e em quais tem interesse. 
4. O Usuário pode escrever novas mensagens ao outro usuário ou também editar sua lista de gemas ofertadas/interessadas.
5. O sistema envia cada mensagem ou alteração para o outro usuário.
6. O sistema encerra o caso de uso.

**Pós-condições:** O estado da negociação da troca foi alterado, tendo adicionado novas mensagens ou atualizado as listas de gemas.