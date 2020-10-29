from voized import app, db
from voized.models import User
from flask import request, jsonify,make_response, g
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_web_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token)
        if not (user and user.validate_passowrd(password)):
             return False
    g.user = user
    return True

@app.route('/user/login', methods = ["POST"])
def login_user():
    if request.method == "POST":
        print(request.json)
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify({"status": "error", "message":"Input a valid username or password!"}), 400
    user = User.query.filter_by(username=username).first() or User.query.filter_by(email = username).first()
    if (not user) or (not user.validate_password(password)):
        return jsonify({"status": "error", "message":"Invaid username or password!"}), 400
    token = user.generate_web_token(9999999999)
    return jsonify({ "status" :'success',"username": user.username,"email":user.email, "token": token}), 200


@app.route("/user/register", methods = ["POST"])
def register_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get("email")
        if username is None or password is None:
            return {"status": "error", "message":"Input a valid username or password!"}, 400
        if  User.query.filter_by(username = username).first():
            return {"status": "error", "message": "Username already taken."}, 409
        if User.query.filter_by(email = email).first():
            return {"status": "error", "message": "Email already taken."}, 400

        user = User(username=username, password=password, email=email)
        token = user.generate_web_token(9999999999)
        db.session.add(user)
        db.session.commit()

        return jsonify({ "status": "success","username": username, "token": token, "exp_sec":259200}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": "An unknwon error occured!"})