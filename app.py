from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "real_estate_secret_key"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
        except Exception as e:
            conn.close()
            return "Username already exists!"

        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/dashboard")
        else:
            return "Invalid username or password!"
    
    
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    properties = conn.execute(
        "SELECT * FROM properties WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("dashboard.html", properties=properties, username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/add_property", methods=["GET", "POST"])
def add_property():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        location = request.form["location"]
        price = request.form["price"]
        status = request.form["status"]

        conn = get_db()
        conn.execute(
            "INSERT INTO properties (user_id, title, location, price, status) VALUES (?, ?, ?, ?, ?)",
            (session["user_id"], title, location, price, status)
        )
        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_property.html")


@app.route("/delete_property/<int:property_id>")
def delete_property(property_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    conn.execute(
        "DELETE FROM properties WHERE id = ? AND user_id = ?",
        (property_id, session["user_id"])
    )
    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/edit_property/<int:property_id>", methods=["GET", "POST"])
def edit_property(property_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    if request.method == "POST":
        title = request.form["title"]
        location = request.form["location"]
        price = request.form["price"]
        status = request.form["status"]

        conn.execute(
            "UPDATE properties SET title = ?, location = ?, price = ?, status = ? WHERE id = ? AND user_id = ?",
            (title, location, price, status, property_id, session["user_id"])
        )
        conn.commit()
        conn.close()

        return redirect("/dashboard")

    property = conn.execute(
        "SELECT * FROM properties WHERE id = ? AND user_id = ?",
        (property_id, session["user_id"])
    ).fetchone()
    conn.close()

    return render_template("edit_property.html", property=property)


if __name__ == "__main__":
    app.run(debug=True)