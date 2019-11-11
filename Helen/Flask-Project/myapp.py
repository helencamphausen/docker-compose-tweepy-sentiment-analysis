from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello from Flask this is Helens first Flask App</h1>'

app.run(host='0.0.0.0', debug=True)
