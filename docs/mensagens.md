# Esquema das mensagens trocadas

## Legenda

As letras `C`, `V` e `F` identificam o Cliente, o Cofre (Vault) e a Forja, respectivamente.
Cada troca de mensagens é especificada da forma

```
[X, Y ---> Z] (op, {arg1:type1, arg2:type2})
```

que indica que espera-se que a entidade X ou Y envie a mensagem para Z, e a mensagem é
identificada pela string `op`, contendo 0 ou mais argumentos, identificados por `arg1`,
`arg2`, etc., de tipos `type1`, `type2`, etc. respectivamente. Se uma seta `-*->` for
usada, isso indica um broadcast. Um `*` no nome da entidade indica que é uma mensagem
que pode ser trocada de ou para uma entidade qualquer. Um exemplo de valor para argumento
pode ser mostrado também da seguinte forma:

```
[X ---> Y] (op, {arg:str="exemplo"})
```

## Mensagens

- `[* ---> *] (error, {code:str})`: indica algum erro qualquer.
- `[C ---> V] (signup, {username:str})`: solicita cadastro.
- `[V ---> C] (ack, {id:str})`: confirma o cadastro, informando o ID único do usuário.
- `[C ---> F] (request, {id:str})`: solicita uma nova gema.
- `[F ---> V] (auth, {id:str})`: solicita dados de usuário para autenticação.
- `[V ---> F] (user, {name:str, key:str})`: informa dados de usuário para autenticação.
- `[F ---> C] (auth, {secret:int})`: envia um número aleatório usado no teste de autenticação.
- `[C ---> F] (auth, {secret:int})`: retorna o mesmo número para confirmar identidade.
- `[F ---> C] (gem, {gem:str})`: entrega dados de uma gema.
- `[F ---> C] (error, {code:str="AuthError"})`: informa erro de autenticação.
- `[F ---> C] (error, {code:str="QuotaExceeded", wait:int})`: informa quanto tempo em segundos o usuário tem que esperar para solicitar mais gemas.
- `[C -*-> C] (search, {})`: realiza descoberta na rede local.
- `[C ---> C] (gallery, {id:str, username:str, port:int, wanted:list[str], offered:list[str]})`: informa o nome das gemas que busca e nas quais possui interesse, e em qual porta espera receber trocas.
- `[C ---> C] (trade, {peerid:str, peername:str, port:int})`: inicia um processo de troca.
- `[C ---> C] (update, {wanted:list[str], offered:list[str]})`: atualiza o estado de uma troca.
- `[C ---> C] (accept, {})`: aceita uma troca.
- `[C ---> C] (reject, {})`: rejeita uma troca.
- `[C ---> C] (fusion, {})`: indica que pretende tentar fusão.
- `[C ---> C] (gems, {gems:list[str]})`: envia dados de gemas.
- `[C ---> C] (ack, {})`: confirma alguma ação.

