from flask import Flask, render_template,request
from flask_restful import Api,Resource
from collections import defaultdict
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO,send,emit
import json
import datetime
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
api = Api(app)
db = SQLAlchemy(app)
active_users = []
login_queue = []
clients = {}
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL,API_URL,config={"app_name":"name"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

class User(db.Model):
    Id = db.Column(db.Integer,primary_key=True)
    Login = db.Column(db.String(50),nullable=False)
    Password = db.Column(db.String(50),nullable=False)


class Message(db.Model):
    Id = db.Column(db.Integer,primary_key=True)
    SendDate = db.Column(db.DateTime,nullable=False)
    Displayed = db.Column(db.Boolean,nullable=False)
    From = db.Column(db.Integer,nullable=False)
    To = db.Column(db.Integer,nullable=False)
    Content = db.Column(db.Text,nullable=True)

    def to_json(self):
        return {"Id":self.Id,"SendDate":self.SendDate.strftime("%m/%d/%Y, %H:%M:%S"),"Displayed":self.Displayed,"From":self.From,"To":self.To,"Content":self.Content}
'''
class ClientSend(Resource):

    def post(self, userId, message):
        msg = Messages(toid=userId,msg=message)
        db.session.add(msg)
        db.session.commit()
        return {"result":"succes"}
      
class ClientUpdate(Resource):
    def get(self, userId):
        msgs = Messages.query.filter_by(toid=userId)
        return_data = []
        for msg in msgs:
            return_data.append(msg.msg)
            db.session.delete(msg)
        db.session.commit()
        print(return_data)
        return {"messages":return_data}

api.add_resource(ClientSend, "/send/<int:userId>/<string:message>")
api.add_resource(ClientUpdate, "/get/<int:userId>")
'''
@app.route('/get_user_list/<int:requestId>')
def get_user_list(requestId):
    users = User.query.all()
    all_users = []
    for user in users:
        if user.Id == requestId:
            continue
        u = {}
        u["Id"] = user.Id
        u["Name"] = user.Login
        u["Status"] = user.Id in active_users
        u["Unread"] = len(Message.query.filter_by(From=user.Id,To=requestId,Displayed=False).all())
        all_users.append(u)
    return json.dumps(all_users)
@app.route('/unread_messages/<int:fromId>/<int:toId>')
def unread_messages(fromId,toId):
    return {"size":len(Message.query.filter_by(From=fromId,To=toId,Displayed=False).all())}
@app.route('/get_messages/<int:fromId>/<int:toId>')
def get_messages(fromId,toId):
    from_msgs = Message.query.filter_by(From=fromId,To=toId).all()
    to_msgs = Message.query.filter_by(From=toId,To=fromId).all()
    messages = []
    notify = False
    for msg in from_msgs:
        messages.append(msg.to_json())
    for msg in to_msgs:
        if msg.Displayed == False:
            notify = True
            msg.Displayed = True
        messages.append(msg.to_json())
    messages.sort(key=lambda x: x["SendDate"])
    db.session.commit()
    if notify:
        update_list_for_users([toId])
    return json.dumps(messages)
@app.route('/read/<int:fromId>/<int:toId>')
def read(fromId,toId):
    msg = Message.query.filter_by(From=fromId,To=toId,Displayed=False).first()
    if msg != None:
        msg.Displayed = True
        db.session.add(msg)
        db.session.commit()
        return {"response":"succes"}
    else:
        return {"response":"there is no more unread messages"}
@app.route("/send_message/<int:fromId>/<int:toId>/<string:content>")
def send_message(fromId,toId,content):
    msg = Message(From=fromId,To=toId,Content=content,Displayed=False,SendDate=datetime.datetime.now())
    db.session.add(msg)
    db.session.commit()
    update_list_for_users([fromId,toId])
    return {"status":"succes"}
@app.route('/login/<string:login>/<string:password>')
def login(login,password):
    user = User.query.filter_by(Login=login,Password=password).first()
    if user != None:
        active_users.append(user.Id)
        login_queue.append(user.Id)
        return {"status":1,"id":user.Id}
    else:
        user = User.query.filter_by(Login=login).first()
        if user != None:
            return {"status":-1,"id":-1}
        else:
            newId = register_new_user(login,password)
            login_queue.append(newId)
            return {"status":1,"id":newId}
    update_list()

#api.add_resource(API, "/get_user_list/<int:requestId>")
#api.add_resource(API, "/unreadMessages/<int:fromId>/<int:toId>")
#api.add_resource(API, "/read/<int:fromId>/<int:toId>")
#api.add_resource(API, "/login/<string:login>/<string:password>")
db.create_all()

def register_new_user(login,password):
    user = User(Login=login,Password=password)
    db.session.add(user)
    db.session.commit()
    active_users.append(user.Id)
    return user.Id
def update_list():
    socketio.emit("update_list",brodcast=True)
def update_list_for_users(users):
    for x in users:
        print(x,clients)
        try:
            sid = list(clients.keys())[list(clients.values()).index(x)]
            socketio.emit("update_list",room=sid)
        except:
            continue    
@socketio.on("connect")
def connect():
    print(request.sid," connected")
    print(active_users)
    clients[request.sid] = login_queue.pop(0)
    update_list()
@socketio.on("disconnect")
def disconnect():
    print(request.sid," disconnected")
    active_users.remove(clients[request.sid])
    del clients[request.sid]
    update_list()
if __name__ == "__main__":
    socketio.run(app)
    #app.run(debug=True)
