from cs50 import SQL
from flask import Flask, redirect, render_template, request, send_file, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, generate_qr, login_required

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///qrcode.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        file_path = generate_qr(url)

        if session.get("user_id"):
            db.execute(
                "INSERT INTO histories (user_id, qrcode_path, url) VALUES (?, ?, ?)",
                session["user_id"],
                file_path,
                url,
            )
        return render_template("generated.html", file_path=file_path, url=url)
    return render_template("index.html")


@app.route("/download/<path:file_path>", methods=["POST"])
def download(file_path):
    return send_file(file_path, as_attachment=True)


@app.route("/history", methods=["GET"])
@login_required
def history():
    histories = db.execute(
        "SELECT * FROM histories WHERE is_deleted = 0 AND user_id = ? ORDER BY timestamp DESC",
        session["user_id"],
    )
    return render_template("history.html", histories=histories)


@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    db.execute("UPDATE histories SET is_deleted = 1 WHERE id = ?", id)
    return redirect("/history")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password:
            return apology("required both username and password", 400)

        user = db.execute("SELECT username FROM users WHERE username = ?", username)
        if user:
            return apology("username already exists", 400)
        elif password != confirmation:
            return apology("passwords do not match")

        hashed_password = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, hashed_password) VALUES(?, ?)",
            username,
            hashed_password,
        )

        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hashed_password"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    return redirect("/")
