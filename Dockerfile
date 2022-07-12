FROM python:3.10

# .pyc
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /code

COPY . /code/

ENV PORT=8000

EXPOSE 8000