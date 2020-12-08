from flask import Flask
from flask_restful import Api,Resource
from collections import defaultdict
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL,API_URL,config={"app_name":"name"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


class Messages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    toid = db.Column(db.Integer,nullable=False)
    msg = db.Column(db.String(800),nullable=False)

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
        print(return_data)
        return {"messages":return_data}

api.add_resource(ClientSend, "/send/<int:userId>/<string:message>")
api.add_resource(ClientUpdate, "/get/<int:userId>")

db.create_all()

if __name__ == "__main__":
    app.run(debug=True)