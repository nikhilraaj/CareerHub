import os
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE_URL = "careerapp.db"
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key_here")  # Replace with your actual secret key

if not os.path.exists(DATABASE_URL):
    from init_db import create_tables
    create_tables()


app = Flask(__name__)
app.secret_key = SECRET_KEY  

# Function to connect to SQLite
def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row 
    return conn

@app.route("/", methods=["GET"])
def Home():
    is_logged_in = 'user_id' in session
    return render_template("index.html", is_logged_in=is_logged_in)

@app.route("/get_all_questions", methods=["GET"])
def get_all_questions():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    is_logged_in = 'user_id' in session

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions ORDER BY topic ASC;")
    questions = cur.fetchall()
    conn.close()

    question_list = [{
        "sr_no": idx + 1,
        "id": question["id"],
        "topic": question["topic"],
        "title": question["title"],
        "practice_link": question["practice_link"],
        "done": bool(question["done"])
    } for idx, question in enumerate(questions)]

    return render_template("qsn.html", questions=question_list,is_logged_in=is_logged_in)

@app.route("/edit_question/<int:id>", methods=["POST"])
def edit_question(id):
    data = request.form
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE questions SET topic = ?, title = ?, practice_link = ? WHERE id = ?",
                (data["topic"], data["title"], data["practice_link"], id))
    conn.commit()
    conn.close()
    return redirect(url_for('get_all_questions'))

@app.route("/delete_question/<int:id>", methods=["POST"])
def delete_question(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_all_questions'))



@app.route("/update_done/<int:id>", methods=["POST"])
def update_done(id):
    done_status = request.form.get('done') == 'on'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE questions SET done = ? WHERE id = ?", (int(done_status), id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Status updated successfully!"})

@app.route("/add_question", methods=["POST"])
def add_question():
    data = request.get_json()
    if "topic" not in data or "title" not in data or "practice_link" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO questions (topic, title, practice_link, done) VALUES (?, ?, ?, ?)",
                (data["topic"], data["title"], data["practice_link"], False))
    conn.commit()
    conn.close()
    return jsonify({"message": "Question added successfully!"}), 201

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("User already exists!", "danger")
            return redirect(url_for("register"))

        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("Home"))

        flash("Invalid username or password!", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return redirect(url_for("Home"))

@app.route("/api/add_question", methods=["POST"])
def api_add_question():
    data = request.get_json()
    if not data or "topic" not in data or "title" not in data or "practice_link" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO questions (topic, title, practice_link, done) VALUES (?, ?, ?, ?)",
                (data["topic"], data["title"], data["practice_link"], 0))
    conn.commit()
    conn.close()

    return jsonify({"message": "Question added successfully!"}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
