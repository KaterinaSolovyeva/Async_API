FROM python:3.9

WORKDIR /opt/app

RUN groupadd -r dev && useradd -d /opt/app -r -g dev dev \
    && chown dev:dev -R /opt/app


COPY ./requirements.txt .

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY ./src .

RUN chown -R dev:dev /opt/app

USER dev

CMD ["python", "/opt/app/src/main.py"]
