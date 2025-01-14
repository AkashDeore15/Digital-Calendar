from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return {"message": "Digital Calendar API is running!"}
