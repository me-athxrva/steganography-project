import os
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, get_jwt_identity, \
    unset_jwt_cookies
from flask import Blueprint, render_template, request, session, jsonify, make_response, redirect
from routes.db import mongo
from datetime import timedelta
from routes.guest import  create_guest_token

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/', methods=['GET'])
@jwt_required(optional=True)
def home():
    print('user entered')
    user = get_jwt_identity()
    guest_token = request.cookies.get('guest_token')
    fingerprint = request.cookies.get('fingerprint')
    logged_token = request.cookies.get('access_token_cookie')
    if logged_token:
        return render_template('main.html')
    if not user and not guest_token:
        resp = make_response(render_template('main.html'))
        guest_token = create_guest_token()
        resp.set_cookie('guest_token', guest_token, max_age=1800, httponly=True)
        return resp
    return render_template('main.html')

@user_blueprint.route('/decode', methods=['GET'])
@jwt_required(optional=True)
def decode():
    return render_template('decode.html')

@user_blueprint.route('/encode', methods=['GET'])
@jwt_required(optional=True)
def encode():
    return render_template('encode.html')

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
    response.delete_cookie('guest_token')
    set_access_cookies(response, access_token)
    return response


@user_blueprint.route('/auth/logout', methods=['GET'])
@jwt_required(optional=True)
def auth_logout():
    session.pop('email', None)
    response = make_response(redirect('/'))
    unset_jwt_cookies(response)
    for cookie in request.cookies:
        response.set_cookie(cookie, '', expires=0)
    return response