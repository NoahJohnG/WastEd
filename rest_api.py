# REST API
# buffer for "cans" which have name(like its location),
# waste category count, and ~arbitrary~ score

from flask import Flask
from flask_restful import Api, Resource, reqparse


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
    # get can
    def get(self, name):
        for can in cans:
            if(name == cans["name"]):
                return can, 200
        return "User not found", 404

    # add new can
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("Trash")
        parser.add_argument("Compost")
        parser.add_argument("Recycling")
        parser.add_argument("Score")
        args = parser.parse_args()

        for can in cans:
            if(name == can["name"]):
                return "Can with name {} already exists".format(name), 400
        can = {
            "name": name,
            "Trash": args["Trash"],
            "Recycling": args["Recycling"],
            "Compost": args["Compost"],
            "Score": args["Score"]
        }
        cans.append(can)
        return can, 201

    # update can details, i.e. increment trash comp recyc count
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


    # deletes a can and its data
    def delete(self, name):
        global cans
        cans = [can for can in cans if can["name"] != can]
        return "{} is deleted.".format(name), 200



