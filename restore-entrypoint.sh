#!/bin/bash
set -e

# If data directory is empty, try to restore
if [ -z "$(ls -A "$PGDATA" 2>/dev/null)" ]; then
    echo "⚠️  Database directory is empty."
    
    if [ ! -z "$WALG_S3_PREFIX" ]; then
        echo "⬇️  Attempting to restore from WAL-G ($WALG_S3_PREFIX)..."
        wal-g backup-fetch "$PGDATA" LATEST
        
        touch "$PGDATA/recovery.signal"
        
        echo "✅ Restore complete. Starting Postgres to finish recovery..."
    fi
else
    echo "✅ Database exists. Skipping restore."
fi

exec /usr/local/bin/docker-entrypoint.sh "$@"