from flask import Flask, render_template
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

flask_app = Flask(__name__)
flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///entries.db"

#Initialize the DB
db = SQLAlchemy(flask_app)

#Create db model
class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.now())



last_entry = [
                {"title":"sebsemilia",
                 "body":"aoooooo"
                },
                {"title:":"steffensemilia",
                 "body":"aoaoaooaoaooooooooo"
                }
             ]

@flask_app.route('/home')
def home():
    return render_template("home.html", last_entry=last_entry)


@flask_app.route('/hello')
def hello_world():
    return Response(
        'Hello world from Flask!\n',
        mimetype='text/plain'
    )



app = flask_app.wsgi_app
