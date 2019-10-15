from web import app

@app.route('/')
def login_view():
    return 'Hello World!'

@app.route('/hello')
def hello():
    return "hello"