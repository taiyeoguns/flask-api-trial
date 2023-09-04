# flask-api-trial API

Flask API Trial

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
docker-compose up
```

Wait till setup is complete and all containers are started.

In another terminal tab/window, run:

```sh
docker-compose exec flask_service flask db upgrade
```

Thereafter, application should be available at `http://localhost:5000`
