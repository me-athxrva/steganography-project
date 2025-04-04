import os

from flask import Blueprint, request, send_file
from flask_jwt_extended import jwt_required
import cv2
import numpy as np
import io

image_blueprint = Blueprint('image', __name__, url_prefix='/image')


@image_blueprint.route('/lsb_stego/encode', methods=['POST'])
@jwt_required()
def lsb_encode_route():
    user_img = request.files['image']
    user_data = request.form['text']
    from routes.aes import aes_encrypt
    encrypted_data = aes_encrypt(user_data, os.getenv('AES_KEY'))

    if not user_img or len(user_data) == 0:
        return {'error': 'No image or Text provided'}, 400

    file_bytes = np.frombuffer(user_img.read(), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return {'error': 'Failed to read image file'}, 500

    from routes.lsb_steganography import lsb_encode
    encoded_img = lsb_encode(img, encrypted_data)

    _, buffer = cv2.imencode('.png', encoded_img)
    img_bytes = io.BytesIO(buffer)

    return send_file(img_bytes, mimetype='image/png', as_attachment=True, download_name="encoded_image.png")


@image_blueprint.route('/lsb_stego/decode', methods=['POST'])
@jwt_required()
def lsb_decode_route():
    user_img = request.files['image']
    if not user_img or user_img.filename == '':
        return {'error': 'No image provided'}, 400

    file_bytes = np.frombuffer(user_img.read(), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return {'error': 'Failed to read image file'}, 500

    from routes.lsb_steganography import lsb_decode
    from routes.aes import aes_decrypt
    decrypted_data = aes_decrypt(lsb_decode(img), os.getenv('AES_KEY'))

    return {'data': decrypted_data}, 200