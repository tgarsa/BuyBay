FROM postgres:15.3

LABEL authors="tomas"
LABEL description="Postgres Image for demo"
LABEL version="1.0"

# to add the initialization scripts
COPY *.sql /docker-entrypoint-initdb.d/
