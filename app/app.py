from flask import Flask, render_template 
from markupsafe import escape
from werkzeug.exceptions import abort
import sqlite3

app = Flask(__name__)
app.debug = True

# @app.route('/variable_path/<var>/')
# def variable_path(var):
#     return f'<h1>Look at my {escape(var)}</h1>'

# @app.route('/add/<int:var1>/<int:var2>/')
# def add(var1, var2):
#     return f'<h1>Look at my {var1 + var2}</h1>'


def get_db_connection():
    conn = sqlite3.connect('..\\fencing.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_fencer(fencer_id):
    conn = get_db_connection()
    fencer = conn.execute('SELECT * FROM fencer WHERE id = ?', (fencer_id,)).fetchone()
    if fencer is None:
        abort(404)
    return fencer
def get_bouts(fencer_id):
    conn = get_db_connection()
    bouts = conn.execute('SELECT bout.win_fencer, bout.win_fencer_')
@app.route('/<int:fencer_id>')
def fencer(fencer_id):
    fencer = get_fencer(fencer_id)
    return render_template('fencer.html', fencer = fencer)

@app.route('/')
def index():
    conn = get_db_connection()
    fencers = conn.execute("SELECT * FROM fencer").fetchall()
    conn.close()
    return render_template('index.html', fencers=fencers)#, content="Big Booty Bitches")

@app.route('/about/')
def about():
    return render_template('about.html')

# @app.route('/comments/')
# def comments():
#     comments = ["so", "many", "comments"]
#     return render_template('comments.html', comments=comments)
