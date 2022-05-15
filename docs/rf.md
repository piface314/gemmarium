# Requisitos Funcionais

- **RF01:** O sistema deve permitir o cadastro de usuários mediante nome de usuário e senha.
- **RF02:** O sistema deve reconhecer a identidade de um usuário utilizando seu login com nome e senha.
- **RF03:** Cada usuário do sistema possui uma coleção de gemas.
- **RF04:** A cada $t$ unidades de tempo o usuário pode solicitar ao sistema $n$ novas gemas aleatórias que serão adicionadas à sua coleção.
- **RF05:** Cada usuário pode colocar quaisquer de suas gemas à mostra para outros usuários. O conjunto de gemas que estão à mostra é chamado de galeria.
- **RF06:** Um usuário pode navegar pelas galerias de outros usuários.
- **RF07:** O sistema deve permitir a filtragem de galerias de demais usuários através do nome do usuário ou nome da gema.
- **RF08:** Um usuário pode selecionar gemas de sua coleção e gemas da galeria de outro usuário para propor uma troca.
- **RF09:** Um usuário que receber uma proposta de troca pode rejeitar ou aceitar a proposta e opcionalmente adicionar outras gemas de sua coleção.
- **RF10:** Deve haver conjuntos específicos de gemas que, ao serem trocadas, podem gerar uma nova gema para cada usuário envolvido na troca. Esse mecanismo de geração de gemas é denominado fusão. A fusão apenas ocorre se cada usuário envolvido na troca possui pelo menos um das gemas do conjunto. Cada usuário pode escolher receber a gema resultante da fusão ao invés da(s) gema(s) oferecida(s) durante a troca. 