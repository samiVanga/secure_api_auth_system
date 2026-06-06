from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    notes = db.relationship('Note', backref='author', lazy=True)
    def __repr__(self):
        return f'<User {self.username}>'

class Note(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

def validatePassword(password):
    returnMessage=""
    if len(password)<8:
        returnMessage+= "Password needs to a minimum of 8 characters\n"
    if not re.search(r"[A-Z]",password):
        returnMessage+= "Password needs to contain at least one uppercase character\n"
    if not re.search(r"[0-9]",password):
        returnMessage+= "Password needs to contain at least one number\n"
    if not re.search(r"[!@£#$%^&*():?\~/;<>|{}+=_-`]", password):
        returnMessage+= "Password needs to contain at least one valid special character\n"
    if len(returnMessage)>0:
        return returnMessage
    return None


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/register-page")
def register_page():
    return render_template('register.html')

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
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

@app.route("/register", methods=["POST"])
@limiter.limit("3 per minute")
def register():
    data = request.get_json()

    username = data["username"]
    password = data["password"]
    repassword= data['repassword']


    if not username or not password:
        return jsonify({"message":"please enter a username and password"}),400
    
    if not repassword:
        return jsonify({"message":"please retype in your password"}),400
    
    if password != repassword:
        return jsonify({"message":"your password needs to match"}),400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists please choose a different username"}), 400
    
    passwordError=validatePassword(password)

    if passwordError:
        return jsonify({"message":passwordError}),400

    

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username,password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@app.route("/protected", methods=["GET"])
@limiter.limit("20 per minute") #Rate limiter for protected route
@jwt_required()
def protected():
    user_id= get_jwt_identity()
    return jsonify({"message":f"Access granted for user {user_id}"})

@app.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    data=request.get_json()
    user_id=get_jwt_identity()

    if not data or "content" not in data:
        return jsonify({"message": "Invalid input"}),400

    note=Note(content=data["content"],user_id=user_id)

    

    db.session.add(note)
    db.session.commit()

    return jsonify ({"message":"Note created successfully"})

@app.route("/notes",methods=["GET"])
@jwt_required()
def get_notes():
    user_id=get_jwt_identity()
    notes=Note.query.filter_by(user_id=user_id).all()

    
    return jsonify([{"id": n.id, "content": n.content} for n in notes])


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)