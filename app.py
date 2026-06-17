from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import (generate_password_hash, check_password_hash)
from datetime import date
from sqlalchemy import extract

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
    transaction_date = db.Column(
        db.Date,
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
                error="Username can't be blank",
                form = request.form
            )
        if not password:
            return render_template(
                "register.html",
                error="Password can't be blank",
                form = request.form
            )
        if len(password) < 8 or len(password) > 30:
            return render_template(
                "register.html",
                error="Password must be between 8 to 30 characters",
                form = request.form
            )
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template(
                "register.html",
                error="Username already exists",
                form = request.form
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
                error="User not found",
                form = request.form
            )
        elif not check_password_hash(user.password, password):
            return render_template(
                "login.html",
                error="Incorrect password",
                form = request.form
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
    query = Transaction.query.filter_by(user_id=session["user_id"])

    filter_option = request.args.get("filter_option", "All")
    if filter_option == "Income":
        query = query.filter_by(transaction_type="Income")
    elif filter_option == "Expenses":
        query = query.filter_by(transaction_type="Expense")

    search_term = request.args.get("search", "")
    if search_term:
        query = query.filter(Transaction.description.contains(search_term))

    today = date.today()
    date_search = request.args.get("date_search", "Any")
    if date_search == "Today":
        query = query.filter(Transaction.transaction_date == today)
    elif date_search == "This month":
        query = query.filter(extract('month', Transaction.transaction_date) == today.month,
                             extract('year', Transaction.transaction_date) == today.year
                             )
    elif date_search == "This year":
        query = query.filter(extract('year', Transaction.transaction_date) == today.year)

    transactions = query.order_by(Transaction.id.desc()).all()

    income_total = 0
    expense_total = 0

    for transaction in transactions:
        if transaction.transaction_type == "Income":
            income_total += transaction.amount
        elif transaction.transaction_type == "Expense":
            expense_total += transaction.amount

    balance = income_total - expense_total
    transaction_count = len(transactions)

    category_total = {}

    for transaction in transactions:
        if transaction.category not in category_total:
            category_total[transaction.category] = 0
        category_total[transaction.category] += transaction.amount
    sorted_categories = sorted(
        category_total.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return render_template(
        "dashboard.html",
        user=user,
        transactions=transactions,
        income_total=round(income_total, 2),
        expense_total=round(expense_total, 2),
        transaction_count=transaction_count,
        balance=round(balance, 2),
        filter_option=filter_option,
        search_term=search_term,
        date_search=date_search,
        sorted_categories=sorted_categories
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
        date_string = request.form["date"]
        
        if amount <= 0:
            return render_template(
            "add_transaction.html",
            error="The entered amount must be greater than 0",
            form = request.form
        )
        if not description:
            return render_template(
                "add_transaction.html",
                error="Must have a description",
                form = request.form
            )
        if not date_string:
            return render_template(
                "add_transaction.html",
                error="Must have a date",
                form = request.form
            )

        new_transaction = Transaction(
            amount=amount,
            category=category,
            description=description,
            user_id=session["user_id"],
            transaction_type=transaction_type,
            transaction_date=date.fromisoformat(request.form["date"])
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
                error="The entered amount must be greater than 0",
                form = request.form
                )
            if not description:
                return render_template(
                    "edit_transaction.html",
                    transaction=transaction,
                    error="Must have a description",
                    form = request.form
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
