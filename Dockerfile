FROM python:3.9

WORKDIR /opt/app

RUN groupadd -r dev && useradd -d /opt/app -r -g dev dev \
    && chown dev:dev -R /opt/app


COPY fastapi_solution/requirements.txt .

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY fastapi_solution .

RUN chown -R dev:dev /opt/app

USER dev

CMD ["python", "/opt/app/src/main.py"]
