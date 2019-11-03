export FLASK_APP=`pwd`/web/web
flask drop-db
flask init-db
flask drop-index
flask init-index