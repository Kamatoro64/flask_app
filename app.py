from flask import Flask
from flask import request

# This creates an instance of the Flask class
app = Flask(__name__)

# This is a decorator in Python. In Flask, decorators like @app.route() define the routes (URLs) that the application will respond to.
# Flask routes are tied to Python functions, which handle the logic of each URL

# Route 1 - Home
@app.route('/')
def home():
    return {"message": "Welcome to my first API!"} # This sends a JSON response to the client. Flask automatically serializes the Python dictionary into JSON when returning it.

# Route 2 - Endpoint with dynamic input
@app.route('/hello/<name>')
def hello(name):
    return {"message": f"Hello, {name}!"}

# Route 3 Handle User Input via Query Parameters: http://127.0.0.1:5000/add?a=5&b=3
@app.route('/add')
def add():
    from flask import request
    a = request.args.get('a', default=0, type=int)
    b = request.args.get('b', default=0, type=int)
    return {"result": a + b}

# Route 4 Handle User Input via JSON Input (POST Request): 
# Curl command to send post request: curl -H 'Content-Type: application/json' -d '{ "a":3,"b":4 }' -X POST http://127.0.0.1:5000/multiply
@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.json
    a = data.get('a', 1)
    b = data.get('b', 1)
    return {"result": a * b}

if __name__ == "__main__":
    app.run(debug=True)
