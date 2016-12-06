import requests
from flask import Flask
app = Flask(__name__)

# route() decorator tells Flask what URL should trigger our function
@app.route('/')
def hello_world():
    return 'Hello, World!'
	
@app.route('/req')
def testing_requests():
    url = 'http://httpbin.org/'
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        return '"%s" status: OK' % url
    else:
        return '"%s" status: NOT OK' % url
        
