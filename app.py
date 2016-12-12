import requests
import os
import sqlite3
from flask import Flask, render_template, g, request, redirect, flash, \
    url_for
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


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'


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


@app.route('/')
def show_websites():
    db = get_db()
    cur = db.execute('select url, status from websites order by id desc')
    websites = cur.fetchall()
    return render_template('show_websites.html', websites=websites)


@app.route('/add', methods=['POST'])
def add_website():
    db = get_db()
    db.execute('insert into websites (url) values (?)',
        [request.form['url']])
    db.commit()
    flash('New website was successfully added')
    return redirect(url_for('show_websites'))


# route() decorator tells Flask
# what URL should trigger our function
# @app.route('/')
# def get_status():
#     for url in websites:
#         r = requests.get(url)
#         if r.status_code == requests.codes.ok:
#             websites[url] = 'OK'
#         else:
#             websites[url] = 'NOT_OK'
#     return render_template('index.html', websites=websites)
