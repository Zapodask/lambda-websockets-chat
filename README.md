# Aws-lambda websockets chat

## Chat em tempo real com api gateway websockets na lambda

## Tecnologias utilizadas

* Python
* Aws
    * Lambda
    * Api gateway
    * DynamoDB

## Setup

1. Use o template.yaml no cloudformation
2. Preencha o .env com o nome do bucket com o código da lambda
3. Utilize os comandos abaixo
```console
    # Criar ambiente virtual
    python -m venv .venv

    # Ativar o ambiente virtual
    .\.venv\Scripts\activate

    # Instalar requerimentos
    pip install -r requirements.txt

    # Enviar código para o bucket
    python .\scripts\update.py
```

## Rotas

```json
# Escolher nome
{
    "action": "setName",
    "name": string
}

# Enviar mensagem para um
{
    "action": "sendTo",
    "to_id": string,
    "message": string
}

# Enviar mensagem para todos
{
    "action": "sendToAll",
    "message": string
}
```

## License
[MIT](https://choosealicense.com/licenses/mit/)