import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# Get MongoDB URI from environment variable
uri = os.getenv("MONGO_URI", "your_default_mongo_uri_here")  # Fallback to a default URI if the environment variable is not set

# Initialize Flask app
app = Flask(__name__)

# Secret key for session management
app.secret_key = os.getenv("SECRET_KEY", "your_default_secret_key_here")

# Initialize MongoDB client within the route or app function to prevent issues with multi-threading
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["question_db"]
collection = db["questions"]
user_collection = db["users"]

@app.route("/", methods=["GET"])
def Home():
    is_logged_in = 'user_id' in session
    return render_template("index.html", is_logged_in=is_logged_in)

@app.route("/get_all_questions", methods=["GET"])
def get_all_questions():
    if "user_id" not in session:  # Check if user is logged in
        return redirect(url_for("login"))  # Redirect non-logged-in users to login page

    questions = collection.find().sort("topic", 1)  # 1 for ascending order
    question_list = []

    for idx, question in enumerate(questions, start=1):
        question_list.append({
            "sr_no": idx,
            "id": str(question["_id"]),
            "topic": question["topic"],
            "title": question["title"],
            "practice_link": question["practice_link"],
            "done": question.get("done", False)
        })

    return render_template("qsn.html", questions=question_list)

@app.route("/edit_question/<id>", methods=["POST"])
def edit_question(id):
    data = request.form
    update_data = {}

    if "topic" in data:
        update_data["topic"] = data["topic"]
    if "title" in data:
        update_data["title"] = data["title"]
    if "practice_link" in data:
        update_data["practice_link"] = data["practice_link"]

    collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    return redirect(url_for('get_all_questions'))

@app.route("/delete_question/<id>", methods=["POST"])
def delete_question(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Question not found"}), 404

    return redirect(url_for('get_all_questions'))

@app.route("/update_done/<id>", methods=["POST"])
def update_done(id):
    done_status = request.form.get('done') == 'on'
    collection.update_one({"_id": ObjectId(id)}, {"$set": {"done": done_status}})
    return jsonify({"message": "Status updated successfully!"})

@app.route("/add_question", methods=["POST"])
def add_question():
    data = request.get_json()

    if "topic" not in data or "title" not in data or "practice_link" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    question = {
        "topic": data["topic"],
        "title": data["title"],
        "practice_link": data["practice_link"]
    }

    collection.insert_one(question)
    return jsonify({"message": "Question added successfully!"}), 201

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if user_collection.find_one({"username": username}):
            flash("User already exists!", "danger")
            return redirect(url_for("register"))

        user_collection.insert_one({"username": username, "password": hashed_password})
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = user_collection.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])
            return redirect(url_for("Home"))

        flash("Invalid username or password!", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return redirect(url_for("Home"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
