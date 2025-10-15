FROM postgres

COPY init_tables.sql /docker-entrypoint-initdb.d
