from bson import objectid
from flask import Flask, request, jsonify

# use to interact with mongo db
from flask_pymongo import PyMongo

# use to convert bson to json
from bson.json_util import dumps

# use to generate random string for id
from bson.objectid import ObjectId

# Hashing library
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"
app.config["MONGO_URI"] = "mongodb://localhost:27017/Users"

mongo = PyMongo(app)

@app.route("/hello")
def hello():
    return "route is working"

@app.route("/add", methods=["POST"])
def add_user():
    json = request.json
    name = json["name"]
    email = json["email"]
    password = json["password"]

    if name and email and password and request.method == "POST":
        hashed_password = generate_password_hash(password)
        id = mongo.db.user.insert({"name": name, "email": email, "password": hashed_password})
        resp = jsonify(" User Added Successfully")
        resp.status_code = 200
        return resp
    
    else:
        return not_found()

# Route for findng all records
@app.route("/users")
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp

# route for finding a specific record
@app.route("/users/<id>")
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp 

#  route for deleting record 
@app.route("/delete/<id>", methods = ['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id' : ObjectId(id)})
    resp = jsonify("User Deleted")
    resp.status_code = 200 
    return resp

# route for update user
@app.route('/update/<id>', methods = ['PUT'])
def update_user(id):
    id  = id
    json  = request.json 
    name  = json['name'] 
    email = json['email']
    password = json['password']

    if id and name and email and password and request.method == 'PUT':
        hashed_passsword = generate_password_hash(password)

        mongo.db.user.update_one(
            {'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)},
            {'$set':{'name': name, 'email': email, 'password': hashed_passsword}})
        resp = jsonify('User updated Successfully')
        resp.status_code = 200
        return resp

    else :
        return not_found()

# funciton for calling error message 
@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status' : 404,
        'message' : 'Not Found' + request.url
    }
    resp =jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(debug=True)

