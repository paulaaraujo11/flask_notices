import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_notice(notice_id):
    conn = get_db_connection()
    notice = conn.execute('SELECT * FROM notices WHERE id = ?',
                        (notice_id,)).fetchone()
    conn.close()
    if notice is None:
        abort(404)
    return notice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dE%HUjC}-[znRAx&7Agl'

@app.route('/<int:notice_id>')
def notice(notice_id):
    notice = get_notice(notice_id)
    return render_template('notice.html', notice=notice)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO notices (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    notice = get_notice(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE notices SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', notice=notice)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    notice = get_notice(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM notices WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(notice['title']))
    return redirect(url_for('index'))

@app.route('/')
def index():
    conn = get_db_connection()
    notices = conn.execute('SELECT * FROM notices').fetchall()
    conn.close()
    return render_template('index.html', notices=notices)

if __name__ == "__main__":
    app.run()

