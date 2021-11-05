FROM python:3.9.7-slim

ENV PYTHONUNBUFFERED=1

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ADD app.py /var/server/app.py

CMD python /var/server/app.py
