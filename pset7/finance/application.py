import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get user_id from session
    user_id = session.get("user_id")

    # Query database for cash
    cash = db.execute("SELECT cash FROM users WHERE user_id = :i", i=user_id)[0]["cash"]

    # Query database for stocks of user
    query = db.execute("""
                       SELECT comp_name, symbol, SUM(shares)
                       FROM transactions JOIN companies
                       ON transactions.comp_id = companies.comp_id
                       WHERE transactions.user_id = :i
                       GROUP BY symbol
                       """, i=user_id)

    # Calculate total share value and format price in USD
    shares_total = 0
    for row in query:
        price = lookup(row["symbol"])["price"]
        total = price * row["SUM(shares)"]
        row["price"] = usd(price)
        row["total"] = usd(total)
        shares_total += total

    return render_template("index.html", total=usd(shares_total + cash), rows=query, cash=usd(cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Checks data from request
        if not request.form.get("symbol"):
            return apology("Missing symbol")
        if not request.form.get("shares"):
            return apology("Missing shares")
        try:
            if int(request.form.get("shares")) <= 0:
                return apology("Invalid shares")
        except ValueError:
            return apology("Invalid shares")

        # Checks if user exist
        user_id = session.get("user_id")
        if not user_id:
            return apology("Logout and login again")

        query = db.execute("SELECT cash FROM users WHERE user_id = :i", i=user_id)
        if len(query) != 1:
            return apology("User do not exist")

        # Available cash
        cash = query[0]["cash"]

        # Check for symbol
        quote_data = lookup(request.form.get("symbol").upper())
        if not quote_data:
            return apology("Invalid symbol")

        # Total price to buy the shares
        shares_price = quote_data["price"] * int(request.form.get("shares"))

        # Check if company exist in database
        query = db.execute("SELECT comp_id FROM companies WHERE symbol = :s", s=quote_data["symbol"])
        if len(query) == 0:
            comp_id = db.execute("INSERT INTO 'companies' ('comp_name', 'symbol') VALUES (:n, :s)",
                                 n=quote_data["name"], s=quote_data["symbol"])
        else:
            comp_id = query[0]["comp_id"]

        # Check if user can afford shares
        if shares_price > cash:
            return apology("Can't afford")

        # Insert transaction
        db.execute("""
                   INSERT INTO 'transactions' ('user_id', 'comp_id', 'shares', 'price', 'time')
                   VALUES (:u, :c, :s, :p, datetime('now', 'utc'))
                   """, u=user_id, c=comp_id, s=int(request.form.get("shares")), p=quote_data["price"])

        # Update cash for user
        cash -= shares_price
        db.execute("UPDATE users SET cash=:c WHERE user_id = :i", c=cash, i=user_id)

        # Flash message
        flash("Bought")

        # Redirect to index
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get user_id from session
    user_id = session["user_id"]

    # Query the database for transactions
    query = db.execute("""
                       SELECT symbol, shares, shares * price, time
                       FROM transactions JOIN companies
                       ON transactions.comp_id = companies.comp_id
                       WHERE transactions.user_id = :i
                       """, i=user_id)

    # Format the total as USD
    for row in query:
        row["total"] = usd(abs(row["shares * price"]))

    # Serve history
    return render_template("history.html", rows=query)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Check data from request
        if not request.form.get("symbol"):
            return apology("Missing symbol")

        # Lookup current price for symbol
        quote_data = lookup(request.form.get("symbol").upper())

        # Check quote
        if not quote_data:
            return apology("Invalid symbol")

        # Serve quoted
        return render_template("quoted.html", name=quote_data["name"],
                               symbol=quote_data["symbol"], usd=usd(quote_data["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        data = request.form

        # Check data from request
        if not data.get("username"):
            return apology("Missing username")
        if not data.get("password"):
            return apology("Missing password")
        if not data.get("password") == data.get("confirmation"):
            return apology("Passwords don't match")

        # Check if user exists
        row = db.execute("SELECT username FROM users WHERE username = :u",
                         u=data.get("username"))
        if len(row) != 0:
            return apology("Username taken")

        # Insert user
        user_id = db.execute("INSERT INTO users ('username', 'hash') VALUES (:u, :h)",
                             u=data.get("username"), h=generate_password_hash(data.get("password")))

        # Remember which user has logged in
        session["user_id"] = user_id

        # Redirect user to home page
        flash('Registered')
        return redirect("/")

    else:
        # Serve register
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Get user_id from session
    user_id = session.get("user_id")

    if request.method == "POST":
        data = request.form

        # Checks data from request
        if not data.get("symbol"):
            return apology("Missing symbol")
        if not data.get("shares"):
            return apology("Missing shares")

        # Query database for available shares
        query = db.execute("""
                           SELECT symbol, SUM(shares), companies.comp_id
                           FROM transactions JOIN companies
                           ON transactions.comp_id = companies.comp_id
                           WHERE transactions.user_id = :i AND symbol = :s
                           GROUP BY symbol
                           """, i=user_id, s=data.get("symbol"))

        # Checks if user has requested number of shares
        if int(data.get("shares")) > query[0]["SUM(shares)"]:
            return apology("Too many shares")

        # Get current price of shares
        price = lookup(data.get("symbol"))["price"]

        # Query database for cash
        cash = db.execute("SELECT cash FROM users WHERE user_id = :i", i=user_id)[0]["cash"]

        # Update cash
        cash += price * int(data.get("shares"))
        db.execute("UPDATE users SET cash = :c", c=cash)

        # Insert transaction
        db.execute("""
                   INSERT INTO 'transactions' ('user_id', 'comp_id', 'shares', 'price', 'time')
                   VALUES (:u, :c, :s, :p, datetime('now', 'utc'))
                   """, u=user_id, c=query[0]["comp_id"],  p=price,
                   s=-int(request.form.get("shares")))

        # Redirect
        flash('Sold')
        return redirect("/")
    else:
        # Query database for symbols of available stocks
        query = db.execute("""
                           SELECT symbol
                           FROM transactions JOIN companies
                           ON transactions.comp_id = companies.comp_id
                           WHERE transactions.user_id = :i
                           GROUP BY symbol
                           """, i=user_id)

        # Serve sell
        return render_template("sell.html", rows=query)


@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():
    """Resets user's password"""
    if request.method == "POST":
        data = request.form

        # Checks data from request
        if not data.get("current-password"):
            return apology("Missing current password")
        if not data.get("new-password"):
            return apology("Missing new password")
        if not data.get("new-password") == data.get("new-password-confirm"):
            return apology("Passwords don't match")

        # Get user_id from session
        user_id = session["user_id"]

        # Verify password
        query = db.execute("SELECT hash FROM users WHERE user_id = :i", i=user_id)

        if not check_password_hash(query[0]["hash"], request.form.get("current-password")):
            return apology("Incorrect password")

        # Update password
        db.execute("UPDATE users SET hash = :h WHERE user_id = :i",
                   h=generate_password_hash(request.form.get("new-password")), i=user_id)

        # Redirect
        flash("Password reset")
        return redirect("/")
    else:
        # Server reset
        return render_template("reset.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add money in user's account"""
    if request.method == "POST":
        data = request.form

        # Checks data from request
        if not data.get("money"):
            return apology("Missing money")

        # Get user_id from session
        user_id = session["user_id"]

        db.execute("UPDATE users SET cash = cash + :c WHERE user_id = :i", c=data.get("money"), i=user_id)

        flash("Money added")
        return redirect("/")
    else:
        # Serve add
        return render_template("add.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
