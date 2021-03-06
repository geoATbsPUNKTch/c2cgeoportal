FROM camptocamp/geomapfish-build:${geomapfish_version}
LABEL maintainer Camptocamp "info@camptocamp.com"

COPY . /app
WORKDIR /app

ARG GIT_HASH

RUN pip install --disable-pip-version-check --no-cache-dir --no-deps --editable=/app/ && \
    c2cwsgiutils_genversion.py $GIT_HASH

ENV NODE_PATH=/usr/lib/node_modules \
    LOG_LEVEL=INFO \
    GUNICORN_ACCESS_LOG_LEVEL=INFO \
    C2CGEOPORTAL_LOG_LEVEL=WARN \
    PGHOST=db \
    PGHOST_SLAVE=db \
    PGPORT=5432 \
    PGUSER=www-data \
    PGPASSWORD=www-data \
    PGDATABASE=geomapfish \
    PGSCHEMA=main \
    PGSCHEMA_STATIC=main_static \
    TINYOWS_URL=http://tinyows/ \
    MAPSERVER_URL=http://mapserver/ \
    PRINT_URL=http://print:8080/print/

ENTRYPOINT []
CMD ["c2cwsgiutils_run"]
