#!/bin/sh
# Start command. Edit freely: Railway runs this on every deploy.
#
# HOST=0.0.0.0 serves Railway's healthcheck, public domain and private network
# (IPv4 since Oct 2025). Set HOST=:: in an older project whose private network
# is IPv6-only. One worker fits the 0.5 GB plan; raise WEB_CONCURRENCY on bigger plans.
host="${HOST:-0.0.0.0}"
port="${PORT:-8000}"
workers="${WEB_CONCURRENCY:-1}"

# A typo in a variable shouldn't fail the deploy: fall back and say so
# (as a JSON line, so Railway shows it as a warning).
warn() { printf '{"level":"warning","logger":"start.sh","message":"%s"}\n' "$(printf %s "$1" | tr '"\\' "''")"; }
case "$port" in ''|*[!0-9]*) warn "PORT=$port is not a number; using 8000"; port=8000 ;; esac
case "$workers" in ''|0|*[!0-9]*) warn "WEB_CONCURRENCY=$workers is not a positive number; using 1"; workers=1 ;; esac

exec uvicorn app.main:app --host "$host" --port "$port" --workers "$workers" \
  --proxy-headers --forwarded-allow-ips "*"
