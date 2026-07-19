from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "nexora_secret_key"

# Home
@app.route("/")
def home():
    return render_template("index.html")

# About
@app.route("/about")
def about():
    return render_template("about.html")

# Internships

@app.route("/internships")
def internships():

    search = request.args.get("search", "")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if search:
        cursor.execute("""
        SELECT * FROM internships
        WHERE company LIKE ?
        OR role LIKE ?
        OR location LIKE ?
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ))
    else:
        cursor.execute("SELECT * FROM internships")

    internships = cursor.fetchall()

    conn.close()

    return render_template(
        "internships.html",
        internships=internships,
        search=search
    )

# ---------------- APPLY INTERNSHIP ----------------

@app.route("/apply/<int:internship_id>")
def apply(internship_id):

    if "user_id" not in session:

        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM applications
    WHERE user_id=? AND internship_id=?
    """,
    (
        session["user_id"],
        internship_id
    ))

    existing = cursor.fetchone()

    if existing:

        conn.close()

        return redirect(url_for("applications"))

    cursor.execute("""
    INSERT INTO applications(user_id, internship_id)

    VALUES(?,?)
    """,
    (
        session["user_id"],
        internship_id
    ))

    conn.commit()

    conn.close()

    return redirect(url_for("applications"))

# Internship Details
@app.route("/internship/<int:id>")
def internship(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM internships WHERE id=?",
        (id,)
    )

    internship = cursor.fetchone()

    conn.close()

    return render_template(
        "internship_details.html",
        internship=internship
    )

# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        skills = request.form["skills"]

        if password != confirm_password:
            return "Passwords do not match!"

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:

            cursor.execute("""
            INSERT INTO users(name,email,password,skills)
            VALUES(?,?,?,?)
            """,
            (
                name,
                email,
                hashed_password,
                skills
            ))

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            return "Email already registered!"

        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            if check_password_hash(user[3], password):

                session["user_id"] = user[0]
                session["name"] = user[1]
                session["email"] = user[2]
                session["skills"] = user[4]

                return redirect(url_for("dashboard"))

        return "Invalid Email or Password"

    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        name=session["name"],
        email=session["email"],
        skills=session["skills"]
    )

# Applications
@app.route("/applications")
def applications():

    if "user_id" not in session:

        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    internships.company,

    internships.role,

    internships.location,

    internships.stipend,

    internships.duration,

    applications.status

    FROM applications

    JOIN internships

    ON applications.internship_id = internships.id

    WHERE applications.user_id=?

    """,

    (session["user_id"],))

    applications = cursor.fetchall()

    conn.close()

    return render_template(

        "applications.html",

        applications=applications

    )

# Contact
@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    