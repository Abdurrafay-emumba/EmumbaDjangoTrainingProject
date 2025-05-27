#!/bin/bash
set -e

echo "Restoring custom-format dump into $POSTGRES_DB"
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" /docker-entrypoint-initdb.d/db_backup.dump

