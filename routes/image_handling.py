from flask import Blueprint, request, send_file, jsonify
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request, decode_token
import cv2
import numpy as np
import io
from functools import wraps

image_blueprint = Blueprint('image', __name__, url_prefix='/image')


def guest_limit_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request(optional=True)
        guest_token = request.cookies.get('guest_token')
        if guest_token:
            decoded = decode_token(guest_token)
            if decoded.get("is_guest"):
                tries_left = decoded.get("tries_left", 0)
                if tries_left <= 0:
                    return jsonify({"error": "Guest tries exceeded. Please log in."}), 401
        return fn(*args, **kwargs)
    return wrapper

@image_blueprint.route('/lsb_stego/encode', methods=['POST'])
@guest_limit_required
def lsb_encode_route():
    user_img = request.files['image']
    user_data = request.form['text']
    user_key = request.form['key']

    guest_token = request.cookies.get('guest_token')
    if guest_token:
        from routes.guest import decrement_tries
        new_token = decrement_tries(guest_token)
    else:
        new_token = None

    from routes.aes import aes_encrypt
    encrypted_data = aes_encrypt(user_data, user_key)

    if not user_img or len(user_data) == 0 or len(user_key) == 0:
        return {'error': 'No image or Text or key provided'}, 400

    file_bytes = np.frombuffer(user_img.read(), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return {'error': 'Failed to read image file'}, 500

    from routes.lsb_steganography import lsb_encode
    encoded_img = lsb_encode(img, encrypted_data)

    _, buffer = cv2.imencode('.png', encoded_img)
    img_bytes = io.BytesIO(buffer)

    response = send_file(img_bytes, mimetype='image/png', as_attachment=True, download_name="encoded_image.png")

    if new_token:
        response.set_cookie('guest_token', new_token, max_age=1800)

    return response


@image_blueprint.route('/lsb_stego/decode', methods=['POST'])
@jwt_required(optional=True)
def lsb_decode_route():
    user_img = request.files['image']
    user_key = request.form['key']
    if not user_img or user_img.filename == '' or len(user_key) == 0 or not user_key:
        return {'error': 'No image or key provided'}, 400

    file_bytes = np.frombuffer(user_img.read(), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return {'error': 'Failed to read image file'}, 500

    from routes.lsb_steganography import lsb_decode
    from routes.aes import aes_decrypt
    decrypted_data = aes_decrypt(lsb_decode(img), user_key)

    return {'data': decrypted_data}, 200