from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import (generate_password_hash, check_password_hash)

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"

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

class Transaction(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    amount = db.Column(
        db.Float,
        nullable=False
    )
    category = db.Column(
        db.String(100),
        nullable=False
    )
    description = db.Column(
        db.String(200)
    )
    user_id = db.Column(
        db.Integer,
        nullable=False     
    )
    transaction_type = db.Column(
        db.String(20),
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

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password=hashed_password   
        )

        if not username:
            return render_template(
                "register.html",
                error="Username can't be blank"
            )
        if not password:
            return render_template(
                "register.html",
                error="Password can't be blank"
            )
        if len(password) < 8 or len(password) > 30:
            return render_template(
                "register.html",
                error="Password must be between 8 to 30 characters"
            )
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template(
                "register.html",
                error="Username already exists"
            )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            return render_template(
                "login.html",
                error="User not found"
            )
        elif not check_password_hash(user.password, password):
            return render_template(
                "login.html",
                error="Incorrect password"
            )
        else:
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))      
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))  
    user = User.query.get(session["user_id"])
    transactions = Transaction.query.filter_by(user_id=session["user_id"]).order_by(Transaction.id.desc()).all()

    income_total = 0
    expense_total = 0

    for transaction in transactions:
        if transaction.transaction_type == "Income":
            income_total += transaction.amount
        elif transaction.transaction_type == "Expense":
            expense_total += transaction.amount

    balance = income_total - expense_total
    transaction_count = len(transactions)

    return render_template(
        "dashboard.html",
        user=user,
        transactions=transactions,
        income_total=round(income_total, 2),
        expense_total=round(expense_total, 2),
        transaction_count=transaction_count,
        balance=round(balance, 2)
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    if "user_id" not in session:
        return redirect(url_for("login"))   
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        description = request.form["description"]
        transaction_type = request.form["transaction_type"]

        if amount <= 0:
            return render_template(
            "add_transaction.html",
            error="The entered amount must be greater than 0"
        )
        if not description:
            return render_template(
                "add_transaction.html",
                error="Must have a description"
            )

        new_transaction = Transaction(
            amount=amount,
            category=category,
            description=description,
            user_id=session["user_id"],
            transaction_type=transaction_type
        )

        db.session.add(new_transaction)
        db.session.commit()

        return redirect(url_for("dashboard"))   
    return render_template("add_transaction.html")

@app.route("/delete_transaction/<int:transaction_id>")
def delete_transaction(transaction_id):
    if "user_id" not in session:
        return redirect(url_for("login"))   
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return redirect(url_for("dashboard"))
    if transaction.user_id == session["user_id"]:
        db.session.delete(transaction)
        db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/edit_transaction/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    transaction = Transaction.query.get(transaction_id)

    if not transaction:
        return redirect(url_for("dashboard"))   
    if transaction.user_id == session["user_id"]:
        if request.method == "POST":
            amount = float(request.form["amount"])
            category = request.form["category"]
            description = request.form["description"]
            transaction_type = request.form["transaction_type"]

            if amount <= 0:
                return render_template(
                "edit_transaction.html",
                transaction=transaction,
                error="The entered amount must be greater than 0"
                )
            if not description:
                return render_template(
                    "edit_transaction.html",
                    transaction=transaction,
                    error="Must have a description"
                )
            
            transaction.amount = amount
            transaction.category = category
            transaction.description = description
            transaction.transaction_type = transaction_type

            db.session.commit()

            return redirect(url_for("dashboard"))
        return render_template(
            "edit_transaction.html",
            transaction=transaction
            )
    else:
        return redirect(url_for("dashboard"))
        
if __name__ == "__main__":  
    with app.app_context(): 
        db.create_all()
        for user in User.query.all():
            print(user.username)   
    app.run(debug=True)
