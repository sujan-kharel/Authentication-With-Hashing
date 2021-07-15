from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    userName = db.Column(db.Text, unique=True, nullable=False)
    hashed = db.Column(db.Text, nullable=False)


class insertUser:
    def __init__(self, name, userName, hashed):
        self.name = name
        self.userName = userName
        self.hashed = hashed

        # creating an object to insert each filed all at once
        user = User(name=name, userName=userName, hashed=hashed)
        db.session.add(user)
        db.session.commit()
        db.session.close()


# renders main menu page
@app.route("/")
def index():
    return render_template("index.html")


# main menu request
@app.route("/requestPage", methods=["POST"])
def getAttribute():
    if request.method == "POST":
        if request.form.get("main"):
            return redirect("/")
        if request.form.get("register"):
            return redirect("/register")
        elif request.form.get("login"):
            return redirect("/login")
        else:
            return render_template("index.html")


# renders page based on request
@app.route("/register")
def showRegisterPage():
    return render_template("register.html")


@app.route("/login")
def showLoginPage():
    return render_template("login.html")


# registration using post method request
@app.route("/register", methods=["post"])
def register():
    if request.method == "POST":
        name = str(request.form.get("firstName"))
        userName = str(request.form.get("userName"))
        password = str(request.form.get("password"))

        if not name or not userName or not password:
            return "one or more fields are missing!"

        existingUser = User.query.filter_by(userName=userName).first()

        # if not duplicate, registers users
        if not existingUser:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            insertUser(name, userName, hashed)
            return "<h1> Registered Successfully! </h1>"
    return "<h1> Please provide a different user name </h>"


# authentication
@app.route("/login", methods=["post"])
def login():
    if request.method == "POST":
        userName = str(request.form.get("userName"))
        password = str(request.form.get("password"))

        if not userName or not password:
            return "One or more fields are missing!"

        existingUser = User.query.filter_by(userName=userName).first()

        if not existingUser:
            return " <h1> User not found! </h1>"
        else:
            if bcrypt.checkpw(password.encode('utf-8'), existingUser.hashed):
                return "<h1> Welcome back, " + existingUser.name + "!! </h1>"

    return redirect("/login")


""" --for testing --
  # queries all the users and prints name, user name, and their salted hashed passwords
  
users = User.query.all()
for user in users:
    print(user.name, user.userName, user.hashed)
    
    """

if __name__ == "__main__":
    app.run(debug=True)
