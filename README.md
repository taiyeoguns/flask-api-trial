# flask-api-trial API

Flask API application to show typical Create, Read, Update, Delete (CRUD) operations.

## Requirements

- Python 3.9
- Docker (for development)
- Postgres

## Installation

### Clone Project

```sh
git clone https://github.com/taiyeoguns/flask-api-trial.git
```

### Install Requirements

With a [virtualenv](https://virtualenv.pypa.io/) already set-up, install the requirements with pip:

```sh
pip install -r requirements-dev.txt
```

### Install pre-commit

```sh
pre-commit install
```

### Add details in `.env` file

Create `.env` file from example file and maintain necessary details in it.

```sh
cp .env.example .env
```

### Set up database

We use sqlalchemy to model the data and alembic to keep the db up-to-date.

To setup a local db, fill in database details in `.env` file from earlier or set up environment variables. Ensure the database and user defined in .env is already created in postgres.

For initial database setup, run the following commands:

```sh
flask db upgrade
```

Subsequently, after making any changes to the database models, run the following commands:

```sh
flask db migrate
flask db upgrade
```

### Run the application

Activate the virtual environment and start the application by running:

```sh
python run.py
```

or

```sh
flask run
```

API should be available at `http://localhost:5000`

API documentation should also be available at `http://localhost:5000/v1/docs`. (For other API versions, change `v1` as appropriate)

### Tests

In command prompt, run:

```sh
pytest -vv
```

### Run application with Docker

Ensure database details are added to `.env` file from earlier.

The following environment variables should be set in the `.env` file even if they do not 'exist', the docker postgres image will use them for setting up the container -
`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`

With Docker and Docker Compose set up, run:

```sh
make docker-run
```

Thereafter, application should be available at `http://localhost:5000`

To authorise API requests, pass a valid API key as a header with key `X-Api-Key`

### Example requests

Sample host: `localhost:5000`
Sample API Key: `11111111-1111-1111-1111-111111111111`

#### Using `httpie`

```sh
http localhost:5000/v1/users X-Api-Key:11111111-1111-1111-1111-111111111111 first_name=test last_name=user email='test.user@email.com'
```

#### Using `curl`

```sh
curl -X POST http://localhost:5000/v1/users -H "X-Api-Key:11111111-1111-1111-1111-111111111111" -H "Content-Type: application/json" -d '{"first_name": "test", "last_name": "user", "email": "test.user@email.com"}'
```
