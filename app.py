from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change to a more secure one for production

DB = os.path.join(os.path.dirname(__file__), "library.db")  # Always use absolute path

# -------------------- DATABASE --------------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id TEXT UNIQUE NOT NULL
        )
    """)
    # Borrow log table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS borrow_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_title TEXT NOT NULL,
            borrower_name TEXT NOT NULL,
            borrower_id TEXT NOT NULL,
            date_borrowed TEXT NOT NULL,
            date_returned TEXT
        )
    """)
    conn.commit()
    conn.close()

# -------------------- ROUTES --------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        name = request.form["name"].strip()
        user_id = request.form["user_id"].strip()
        if not name or not user_id:
            error = "Please enter both Name and Student ID"
        else:
            try:
                with get_db() as conn:
                    conn.execute("INSERT INTO users(name, user_id) VALUES(?,?)", (name, user_id))
                return redirect("/login")
            except sqlite3.IntegrityError:
                error = "Student ID already exists"
    return render_template("register.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user_id = request.form["user_id"].strip()
        with get_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        if user:
            session["user_name"] = user["name"]
            session["user_id"] = user["user_id"]
            return redirect("/")
        else:
            error = "Invalid Student ID"
    return render_template("login.html", error=error)

@app.route("/", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        book = request.form["book_title"].strip()
        if book:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO borrow_log(book_title, borrower_name, borrower_id, date_borrowed) VALUES(?,?,?,?)",
                    (book, session["user_name"], session["user_id"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )

    with get_db() as conn:
        borrows = conn.execute(
            "SELECT * FROM borrow_log WHERE date_returned IS NULL ORDER BY date_borrowed DESC"
        ).fetchall()

    return render_template("home.html", borrows=borrows, user_name=session.get("user_name"))

@app.route("/return/<int:borrow_id>")
def return_book(borrow_id):
    if "user_id" not in session:
        return redirect("/login")

    with get_db() as conn:
        conn.execute(
            "UPDATE borrow_log SET date_returned=? WHERE id=?",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), borrow_id)
        )
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -------------------- RUN --------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
