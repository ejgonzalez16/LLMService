#!/bin/sh
set -e

host="$1"
shift

until mysql -h "$host" -uroot -pargydb123 -e "select 1" > /dev/null 2>&1; do
  echo "Esperando a MySQL..."
  sleep 2
done

exec "$@"
