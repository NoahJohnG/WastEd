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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/leaderboard")
def leaderboard():
    users_ref = db.collection(u'names').order_by(
        u'Score', direction =firestore.Query.DESCENDING
    )
    docs = users_ref.get()

    return render_template("leaderboard.html", docs=docs)



if __name__ == "__main__":
    app.run(debug=True)