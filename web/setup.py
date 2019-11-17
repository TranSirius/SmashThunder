from web import create_app
import sys

app = create_app(sys.argv[-1])
app.run(host = app.config['HOST'], port = app.config['PORT'], threaded = True)
