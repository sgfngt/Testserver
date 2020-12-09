import argparse
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///entries.db"

#Initialize the DB
db = SQLAlchemy(app)

#Create db model
class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200))
    date_created = db.Column(db.DateTime)


@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/eingabe', methods=["GET", "POST"])
def eingabe():

    if request.method == "POST":
        inputMessage = request.form["message"]
        newMessage = Entries(message=inputMessage, date_created=datetime.now())

        #Push to DB
        try:
            db.session.add(newMessage)
            db.session.commit()
            return redirect("/eingabe")
        except:
            return "Fehler beim Hinzufuegen zur Datenbank"

    else:
        entries = Entries.query.order_by(Entries.id.desc())
        return render_template("eingabe.html", entries=entries)

if __name__ == '__main__':
    #set default values for host and port
    host = "0.0.0.0"
    port = 5000

    #Create argument parser to pass custom values for host and port
    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    parser.add_argument("--port")
    args = parser.parse_args()

    if args.host is not None:
        host = args.host
    if args.port is not None:
        port = args.port

    print("Starting Server on Port "+str(port))
    app.run(debug=True, host=host, port=port)