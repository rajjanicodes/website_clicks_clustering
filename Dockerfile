FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY ./app /app
