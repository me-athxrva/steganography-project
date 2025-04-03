from flask import Blueprint, request
from Cryptodome.Cipher import AES
import hashlib
import base64

encryption_blueprint = Blueprint('encryption', __name__)

@encryption_blueprint.route('/aes/encrypt', methods=['POST'])
def aes_encrypt():
    data = request.get_json() # fetch data from request

    if not data.get('message') or not data.get('key'):
        return {"error": "Missing parameters"}, 400

    hashed_key = hashlib.sha256(data.get('key').encode('utf-8')).digest()
    cipher = AES.new(hashed_key, AES.MODE_GCM)
    nonce = cipher.nonce
    cipher_text, tag = cipher.encrypt_and_digest(data.get('message').encode('ascii'))

    encrypted_data = nonce + tag + cipher_text

    return {'encrypted': base64.b64encode(encrypted_data).decode()}, 200

@encryption_blueprint.route('/aes/decrypt', methods=['GET'])
def aes_decrypt():
    data = request.get_json() # fetch data from request

    if not data.get('encrypted') or not data.get('key'):
        return {"error": "Missing parameters"}, 400

    hashed_key = hashlib.sha256(data.get('key').encode('utf-8')).digest()

    encrypted_data_b64 = base64.b64decode(data.get('encrypted'))
    nonce = encrypted_data_b64[:16]
    tag = encrypted_data_b64[16:32]
    ciphertext = encrypted_data_b64[32:]

    cipher = AES.new(hashed_key, AES.MODE_GCM, nonce=nonce)

    try:
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return {'Decrypted': decrypted_data.decode('ascii')}, 200
    except ValueError:
        return {'Decryption failed': 'Invalid cipher text, nonce, tag or key'}, 401