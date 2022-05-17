# Requisitos Funcionais

- **RF01:** O sistema deve permitir o cadastro de usuários usando nome de usuário e senha.
- **RF02:** O sistema deve reconhecer a identidade de um usuário utilizando seu login com nome e senha, ou através de um esquema de criptografia assimétrica.
- **RF03:** Cada usuário do sistema possui uma **coleção** de gemas.
- **RF04:** O sistema deve permitir que usuários solicitem novas gemas sorteadas para serem adicionadas à sua coleção, de acordo com uma certa cota de solicitações por usuário.
- **RF05:** O sistema deve permitir que os usuários registrem publicamente _o nome_ das gemas estão dispostos a oferecer, e _o nome_ das gemas nas quais tem interesse em obter. Esse registro é chamado de **galeria**.
- **RF06:** O sistema deve permitir que usuários naveguem pelas **galerias** de outros usuários.
- **RF07:** O sistema deve permitir a filtragem de **galerias** de demais usuários através do nome do usuário ou nome de gema.
- **RF08:** O sistema deve permitir a troca par-a-par entre usuários, na qual um dos usuários inicia uma proposta de troca a outro usuário, declarando quais gemas pretende oferecer, e em quais gemas possui interesse.
- **RF09:** O sistema deve notificar o usuário de novos pedidos de troca, permitindo que o mesmo responda também declarando quais gemas pretende oferecer, e em quais gemas possui interesse.
- **RF10:** O sistema deve permitir que qualquer usuário permutante decida rejeitar ou aceitar a troca, enviando os dados completos das gemas declaradas oferecidas para o outro usuário caso afirmativo.
- **RF11:** O sistema deve conhecer uma lista de conjuntos de gemas que, ao serem trocadas, podem gerar uma nova gema. Esse mecanismo de geração de gemas é denominado **fusão**.
- **RF12:** O sistema deve permitir, se ambos os usuários permutantes assim desejarem, tentar realizar uma **fusão** entre as gemas trocadas. A fusão ocorre apenas se cada usuário permutante possui pelo menos uma das gemas de algum conjunto de fusão válido. 
- **RF13:** O sistema deve permitir que o usuário verifique a autenticidade das gemas de sua coleção, ou seja, verificar se foi obtida inicialmente através de alguma interação legítima com o sistema.
- **RF14:** O sistema deve permitir que o usuário apague gemas de sua coleção.