import requests
from flask import Flask
app = Flask(__name__)

websites = {
    'http://httpbin.org/': 'OK', 
    'http://httpbin.org/status/404': 'OK', 
    'http://httpbin.org/status/500': 'OK'
    }

# route() decorator tells Flask 
# what URL should trigger our function
@app.route('/')
def get_status():
    for url in websites:
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            websites[url] = 'OK'
        else:
            websites[url] = 'NOT_OK'
    return str(websites)

        
