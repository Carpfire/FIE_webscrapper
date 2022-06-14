from flask import Flask, render_template 
from markupsafe import escape
import datetime
app = Flask(__name__)
app.debug = True

# @app.route('/variable_path/<var>/')
# def variable_path(var):
#     return f'<h1>Look at my {escape(var)}</h1>'

# @app.route('/add/<int:var1>/<int:var2>/')
# def add(var1, var2):
#     return f'<h1>Look at my {var1 + var2}</h1>'


@app.route('/')
def index():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())#, content="Big Booty Bitches")

@app.route('/about/')
def about():
    return render_template('about.html')

# @app.route('/comments/')
# def comments():
#     comments = ["so", "many", "comments"]
#     return render_template('comments.html', comments=comments)
