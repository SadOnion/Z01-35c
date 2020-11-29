from flask import Flask
from flask_restful import Api,Resource
from collections import defaultdict
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

messages = defaultdict(list)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL,API_URL,config={"app_name":"name"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


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