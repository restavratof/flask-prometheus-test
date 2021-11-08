FROM python:3.9-alpine

RUN apk update && apk add gcc g++ python3-dev

ENV PYTHONUNBUFFERED=1
RUN adduser -D flask1

WORKDIR /home/flask1

COPY requirements.txt requirements.txt
RUN python -m venv venv \
    && venv/bin/pip install --no-cache-dir -r requirements.txt

COPY app.py gunicorn.sh ./
RUN chmod +x gunicorn.sh \
    && chown -R flask1:flask1 ./

USER flask1

EXPOSE 5000
ENTRYPOINT ["./gunicorn.sh"]
