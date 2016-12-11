import requests
import os
import sqlite3
from flask import Flask, render_template, g
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'websites.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Some predefined sites for testing
websites = {
    'http://httpbin.org/': 'OK',
    'http://httpbin.org/status/404': 'OK',
    'http://httpbin.org/status/500': 'OK'
    }

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


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
    return render_template('index.html', websites=websites)
