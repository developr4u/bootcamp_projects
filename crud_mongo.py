from flask import Flask,request,jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

#Connecting Database through uri, 
app.config['MONGO_URI'] = 'mongodb+srv://abbasshipping:Ahmed654321@mongo1-dctf4.mongodb.net/test?retryWrites=true&w=majority'

#Database Connection
mongo = PyMongo(app)


#Making Routes:

@app.route('/todo/api/v1.0/tasks',methods=['GET','POST'])
def get_or_post():
    if request.method == 'POST':
        connection = mongo.db.axiom
        data = request.get_json({})
        connection.insert({'_id':data['_id'],'title':data['title'],'description':data['description'],'done':data['done']})
        return (f"Collection of ID {data['_id']} is added in data base")

    elif request.method == 'GET':
        connection = mongo.db.axiom
        data = connection.find()
        all_data = []
        for i in data:
            all_data.append(i)
        return jsonify({'DATA':all_data})

    else:
        return 'there is mistake somewhere plz try again'

@app.route('/todo/api/v1.0/tasks/<task_id>',methods=['GET','PUT','DELETE'])
def update_del_show(task_id):
    if request.method == 'GET':
        connection = mongo.db.axiom
        return jsonify({'data':connection.find_one({'_id':int(task_id)})})
        


    elif request.method == 'PUT':
        connection = mongo.db.axiom
        data = request.get_json({})
        connection.replace_one({'_id':int(task_id)},{'title':data['title'],'description':data['description'],'done':data['done']})
        return jsonify({'data':data})

    elif request.method == 'DELETE':
        connection = mongo.db.axiom
        data = connection.find_one({'_id':int(task_id)})
        print(data)
        if data:
            connection.find_one_and_delete({'_id':int(task_id)})
            return 'DELETED'
        return 'NOT FOUND' 

    else:
        return 'DATABASE PROBLEM TRY AGAIN LATER!'      



#Runing application
if __name__ == '__main__':
    app.run(debug=True)