## CSU07: Propor Troca

**Sumário:** O Usuário utiliza o sistema para propor trocas com outro usuário.

**Ator primário:** Usuário.

### Fluxo Principal:
1. O Usuário busca pela galeria de um outro usuário e solicita propor uma troca.
2. O sistema apresenta a coleção do Usuário.
3. O Usuário seleciona quais gemas de sua coleção ele deseja oferecer na troca, e confirma.
4. O sistema volta para a galeria do outro usuário.
5. O Usuário seleciona quais gemas do outro usuário ele possui interesse na troca, e confirma.
6. O sistema apresenta um campo de texto, um botão para submeter a solicitação de troca, e um botão de cancelar.
7. O Usuário insere uma mensagem que deseja enviar ao outro usuário junto com a solicitação de troca.
8. O sistema apresenta uma caixa de diálogo confirmando se o Usuário realmente deseja realizar a solicitação.
9. Caso o Usuário confirme a troca, o sistema envia a solicitação de troca ao outro usuário através do IP encontrado na busca.
10. O sistema do outro usuário armazena a solicitação recebida. 
11. O sistema encerra o caso de uso.

**Pós-condições:** a solicitação de troca foi enviada e ficou como pendente para o outro usuário.