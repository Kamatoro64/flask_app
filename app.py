from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask App
app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Create Database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return {"message": "Welcome to the User API"}

# Create (Add a User)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# Read (Get All Users)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": user.id, "name": user.name, "email": user.email} for user in users
    ])

# Read (Get a Specific User)
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({"id": user.id, "name": user.name, "email": user.email})

# Update (Modify a User)
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get_or_404(id)
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

# Delete (Remove a User)
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
