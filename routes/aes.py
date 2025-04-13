from Cryptodome.Cipher import AES
import hashlib
import base64

def aes_encrypt(message, key):
    hashed_key = hashlib.sha256(key.encode('utf-8')).digest()
    cipher = AES.new(hashed_key, AES.MODE_GCM)
    nonce = cipher.nonce
    cipher_text, tag = cipher.encrypt_and_digest(message.encode('ascii'))

    encrypted_data = nonce + tag + cipher_text

    return base64.b64encode(encrypted_data).decode()

def aes_decrypt(encrypted_data, key):
    hashed_key = hashlib.sha256(key.encode('utf-8')).digest()

    encrypted_data_b64 = base64.b64decode(encrypted_data)
    nonce = encrypted_data_b64[:16]
    tag = encrypted_data_b64[16:32]
    ciphertext = encrypted_data_b64[32:]

    cipher = AES.new(hashed_key, AES.MODE_GCM, nonce=nonce)

    try:
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data.decode('ascii')
    except ValueError:
        return 'Decryption failed!'

def toBinary(text):
    text_binary = ''.join(format(ord(char), '08b') for char in text)
    return text_binary

def toAscii(binary):
    ascii_text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return ascii_text