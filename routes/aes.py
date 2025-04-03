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
    cipher = AES.new(hashed_key, AES.MODE_EAX)
    nonce = cipher.nonce
    cipher_text, tag = cipher.encrypt_and_digest(data.get('message').encode('ascii'))

    return {'ciphertext': base64.b64encode(cipher_text).decode(),
            'nonce': base64.b64encode(nonce).decode(),
            'tag': base64.b64encode(tag).decode()
    }, 200

@encryption_blueprint.route('/aes/decrypt', methods=['GET'])
def aes_decrypt():
    data = request.get_json() # fetch data from request

    if not data.get('ciphertext') or not data.get('nonce') or not data.get('tag') or not data.get('key'):
        return {"error": "Missing parameters"}, 400

    hashed_key = hashlib.sha256(data.get('key').encode('utf-8')).digest()
    cipher_text_b64 = base64.b64decode(data.get('ciphertext'))
    nonce_b64 = base64.b64decode(data.get('nonce'))
    tag_b64 = base64.b64decode(data.get('tag'))

    cipher = AES.new(hashed_key, AES.MODE_EAX, nonce=nonce_b64)

    try:
        decrypted_data = cipher.decrypt_and_verify(cipher_text_b64, tag_b64)
        return {'Decrypted': decrypted_data.decode('ascii')}, 200
    except ValueError:
        return {'Decryption failed': 'Invalid cipher text, nonce, tag or key'}, 500