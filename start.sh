# python web/setup.py release
cd web
gunicorn -w 4 -b 127.0.0.1:3000 run:app
cd ..