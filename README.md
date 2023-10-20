# THE GRADS - SOLAR PLATE FRONTEND
Repositório do frontend que está sendo desenvolvido para o projeto da equipe THE GRADS.

### Requisitos para o setup do ambiente
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
* [Make](https://www.gnu.org/software/make/)


### Rodando
O projeto foi construído com [Dash](https://dash.plotly.com/) e para rodar o projeto só é necessário executar o comando: 
```sh
make run-dev
```

Esse comando vai levantar todos os serviços necessários e será possível analisar o log da aplicação pelo terminal.

Com o sistema rodando abra a [http://localhost:8050](http://localhost:8050) para acessar o sistema.

Através dele será possível relizar os testes, o usuário padrão é o:
```
user: test@test.com
sena: password
```