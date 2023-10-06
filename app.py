import sqlite3
from flask import Flask, render_template, request, g

DATABASE = 'database.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		db.row_factory = sqlite3.Row
	return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('app.html')

@app.route("/products/list")
def nose():
	products = query_db('select * from products')
	return render_template("list.html", products = products)

if __name__ == 'main':
   app.run(debug = True)