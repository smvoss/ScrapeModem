FROM python:3.8.5-buster

WORKDIR /scrapemodem

ADD app.py /scrapemodem
ADD requirements.txt /scrapemodem

RUN pip install -r requirements.txt

CMD ["python", "app.py"]