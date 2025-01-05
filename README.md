# goit-pythonweb-hw-12

## GOIT Python Web Homework 12

### Requirements
- Python 3.10
- Docker and Docker Compose

### Installation

```shell
git clone https://github.com/AntonChubarov/goit-pythonweb-hw-012
```

```shell
cd goit-pythonweb-hw-012
```

### Running the Application

```shell
docker compose up -d --build
```

### Deployment

This service is deployed on a personal virtual server hosted by [cityhost.ua](https://cityhost.ua/) provider.
It leverages Docker Compose for container orchestration,
uses Apache 2 as the reverse proxy, and relies on [nic.ua](https://nic.ua/) for domain management.
SSL certificates are managed through Certbot.
### Testing

Open https://sandbox.nutarianfood.tech/docs in your browser
to view the automatically generated Swagger
documentation and test the API.
