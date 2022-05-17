## CSU13: Autenticar Usuário

**Sumário:** O usuário fornece credenciais para que seja identificado.

**Ator primário:** Usuário.

**Atores secundários:** Serviço.

### Fluxo principal:
1. O usuário solicita uma interação com um Serviço.
2. O sistema envia uma solicitação a esse Serviço.
3. O Serviço gera um número aleatório, criptografa-o com a chave pública do usuário, e responde ao sistema.
4. O sistema descriptografa com sua chave privada e responde ao Serviço o número encontrado.
5. O Serviço confere se o número recebido casa com o número gerado, e identifica o usuário.
6. O sistema encerra o caso de uso. 

**Pós-condições:** o Usuário foi identificado pelo Serviço.
