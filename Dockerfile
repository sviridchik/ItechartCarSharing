FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ../ItehartProject-homework/requirements.txt /code/
RUN pip install -r requirements.txt
COPY ../ItehartProject-homework /code/