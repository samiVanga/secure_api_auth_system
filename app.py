from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route("/")
def home():
    return "Flask app is running!"


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"message": "Login Success", "access_token": access_token})
    else:
        return jsonify({"message": "Login Failed"}), 401


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)