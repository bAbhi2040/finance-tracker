from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        print(f"Creating user: {username}")

        new_user = User(
            username=username,
            password=password   
        )

        db.session.add(new_user)
        db.session.commit()

        print("User saved!")

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()

        if user:
            print("Found user")
        else:
            print("User not found")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":  
    with app.app_context(): 
        db.create_all()
        for user in User.query.all():
            print(user.username)
        
    app.run(debug=True)
