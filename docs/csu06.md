## CSU06: Pesquisar Galeria

**Sumário:** O Usuário utiliza o sistema para encontrar usuários, de acordo com os critérios desejados.

**Ator primário:** Usuário.

**Ator secundário:** Galeria.

### Fluxo Principal:
1. O sistema apresenta a tela principal.
2. O Usuário solicita buscar na Galeria.
3. O sistema apresenta uma caixa de buscas por nome de usuário ou por nome de gema. No caso da filtragem por nome de gema, o sistema também permite marcar se a busca é por gemas possuídas ou gemas interessadas.
4. O Usuário digita o termo que deseja buscar e confirma a busca.
5. O sistema envia essa solicitação à Galeria
6. A Galeria busca por usuários que se encaixam nos parâmetros de busca, e responde com esses dados, incluindo o IP de cada usuário para que possa ser localizado na rede.
7. O sistema apresenta ao Usuário os dados retornados pela Galeria.
8. O sistema encerra o caso de uso.
