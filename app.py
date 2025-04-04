from flask import Flask

from routes.image_handling import image_blueprint
from routes.user import user_blueprint
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv() # loading environment variables from.env file

app = Flask(__name__)

# Session configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False # False for development mode only
app.config['JWT_COOKIE_CSRF_PROTECT'] = False # False for development mode only
JWTManager(app)

# route registration
app.register_blueprint(user_blueprint, url_prefix='/')
app.register_blueprint(image_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run()
