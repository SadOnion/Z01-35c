from flask import Flask
from flask_restful import Api, Resource
from collections import defaultdict
app = Flask(__name__)
api = Api(app)

messages = defaultdict(list)

class ClientSend(Resource):
    def post(self, userId, message):
        messages[str(userId)].append(message)
        print(messages[str(userId)])
        return {"result":"succes"}
class ClientUpdate(Resource):
    def get(self, userId):
        return_data = messages[str(userId)]
        messages[str(userId)] = []
        print(return_data)
        return {"messages":return_data}

api.add_resource(ClientSend, "/send/<int:userId>/<string:message>")
api.add_resource(ClientUpdate, "/get/<int:userId>")

if __name__ == "__main__":
    app.run(debug=True)