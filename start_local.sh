#!/bin/bash
# Start local PostgreSQL + Party API
export PATH="/usr/lib/postgresql/16/bin:$PATH"
PGDATA=/tmp/pgdata

if ! pg_isready -p 5433 -h "$PGDATA" &>/dev/null; then
    echo "Starting PostgreSQL on port 5433..."
    pg_ctl -D "$PGDATA" -l "$PGDATA/log" start 2>/dev/null || initdb -D "$PGDATA" && \
    echo "host all all 127.0.0.1/32 trust" >> "$PGDATA/pg_hba.conf" && \
    echo "host all all ::1/128 trust" >> "$PGDATA/pg_hba.conf" && \
    echo "local all all trust" >> "$PGDATA/pg_hba.conf" && \
    echo "port = 5433" >> "$PGDATA/postgresql.conf" && \
    echo "unix_socket_directories = '$PGDATA'" >> "$PGDATA/postgresql.conf" && \
    pg_ctl -D "$PGDATA" -l "$PGDATA/log" start && \
    sleep 1 && \
    createdb -p 5433 -h "$PGDATA" businesscore 2>/dev/null || true && \
    createdb -p 5433 -h "$PGDATA" palmarante 2>/dev/null || true && \
    psql -p 5433 -h "$PGDATA" -d businesscore -f database/ddl/002_party.sql 2>/dev/null || true
    echo "PostgreSQL ready."
fi

export PG_HOST=localhost PG_PORT=5433 PG_USER=postgres PG_PASSWORD=postgres
python3 -m uvicorn modules.party.infrastructure.api.party_api:app --host 0.0.0.0 --port 8000
