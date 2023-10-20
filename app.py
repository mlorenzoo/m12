import sqlite3
from flask import Flask, render_template, request, g
from datetime import datetime

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

def allowed_file(filename):
	ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('app.html')

@app.route("/products/list")
def prod_list():
	products = query_db('select * from products')
	return render_template("/products/list.html", products = products)

@app.route("/products/create", methods=["GET", "POST"])
def items_create():
	if request.method == 'GET':
		return render_template('/products/create.html')
	else:
		titulo = request.form['titulo']
		desc = request.form['desc']
		precio = request.form['precio']
		cat_id = 1
		seller_id = 1
		created = datetime.now()
		updated = datetime.now()
		if 'imagen' in request.files:
			foto = request.files['imagen']
			if foto and allowed_file(foto.filename):
				with get_db() as db:
					db.execute("INSERT into products (title, description, photo, price, category_id, seller_id, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
					(titulo, desc, foto.filename, precio, cat_id, seller_id, created, updated))

		return render_template('productlist')

if __name__ == 'main':
   app.run(debug = True)