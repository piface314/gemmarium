<p align="center"><img src="docs/logo.png" width="200" alt="Gemmarium logo"></p>

Trabalho prático da disciplina CCF355 - Sistemas Distribuídos e Paralelos, da Universidade Federal de Viçosa Campus Florestal. Trata-se de um sistema de visualização e troca de gemas mágicas virtuais.

Para executar o sistema, certificar que o `python` e o `pip` estão instalados. Se necessário, use `sudo`.

    $ python3 -m pip install --upgrade pip setuptools virtualenv

Execute o `makefile` com o comando `make`, e depois use algum dos scripts de execução a depender do processo que deve ser iniciado. Primeiramente é ideal que o Cofre seja iniciado, depois a Forja, e por último duas instâncias do Cliente. Cofre e Forja podem simplesmente ser executados com `./vault.sh` e `./forge.sh` na raiz do projeto. Já os clientes, para que executem corretamente, devem ser executados com parâmetros adequados:

```bash
# cliente 1
./client.sh 7515 127.0.0.1 7513 127.0.0.1 7514 client.db 5

# cliente 2
./client.sh 7520 127.0.0.1 7513 127.0.0.1 7514 client2.db -5
```

Mais de dois clientes **numa mesma máquina** não vão conseguir se encontrar via broadcast.
