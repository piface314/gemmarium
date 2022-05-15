# CSU10: Receber Gemas

**Sumário:** O usuário confirma as gemas que recebeu através de uma troca.

**Ator primário:** Usuário.

**Precondições:** O usuário deve estar autenticado no sistema.

## Fluxo Principal:
1. Na tela principal, o sistema apresenta as gemas que o Usuário recebu através de trocas aceitas.
2. O Usuário seleciona as gemas recebidas por alguma troca, ou opta por receber todas simultaneamente.
3. O sistema inclui essas gemas à coleção do Usuário.
4. O sistema encerra o caso de uso.

## Fluxo Alternativo (3): Gemas de Fusão estão disponíveis
- Caso haja alguma gema resultante de fusão entre as gemas recebidas, o sistema apresenta, para cada uma delas, uma caixa de diálogo constando a informação de quais gemas foram usadas para criar a fusão.
- Se o Usuário optar por receber as gemas originais, a gema de fusão é descartada pelo sistema, e o sistema inclui as gemas originais à coleção do Usuário, encerrando o caso de uso.
- Se o Usuário optar por receber a gema de fusão, as gemas originais são descartadas pelo sistema, e o sistema inclui a gema de fusão à coleção do Usuário, encerrando o caso de uso.

**Pós-condições:** as gemas recebidas foram incluídas na coleção do Usuário.