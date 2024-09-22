from flask import Flask
from flask_cors import CORS
from Routes import init_routes
from config import init_connect

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, 
     headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     supports_credentials=True)

init_routes(app=app)

app.run(debug=True, port=5840)