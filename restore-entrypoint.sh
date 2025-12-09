#!/bin/bash
set -e

load_secret() {
    local var_name="$1"
    local file_name="$2"
    local secret_path="/run/secrets/$file_name"

    if [ -f "$secret_path" ]; then
        # Read the file, trim whitespace, export as variable
        export "$var_name"="$(cat "$secret_path" | tr -d '[:space:]')"
        echo "✅ Loaded secret for $var_name"
    else
        echo "⚠️  Secret file $secret_path not found. Using existing env var if set."
    fi
}

load_secret "AWS_ACCESS_KEY_ID" "aws-access-key-id"
load_secret "AWS_SECRET_ACCESS_KEY" "aws-secret-access-key"
load_secret "PGPASSWORD" "db-password"



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

exec docker-entrypoint.sh "$@"