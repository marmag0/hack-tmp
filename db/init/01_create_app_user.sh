#!/bin/sh

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${APP_USER}') THEN
            CREATE ROLE ${APP_USER} WITH LOGIN PASSWORD '${APP_PASSWORD}';
        ELSE
            ALTER ROLE ${APP_USER} WITH LOGIN PASSWORD '${APP_PASSWORD}';
        END IF;
    END
    \$\$;
EOSQL
