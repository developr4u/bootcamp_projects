import graphene 
from flask import Flask,request,jsonify
from flask_graphql import GraphQLView
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER']  = 'sql12316204'
app.config['MYSQL_PASSWORD'] = 'EyyaRrHm9t'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql12316204'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql=MySQL(app)

class Todo_list(graphene.ObjectType):
    id=graphene.Int()
    title=graphene.String(name=graphene.String(default_value="todo_item"))
    description=graphene.String(required=True)
    done=graphene.Boolean(status=graphene.Boolean(default_value=False))

    def todo_items(self,args,context,info):
        database=mysql.connection.cursor()
        database.execute("SELECT * FROM grapgql_sql.todoapps")
        response=database.fetchall()
        data=[Todo_list(id=todo["id"],description=todo["description"],title=todo["title"],done=todo["done"]) for todo in response]
        return data

class my_query(graphene.ObjectType):
    my_list=graphene.List(Todo_list)
    my_list1=graphene.Field(Todo_list,id=graphene.Int())

    def todo_items1(self,args):
        database=mysql.connection.cursor()
        database.execute("SELECT * FROM grapgql_sql.todoapps")
        response=database.fetchall()
        data=[Todo_list(id=todo["id"],description=todo["description"],title=todo["title"],done=todo["done"]) for todo in response]
        return data



schema=graphene.Schema(query=my_query)
app.add_url_rule('/', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@app.route("/task",methods=["GET"])
def get_list():
    database=mysql.connection.cursor()
    database.execute("SELECT * FROM grapgql_sql.todoapps")
    result=database.fetchall()
    return jsonify(result)

@app.route('/tasks/<id>',methods=['GET'])
def retrieve(id):
    database = mysql.connection.cursor()
    database.execute("SELECT * FROM grapgql_sql.todoapps WHERE id = "+ str(id))
    task=database.fetchone()
    return jsonify(task)


@app.route('/tasks',methods=['POST'])
def create():
    task = (request.json)
    database = mysql.connection.cursor()
    try:
        task["id"] = int(task["id"])
    except:
        return jsonify({"not succesful":"id must be numeric"})
    else:
        database.execute("SELECT * FROM grapgql_sql.todoapps where id = "+ str(task["id"]))
        old = database.fetchone()
        if old:
            return jsonify({"unsuccessful":"id must be unique"})
        else:
            id = int(task["id"])
            title = task["title"]
            description = task["description"]
            done = task["done"]
            database.execute("INSERT INTO grapgql_sql.todoapps (id,title,description,done) VALUES (%s , %s, %s, %s)",(str(id),title,description,done))
            mysql.connection.commit()
            result = {'task':task}
            return jsonify({"result":result})


@app.route('/tasks/<id>',methods=['PUT'])
def update(id):
    database=mysql.connection.cursor()
    task=request.json
    try:
        task["id"] = int(task["id"])
    except:
        return jsonify({"not succesful":"id must be numeric"})
    else:
        database.execute("SELECT * FROM grapgql_sql.todoapps where id = "+ str(task["id"]))
        old = database.fetchall()
        if old:
            database.execute("UPDATE grapgql_sql.todoapps SET title=%s, description=%s, done=%s WHERE id = %s", (task["title"],task["description"],task["done"],str(task["id"])))
            mysql.connection.commit()
            return jsonify({"task":task})
        else:
            return jsonify({"unsuccessful":"id not found to be updated"})

@app.route('/tasks/<id>',methods =['DELETE'])
def delete(id):
    database = mysql.connection.cursor()
    response=database.execute("Delete FROM grapgql_sql.todoapps WHERE id = "+str(id))
    if response>0:
        result={"success":"record delete"}
    else:
        result={"unsuccesful":"no record found"}
    mysql.connection.commit()
    return jsonify({"result":result})


if __name__ == '__main__':
     app.run(debug=True)