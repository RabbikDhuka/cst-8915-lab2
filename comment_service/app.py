from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize an in-memory dictionary to store comments
comments = {
    1: {"user_id": "1", "post_id": 2, "comment_text": "This is a sample comment"},
    2: {"user_id": "2", "post_id": 1, "comment_text": "This is a sample comment 2"},
}


# Create a new comment
@app.route("/comments", methods=["POST"])
def create_comment():
    data = request.json
    comment_id = len(comments) + 1
    comments[comment_id] = {
        "user_id": data["user_id"],
        "post_id": data["post_id"],
        "comment_text": data["comment_text"],
    }
    return jsonify({"comment_id": comment_id}), 201


# Get a comment by comment_id
@app.route("/comments/<int:comment_id>", methods=["GET"])
def get_comment(comment_id):
    comment = comments.get(comment_id)
    if comment:
        return jsonify(comment), 200
    return "Comment not found", 404


# Update an existing comment
@app.route("/comments/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    if comment_id in comments:
        data = request.json
        comments[comment_id]["user_id"] = data["user_id"]
        comments[comment_id]["post_id"] = data["post_id"]
        comments[comment_id]["comment_text"] = data["comment_text"]
        return jsonify({"message": "Comment updated"}), 200
    return "Comment not found", 404


# Delete a comment by comment_id
@app.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    if comment_id in comments:
        del comments[comment_id]
        return jsonify({"message": "Comment deleted"}), 200
    return "Comment not found", 404


# Get a list of all comments
@app.route("/comments", methods=["GET"])
def get_all_comments():
    return jsonify(comments), 200


if __name__ == "__main__":
    app.run(port=5003, debug=True)
