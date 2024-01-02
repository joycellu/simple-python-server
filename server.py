# Imports
from flask import Flask, request
from json import load, dump

# Init Flask app
app = Flask(__name__)


@app.route("/", methods=["GET", "POST", "DELETE"])
def main():
    if request.method == "GET":
        return request_get(request)
    elif request.method == "POST":
        return request_post(request)
    elif request.method == "DELETE":
        return request_delete(request)
    else:
        return {"success": 0, "message": f"{request.method} Unsuccessful"}


# methods
def request_get(param):
    """
    Handles 'GET' request to the '/' endpoint. Queries the database and return all items.
    Query Parameters: None
    Headers: None
    Body: None
    """
    json_data = {}
    with open("database.json", "r") as f:
        json_data = load(f)

    response = {"data": json_data, "message": "GET Request Recieved", "success": 1}

    return response


def request_post(param):
    """
    Handles 'POST' request to the '/' endpoint. Adds an additional item to the database.
    Query Parameters:
        key: sample_key
        Headers:
    Content-Type: application/json
    Body:raw, Example:
    {
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "score": 9.2
    }
    """
    # Verfiy "key"
    if ("key" not in param.args) or (param.args.get("key") != "sample_key"):
        return {"success": 0, "message": "Incorrect parameter 'key'"}

    json_data = {}
    with open("database.json", "r") as f:
        json_data = load(f)
        json_data.append(param.get_json())
    with open("database.json", "w") as f:
        dump(json_data, f)

    response = {"data": json_data, "message": "POST Request Recieved", "success": 1}

    return response


def request_delete(param):
    """
    Handles 'DELETE' request to the '/' endpoint. Removes all entries of books with the provided title.
    Query Parameters:
        key: sample_key
        title: title of target deletion (Brave New World)
    Headers: None
    Body: None
    """
    # Verfiy "key"
    if ("key" not in param.args) or (param.args.get("key") != "sample_key"):
        return {"success": 0, "message": "Incorrect parameter 'key'"}
    elif "title" not in param.args:
        return {"success": 0, "message": "Missing parameter 'title'"}

    with open("database.json", "r") as f:
        json_data = load(f)
        updated_data = list(
            filter(lambda x: x["title"] != param.args.get("title"), json_data)
        )
    with open("database.json", "w") as f:
        dump(updated_data, f)

    response = {
        "data": updated_data,
        "message": "DELETE Request Recieved",
        "success": 1,
    }

    return response
