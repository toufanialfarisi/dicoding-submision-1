from flask import redirect, url_for, render_template, Blueprint, flash, request, Flask
from forms import Post
import numpy as np
import pyodbc

server = 'toufani-ra-server.database.windows.net'
database = 'toufani-ra-db'
username = 'toufani1515'
password = '#serigala95'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

book = Flask(__name__)
book.jinja_env.filters['zip'] = zip
book.config['SECRET_KEY'] = 'mysecretkey'

@book.route('/list-book')
def list_book():
    tsql = "SELECT * FROM blogpost;"
    row_res = []
    id_  = []
    author_ = []
    title_ = []
    content_ = []
    with cursor.execute(tsql) :
        row = cursor.fetchmany()
        row2 = cursor.fetchall()
        for i in row2:
            id_.append(i[0])
            author_.append(i[1])
            title_.append(i[2])
            content_.append(i[3])
            print('id', i[0])
            print('author', i[1])
            print('title', i[2])
            print('content', i[3])
    # row = list(id_, author_, title_, content_)
    print(row)

    return render_template('list_book.html', containers=row, no=range(1,len(id_)+1), id=id_, author=author_, title=title_, content=content_)


@book.route('/', methods=['POST', 'GET'])
# @login_required
def add_book():
    form = Post()
    if request.method == 'POST':
        author  = form.author.data
        title   = form.title.data
        content = form.content.data
        # tsql = "INSERT INTO dbo.blogpost (author, title, content) VALUES (?,?,?);"
        with cursor.execute("INSERT INTO dbo.blogpost (author, title, content) VALUES ('{}','{}','{}');".format(author, title, content)):
            print ('Successfully Inserted!')
        output = [author, title, content]
        flash('new post was added', 'success')
        # print(output)
        return redirect(url_for('list_book'))
    return render_template('add_book.html', form=form)

@book.route('/delete/<int:id>', methods=['POST','GET'])
# @login_required
def delete_book(id):
    tsql = "DELETE FROM blogpost WHERE id = ?"
    with cursor.execute(tsql,id):
        print ('Successfully Deleted!')
    flash('Post successfully deleted', 'success')
    return redirect(url_for('list_book'))

if __name__ == "__main__":
    book.run(debug=True)