#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/.env
source ${DIR}/.venv/Scripts/activate

sqlacodegen postgresql://${DBUSER}:${DBPASS}@${DBHOST}/${DBNAME} > models.py

sed -i -e '1h;2,$H;$!d;g' -e 's/\nBase = declarative_base()/from app import db\n\nBase = db.Model/' models.py