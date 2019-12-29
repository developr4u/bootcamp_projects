from flask import Flask,request,jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER']  = 'sql12316204'
app.config['MYSQL_PASSWORD'] = 'EyyaRrHm9t'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql12316204'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def create_table():
    cur = mysql.connection.cursor()
    result = cur.execute('''CREATE TABLE todo_app(id INT AUTO_INCREMENT, title VARCHAR(100), description VARCHAR(100), done BOOLEAN, PRIMARY KEY(id))''')
    result.commit()
    return jsonify(result)


@app.route('/todo/api/v1.0/tasks', methods=['POST','GET'])
def insert_or_display():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        result = request.form
        cur.execute(f"INSERT INTO todo_app(title, description, done) VALUE ( '{result['title']}', '{result['description']}', '{result['done']}')")
        mysql.connection.commit()
        return result

    elif request.method == 'GET':
        cur = mysql.connection.cursor()  
        cur.execute('''SELECT * FROM todo_app''')
        disp = cur.fetchall()
        return jsonify({'DATA':disp})

@app.route('/todo/api/v1.0/tasks/<task_id>',methods=['GET','PUT','DELETE'])
def get_update_del(task_id):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM todo_app WHERE id = ''' + task_id)
        disp = cur.fetchall()
        return jsonify({'DATA':disp})

    elif request.method == 'PUT':
        cur = mysql.connection.cursor()
        result = request.form
        cur.execute(f"UPDATE todo_app SET title= '{result['title']}', description= '{result['description']}', done='{result['done']}'  WHERE ID = {task_id} ")
        mysql.connection.commit()
       
        return 'UPDATED'

    elif request.method == 'DELETE':
        cur = mysql.connection.cursor()
        cur.execute(f"DELETE FROM todo_app where id = {task_id}")
        mysql.connection.commit()
        return 'DELETED DATA'

    else:
        return 'DATABASE PROBLEM TRY AGAIN'    










#Runing application
if __name__ == '__main__':
    app.run(debug=True)