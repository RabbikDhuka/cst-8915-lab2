# post_service.py

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory posts data (a dictionary with post IDs as keys)
posts = {
    1: {"user_id": "1", "post": "Hello, world!"},
    2: {"user_id": "2", "post": "My first blog post"},
}


# Function to generate a unique post ID
def generate_post_id():
    return max(posts.keys()) + 1


# Function to fetch user information from the user service
def get_user_info(user_id):
    user_service_url = "http://127.0.0.1:5000/users/" + str(
        user_id
    )  # Replace with the actual host
    response = requests.get(user_service_url)
    return response.json() if response.status_code == 200 else None


# Create a new post
@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    user_id = data.get("user_id")
    user_info = get_user_info(user_id)

    if user_info:
        post_id = generate_post_id()
        new_post = {
            "user_id": user_id,
            "post": data.get("post", "This is a random post."),
        }
        posts[post_id] = new_post
        return jsonify(new_post), 201
    return "User not found", 404


# Get all posts
@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(posts)


# Get a specific post by ID
@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = posts.get(post_id)
    if post is not None:
        return jsonify(post)
    return "Post not found", 404


# Update a post by ID


@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json()
    post = posts.get(post_id)
    if post is not None:
        post["post"] = data["post"]
        return jsonify(post)
    return "Post not found", 404


# Delete a post by ID


@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = posts.pop(post_id, None)
    if post is not None:
        return "Post deleted", 204
    return "Post not found", 404


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")
