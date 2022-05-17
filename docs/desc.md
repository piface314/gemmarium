# Descrição Geral

O nome do sistema é Gemmarium, e se trata, de certa forma, de um jogo social de colecionamento de gemas mágicas virtuais. Essas gemas podem ser obtidas de duas maneiras: adquirindo de um servidor do jogo, ou trocando diretamente com outro usuário. Essas duas maneiras podem ser combinadas através de um mecanismo de fusão, que ocorre quando dois usuários trocam suas gemas e solicitam ao sistema que querem tentar fundir aquelas gemas trocadas em uma nova gema. A motivação do "jogo" está em descobrir novas gemas através de interações com o servidor e com outros usuários.

Podemos projetar quatro papéis nessa arquitetura: os Clientes, e três serviços - o Cofre, a Forja e a Galeria - compondo o sistema. Os Clientes podem comunicar entre si de forma par-a-par, e podem também comunicar com os três serviços do sistema. Todos tem pares de chaves pública e privada, e os três serviços são entidades confiáveis.

Pra cadastrar no sistema, um Cliente vai criar nome de usuário e senha com o Cofre, e informar também ao Cofre a sua chave pública. O Cofre então registra essas informações e notifica à Forja e à Galeria o nome desse novo usuário e a chave pública dele.

Para obter novas gemas, um Cliente deve comunicar com a Forja. A Forja vai [identificar](#identificação-de-usuários) esse usuário, e entregar uma (ou mais) nova(s) gema(s) pra ele caso esteja dentro da cota do usuário (por exemplo, 1 pedido por dia). Essa mensagem é composta por todos os dados que representam aquela gema, junto de uma assinatura da Forja. Essa assinatura é uma mensagem criptografada pela chave privada da Forja, e contém: um ID da Forja, um ID do usuário que solicitou a gema, um ID da gema, um número aleatório, e a timestamp da criação da gema. Os dados da gema e a assinatura são criptografados em conjunto usando a chave pública do Cliente solicitante, e então enviada pra ele.

Todo Cliente pode comunicar com a Galeria e cadastrar o nome das gemas que possui, sem fornecer os dados completos das gemas. Assim, outros Clientes podem buscar na Galeria por Clientes que possuem alguma gema de seu interesse, e obter o IP desse outro Cliente.

Tendo o IP de um Cliente B, o Cliente A pode solicitar uma troca, listando o nome de quais gemas ele oferece e quais ele tem interesse. O Cliente B vê esse pedido e faz o mesmo, lista quais ele vai oferecer e quais ele tem interesse. Ao confirmar a troca, Cliente A criptografa os dados da gema junto à respectiva assinatura da Forja com a chave de B, e B faz o mesmo, com a chave de A, e os dados são trocados. Após a troca, ambos podem verificar a autenticidade das gemas usando a chave pública da Forja, e podem descartar gemas fraudadas.

Se ambos os Clientes permutantes estiverem interessados, eles podem solicitar uma fusão à Forja, que consiste em testar se há um conjunto de gemas compartilhadas pelos dois Clientes permutantes que se combinadas geram uma nova gema. Ambos Clientes enviam os dados das gemas para a Forja, a Forja verifica a autenticidade das gemas, e busca por uma fusão disponível. Se houver alguma fusão disponível, a Forja vai assiná-la da mesma forma descrita antes, porém colocando o ID de ambos os Clientes, e então entregar os dados da nova gema para ambos.

Além de poder verificar a autencidade das gemas, os usuários podem ver quem foram o usuários que descobriram aquela gema inicialmente através da assinatura da Forja, ou quais foram os usuários que se uniram para fundir uma gema, caracterizando o aspecto social do jogo.

## Observações

### Identificação de usuários

Para identificar um usuário sem pedir a senha, o servidor gera um número aleatório e criptografa com a chave pública do Cliente, e envia. O Cliente descriptografa com a chave privada dele, e criptografa com a chave pública do servidor, e responde. O servidor descriptografa e confere se o número casa com o que foi enviado, se sim, ele tem certeza que quem comunicou com ele é alguém que possui a chave privada do Cliente em questão, e usa a chave pública do Cliente para identificá-lo no seu registro.

### Troca de itens P2P

Não há necessidade dos Clientes apagarem os dados da gema que estão oferecendo, pois os usuários estão coletando _informação_, e não quantidades de itens físicos. Um problema da troca P2P, no entanto, é que não há garantia de que um Cliente vai cumprir com sua proposta, mas pelo menos, por não haver perda do que já se tinha, ninguém sai no prejuízo. No máximo, um Cliente não vai obter nenhuma gema (autêntica) nova.

## Funcionalidades opcionais

Poderia ser interessante ter mais de uma Forja, que ofereça gemas diferentes de acordo com algum tema, o que incentivaria os usuários a buscarem fontes diferentes de gemas. Além disso, o Cofre poderia servir para relizar "backup" dos dados das gemas de cada Cliente, visto que o armazenamento dos dados das gemas é feito localmente.