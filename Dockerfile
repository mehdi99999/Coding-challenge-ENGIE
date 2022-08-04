FROM python:latest

COPY ./app/ /challenge/

RUN pip install -r /challenge/requirements.txt

EXPOSE 8888

CMD ["python", "/challenge/main.py"]
