# CSU04: Obter Gemas

**Sumário:** O usuário utiliza o sistema para obter novas gemas sorteadas.

**Ator primário:** Usuário.

**Precondições:** o Usuário está autenticado no sistema.

## Fluxo Principal:
1. O sistema apresenta a tela principal.
2. O Usuário solicita novas gemas sorteadas.
3. O sistema sortea gemas aleatórias e as adiciona à coleção do Usuário.
4. O sistema encerra o caso de uso.

## Fluxo de Exceção (2) - Última solicitação ocorreu há menos de $t$ unidades de tempo:
- O sistema apresenta um alerta ao Usuário, informando quanto tempo deve ser esperado para realizar uma nova solicitação de novas gemas, e redireciona para a tela principal encerrando o caso de uso.

**Pós-condições:** novas gemas aleatórias foram adicionadas à coleção do Usuário.