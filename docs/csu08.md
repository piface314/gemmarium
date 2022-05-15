# CSU08: Propor Troca

**Sumário:** O Usuário Proponente utiliza o sistema para propor trocas com outro usuário.

**Ator primário:** Usuário Proponente.

**Ator secundário:** Usuário Proposto.

**Precondições:** O Usuário Proponente deve estar autenticado no sistema.

## Fluxo Principal:
1. O Usuário Proponente acessa a galeria de um outro usuário e solicita propor uma troca.
2. O sistema apresenta a coleção do Usuário Proponente.
3. O Usuário Proponente seleciona quais gemas de sua coleção ele deseja oferecer na troca, e confirma.
4. O sistema volta para a galeria do Usuário Proposto.
5. O Usuário Proponente seleciona quais gemas do Usuário Proposto ele possui interesse na troca, e confirma.
6. O sistema apresenta um campo de texto, um botão para submeter a solicitação de troca, e um botão de cancelar.
7. O Usuário Proponente insere uma mensagem que deseja enviar ao Usuário Proposto junto com a solicitação de troca.
8. O sistema apresenta uma caixa de diálogo confirmando se o Usuário Proponente realmente deseja realizar a solicitação.
9. Caso o Usuário Proponente confirme a troca, o sistema envia a solicitação de troca ao Usuário Proposto.
10. O sistema encerra o caso de uso.

**Pós-condições:** a solicitação de troca foi enviada e ficou como pendente para o Usuário Proposto.