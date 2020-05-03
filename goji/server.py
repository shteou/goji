from flask import Flask

app = Flask(__name__)

@app.route('/health')
def hello_world():
    return 'OK!'
