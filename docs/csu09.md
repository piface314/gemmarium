# CSU09: Concluir Troca

**Sumário:** O Usuário Proposto utiliza o sistema para aceitar ou rejeitar trocas com outro usuário.

**Ator primário:** Usuário Proposto.

**Ator secundário:** Usuário Proponente.

**Precondições:** O Usuário Proposto deve estar autenticado no sistema. 

## Fluxo Principal
1. Na tela principal, o sistema apresenta as solicitações de troca pendentes para o Usuário Proposto.
2. O Usuário Proposto seleciona uma solicitação de troca.
3. O sistema apresenta em um painel as gemas oferecidas pelo Usuário Proponente, um outro painel com lacunas correspondentes às gemas pelas quais o mesmo tem interesse, a coleção do Usuário Proposto, e botões para rejeitar ou aceitar a proposta.
4. O Usuário Proposto inclui gemas de sua coleção para preencher as lacunas do painel de troca, e opcionalmente pode oferecer mais gemas de sua coleção.
5. O Usuário Proposto aceita a proposta.
6. O sistema exibe uma caixa de diálogo para confirmar a troca.
7. Caso o Usuário Proposto confirme, o sistema envia ao Usuário Proposto as gemas oferecidas pelo Usuário Proponente, e envia ao Usuário Proponente as gemas oferecidas pelo Usuário Proposto.
8. O sistema redireciona para a tela da caixa de entrada do Usuário Proposto.
9. O sistema encerra o caso de uso.

## Fluxo Alternativo (5): Usuário Proposto rejeita a troca
- Caso o Usuário Proposto rejeite a solicitação de troca, o sistema exibe uma caixa de diálogo para confirmar a rejeição.
- O Usuário Proposto confirma a rejeição e o sistema encerra o caso de uso. Se cancelar a rejeição, o caso de uso retorna ao passo 4.

## Fluxo Alternativo (8): Fusão de gemas disponível
- Caso o sistema detecte que uma fusão de gemas está disponível, além de enviar as gemas trocadas, o sistema envia para cada Usuário os dados da nova gema, resultado da fusão ocorrida.
- O caso de uso retorna ao passo 8.

**Pós-condições:** A solicitação de troca foi rejeitada e removida das propostas pendentes, ou foi aceita, e as gemas são devidamente trocadas e enviadas às caixas de entrada dos Usuários.