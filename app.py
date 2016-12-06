import requests
from flask import Flask
app = Flask(__name__)

# route() decorator tells Flask what URL should trigger our function
@app.route('/')
def hello_world():
    return 'Hello, World!'
	
@app.route('/req')
def testing_requests():
    r = requests.get('http://httpbin.org/status/404')
    return str(r.status_code)
