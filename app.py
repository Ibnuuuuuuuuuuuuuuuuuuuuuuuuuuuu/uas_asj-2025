from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from dotenv import load_dotenv
import time 

load_dotenv() 

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key_if_not_set')

def init_db():
    max_retries = 5
    retry_delay = 5 # seconds
    for i in range(max_retries):
        try:
            with app.app_context(): 
                cur = mysql.connection.cursor()
                cur.execute("SELECT 1")
                cur.close()
            print("Database connection successful.")
            break 
        except Exception as e:
            print(f"Attempt {i+1} to connect to DB and create table failed: {e}")
            if i < max_retries - 1:
                time.sleep(retry_delay) 
            else:
                print("Max retries reached. Could not connect to database.")
                raise 


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu_items ORDER BY category ASC, name ASC")
    all_items = cur.fetchall()
    cur.close()

    menu_by_category = {}
    for item in all_items:
        category = item['category']
        if category not in menu_by_category:
            menu_by_category[category] = []
        menu_by_category[category].append(item)
            
    ordered_categories = ['Coffee', 'Non-Coffee', 'Food', 'Snack']
    
    sorted_categories = [cat for cat in ordered_categories if cat in menu_by_category]
    for category in menu_by_category:
        if category not in sorted_categories:
            sorted_categories.append(category)


    return render_template('index.html', menu_by_category=menu_by_category, sorted_categories=sorted_categories)

@app.route('/add_item', methods=['POST']) 
def add_item(): 
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO menu_items (name, description, price, category) VALUES (%s, %s, %s, %s)",
                        (name, description, price, category))
            mysql.connection.commit()
            flash('Item menu berhasil ditambahkan!', 'success')
        except MySQLdb.Error as e:
            flash(f'Gagal menambahkan item menu: {e}', 'danger')
        finally:
            cur.close()
        return redirect(url_for('index'))

@app.route('/edit_item/<int:id>')
def edit_item(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu_items WHERE id = %s", (id,))
    item = cur.fetchone()
    cur.close()
    if item:
        return render_template('edit_item.html', item=item)
    flash('Item menu tidak ditemukan.', 'danger')
    return redirect(url_for('index'))

@app.route('/update_item/<int:id>', methods=['POST']) 
def update_item(id): 
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']

        cur = mysql.connection.cursor()
        try:
            cur.execute("UPDATE menu_items SET name = %s, description = %s, price = %s, category = %s WHERE id = %s",
                        (name, description, price, category, id))
            mysql.connection.commit()
            flash('Item menu berhasil diperbarui!', 'success')
        except MySQLdb.Error as e:
            flash(f'Gagal memperbarui item menu: {e}', 'danger')
        finally:
            cur.close()
        return redirect(url_for('index'))

@app.route('/delete_item/<int:id>', methods=['POST']) 
def delete_item(id): 
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM menu_items WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Item menu berhasil dihapus!', 'success')
    except MySQLdb.Error as e:
        flash(f'Gagal menghapus item menu: {e}', 'danger')
    finally:
        cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Waiting for database to be fully ready (if it's the first time running this container)...")
    time.sleep(15)
    init_db() 
    app.run(debug=True, host='0.0.0.0', port=5000)