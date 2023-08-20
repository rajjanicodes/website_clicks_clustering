# Raft task base microservice

This is a template for a basic microservice.
Feel free to add to and edit as required.

## What's included
- FastAPI (examples in `app/main.py`)
- SQLAlchemy (models in `app/db_models.py`)
- PostgreSQL
- NumPy

## Getting started

0) Install Docker
1) Clone the repository
2) Use `docker-compose up` in your Terminal to start the Docker container.
3) The app is defaulted to run on `localhost:8004`
   * `/`: The root url (contents from `app/main.py`)

## Rebuild infrastructure (not for code changes)
- `docker-compose build`

## Troubleshooting
- `docker-compose down` (This will destroy all your containers for the project, might need it when you change db models)
- `docker-compose up`


## Running tests
### Installation
```bash
python3 -m pip install requests
```

### Run test cases
```bash
python3 tests/test.py
```