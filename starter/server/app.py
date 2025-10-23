# Import necessary libraries and modules
from bson.objectid import ObjectId
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
import os

# Define the MongoDB connection string
MONGODB_SERVER = "mongodb+srv://teamthree:friday@ece461l.38dktsx.mongodb.net/Team_Project?retryWrites=true&w=majority&appName=ECE461L"

# Initialize a new Flask web application
app = Flask(__name__, static_folder='../client/build/static', static_url_path='/static')
app.config["MONGO_URI"] = MONGODB_SERVER
mongo = PyMongo()
mongo.init_app(app)
CORS(app)

# --- Existing API routes ---

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "username and password required"}), 400

    login_success = mongo.db.user_info.find_one({"username": username, "password": password})
    if login_success:
        user_safe = {"_id": str(login_success.get("_id")), "username": login_success.get("username"), "projects": login_success.get("projects", [])}
        return jsonify({"message": "Login successful", "user": user_safe}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "username and password required"}), 400

    existing_user = mongo.db.user_info.find_one({"username": username})
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    user_doc = {
        "username": username,
        "password": password,
        "projects": []
    }

    result = mongo.db.user_info.insert_one(user_doc)
    inserted_id = str(result.inserted_id)

    user_safe = {"_id": inserted_id, "username": username, "projects": []}
    return jsonify({"message": "User added successfully", "user": user_safe}), 201

@app.route('/forgot', methods=['POST'])
def forgot_password():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"message": "username required"}), 400

    existing_user = mongo.db.user_info.find_one({"username": username})
    if not existing_user:
        return jsonify({"message": "User does not exist"}), 404

    return jsonify({"message": f"Your password is: {existing_user['password']}"}), 200

# --- Placeholder routes (unchanged, return empty JSON) ---
@app.route('/main')
def mainPage():
    return jsonify({})

@app.route('/join_project', methods=['POST'])
def join_project():
    return jsonify({})

@app.route('/get_user_projects_list', methods=['POST'])
def get_user_projects_list():
    return jsonify({})

@app.route('/create_project', methods=['POST'])
def create_project():
    return jsonify({})

@app.route('/get_project_info', methods=['POST'])
def get_project_info():
    return jsonify({})

@app.route('/get_all_hw_names', methods=['POST'])
def get_all_hw_names():
    return jsonify({})

@app.route('/get_hw_info', methods=['POST'])
def get_hw_info():
    return jsonify({})

@app.route('/check_out', methods=['POST'])
def check_out():
    return jsonify({})

@app.route('/check_in', methods=['POST'])
def check_in():
    return jsonify({})

@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    return jsonify({})

@app.route('/api/inventory', methods=['GET'])
def check_inventory():
    return jsonify({})

# --- React app static file serving ---

# Serve React static files from build folder
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('../client/build/static', path)

# Serve React index.html for all other routes (SPA)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    build_dir = os.path.join(os.path.dirname(__file__), '../client/build')
    if path != "" and os.path.exists(os.path.join(build_dir, path)):
        return send_from_directory(build_dir, path)
    else:
        return send_from_directory(build_dir, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Heroku's port or default to 5000
    app.run(host='0.0.0.0', port=port)
