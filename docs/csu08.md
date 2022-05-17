## CSU08: Responder Proposta de Troca

**Sumário:** O Usuário A utiliza o sistema para prosseguir com a negociação da troca com Usuário B.

**Ator primário:** Usuário A.

**Ator secundário:** Usuário B.

### Fluxo Principal
1. Na tela principal, o sistema apresenta as solicitações de troca pendentes para o Usuário A.
2. O Usuário A seleciona uma solicitação de troca.
3. O sistema apresenta a mensagem enviada pelo Usuário B, uma listagem do nome das gemas oferecidas e as de interesse do Usuário B, essa mesma listagem, porém editável, referente ao Usuário A, e botões para rejeitar, aceitar ou negociar a proposta.
4. O Usuário A pode incluir gemas de sua coleção para preencher a listagem de suas gemas oferecidas, e também pode alterar as gemas que listou de interesse.
5. O Usuário A aceita a proposta.
6. O sistema envia ao Usuário B todos os dados das gemas oferecidas pelo Usuário A, e, quando receber as gemas do Usuário B, armazena seus dados.
7. O sistema encerra o caso de uso.

### Fluxo Alternativo (5): Usuário A rejeita a troca
- Caso o Usuário A rejeite a troca, o sistema apaga a solicitação, comunica a rejeição ao Usuário B, e encerra o caso de uso.

### Fluxo Alternativo (5): Usuário A negocia a troca
- Caso o Usuário A decida negociar a troca, o sistema exibe uma caixa de texto para compor uma mensagem ao Usuário B.
- O Usuário A escreve uma mensagem.
- O sistema envia ao Usuário B essa mensagem junto da lista atualizada de nomes das gemas oferecidas e de interesse.
- O sistema encerra o caso de uso.

**Pós-condições:** A solicitação de troca foi rejeitada e removida das propostas pendentes, ou foi aceita, e as gemas foram devidamente trocadas entre os Usuários.