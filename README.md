<p align="center"><img src="docs/logo.png" width="200" alt="YGOFabrica logo"></p>

Trabalho prático da disciplina CCF355 - Sistemas Distribuídos e Paralelos, da Universidade Federal de Viçosa Campus Florestal. Trata-se de um sistema de visualização e troca de gemas mágicas virtuais.

## Cliente

Para executar o lado cliente, certificar que o `python` e o `pip` estão instalados. Se necessário, use `sudo`.

    $ python -m pip install --upgrade pip setuptools virtualenv

Acesse a pasta `client` e instale as dependências:

    $ cd client && \
      python -m virtualenv .venv && \
      source .venv/bin/activate && \
      pip install -r requirements.txt
      