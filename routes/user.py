import os
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, get_jwt_identity, \
    unset_jwt_cookies
from flask import Blueprint, render_template, request, session, jsonify
from routes.db import mongo
from datetime import timedelta

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/', methods=['GET'])
@jwt_required(optional=True)
def home():
    user = get_jwt_identity()
    if not user:
        return {'error': 'You are unauthorized bro!'}, 401
    return render_template('home.html', user=user)

@user_blueprint.route('/auth/register', methods=['POST'])
def auth_register():
    auth_data = request.get_json()

    if not auth_data or auth_data['email'] == '' or auth_data['password'] == '':
        return {'error': 'Missing username or password'}, 400

    if mongo.steganographyProject.users.find_one({"email": auth_data['email']}):
        return {'error': 'User already exists'}, 409

    from routes.aes import aes_encrypt
    email = auth_data['email']
    encrypted_password = aes_encrypt(auth_data['password'], os.getenv('AES_KEY'))
    token = create_access_token(identity=email, expires_delta=timedelta(hours=1))

    mongo.steganographyProject.users.insert_one({
        "email": email,
        "password": encrypted_password,
        "jwt": token
    })

    session['email'] = email

    response = jsonify({"message": "Registration successful"})
    set_access_cookies(response, token)
    return response


@user_blueprint.route('/auth/login', methods=['POST'])
def auth_login():
    auth_data = request.get_json()
    if not auth_data or auth_data['email'] == '' or auth_data['password'] == '':
        return {'error': 'Missing username or password'}, 400

    user = mongo.steganographyProject.users.find_one({"email": auth_data['email']})

    if not user:
        return {'error': 'User not found'}, 404

    from routes.aes import aes_decrypt
    user_password = aes_decrypt(user['password'], os.getenv('AES_KEY'))

    if user_password != auth_data['password']:
        return {'error': 'Incorrect password'}, 401

    session['email'] = auth_data['email']

    access_token = create_access_token(identity=auth_data['email'], expires_delta=timedelta(hours=1))

    mongo.steganographyProject.users.update_one(
        {"email": auth_data['email']},
        {"$set": {"jwt": access_token}}
    )

    response = jsonify({"message": "Login successful"})
    set_access_cookies(response, access_token)
    return response


@user_blueprint.route('/auth/logout', methods=['POST'])
@jwt_required()
def auth_logout():
    session.pop('email', None)
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response