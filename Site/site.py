from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "slo-hacks-wasted",
})

db = firestore.client()

app = Flask(__name__)
api = Api(app)

cans = [
    {
        "name": "UU Chandler Lounge",
        "Trash": 0,
        "Compost": 0,
        "Recycling": 0,
        "Score": 0
    },
    {
        "name": "wastEd OG bin",
        "Trash": 0,
        "Compost": 0,
        "Recycling": 0,
        "Score": 0
    },
    {
        "name": "Chumash Auditorium",
        "Trash": 0,
        "Compost": 0,
        "Recycling": 0,
        "Score": 0
    },
    {
        "name": "The Ave",
        "Trash": 0,
        "Compost": 0,
        "Recycling": 0,
        "Score": 0
    },
    {
        "name": "Baker Science",
        "Trash": 0,
        "Compost": 0,
        "Recycling": 0,
        "Score": 0
    }

]

class Can(Resource):
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("Trash")
        parser.add_argument("Recycling")
        parser.add_argument("Compost")
        parser.add_argument("Score")
        args = parser.parse_args()

        # update can's fields
        for can in cans:
            if(can == cans["name"]):
                can["Trash"] = args["Trash"]
                can["Recycling"] = args["Recycling"]
                can["Compost"] = args["Compost"]
                can["Score"] = args["Score"]
                return can, 200
        # can not found, create new can
        can = {
            "name": name,
            "Trash": args["Trash"],
            "Recycling": args["Recycling"],
            "Compost": args["Compost"],
            "Score": args["Score"]
        }
        cans.append(can)
        return can, 201

        # get can
    def get(self, name):
        for can in cans:
            if (name == cans["name"]):
                return can, 200
        return "User not found", 404


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/leaderboard")
def leaderboard():
    users_ref = db.collection(u'names')
    docs = users_ref.get()

    names = {}
    for doc in docs:
        names[doc.id] = doc.to_dict()

    return render_template("leaderboard.html", names=names)



if __name__ == "__main__":
    app.run(debug=True)