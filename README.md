# SISU-APP

Sistema web para gerenciamento de processos seletivos, inspirado no SISU, desenvolvido em Python com Orator ORM, PostgreSQL e Docker.

## Funcionalidades
- Cadastro e gerenciamento de cursos
- Cadastro e gerenciamento de edições (processos seletivos)
- Associação de cursos a edições
- Cadastro de candidatos
- Controle de vagas por categoria
- Feedback dos candidatos
- Interface web simples

## Estrutura do Projeto
```
sisu-app/
├── app/                # Código-fonte da aplicação (controllers, models, views)
├── initdb/             # Scripts de inicialização do banco de dados
├── nginx/              # Configuração do Nginx para servir a aplicação
├── requirements.txt    # Dependências Python
├── Dockerfile          # Dockerfile da aplicação
├── docker-compose.yml  # Orquestração dos serviços (app, db, nginx)
```

## Tecnologias Utilizadas
- Python 3.8+
- Orator ORM
- PostgreSQL
- Docker & Docker Compose
- Nginx

## Como rodar o projeto
1. **Configure as variáveis de ambiente** no arquivo `.env` (usuário, senha e nome do banco):
   ```env
   APP_USER=usuario
   APP_PASS=senha
   APP_DB=nome_do_banco
   ```
2. **Suba os containers:**
   ```sh
   docker-compose up --build
   ```
3. Acesse a aplicação em: [http://localhost:1080](http://localhost:1080)

> Os scripts SQL em `initdb/` serão executados automaticamente na primeira inicialização do banco.

## Estrutura das Pastas
- `app/` - Código Python (controllers, models, views)
- `initdb/` - Scripts de criação e popularização do banco
- `nginx/` - Configuração do proxy reverso

## Observações
- Se mudar o nome da pasta principal, ajuste os caminhos relativos nos volumes do `docker-compose.yml`.
- Para reinicializar o banco, remova o volume do Docker referente ao banco de dados.

## Licença
Projeto acadêmico - IFG

---

Desenvolvido por José Mateus F. Neto para fins educacionais.
