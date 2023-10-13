# user_service

from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
}


# Generate a unique user ID
def generate_user_id():
    return max(users.keys()) + 1


# Create a new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user_id = generate_user_id()
    new_user = {"name": data["name"], "email": data["email"]}
    users[user_id] = new_user
    return jsonify(new_user), 201


# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


# Get a specific user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user is not None:
        return jsonify(user)
    return "User not found", 404


# Update a user by ID
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = users.get(user_id)
    if user is not None:
        user["name"] = data["name"]
        return jsonify(user)
    return "User not found", 404


# Delete a user by ID
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = users.pop(user_id, None)
    if user is not None:
        return "User deleted", 204
    return "User not found", 404


if __name__ == "__main__":
    app.run(port=5000, debug=True)
