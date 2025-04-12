from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta
import uuid

def create_guest_token():
    guest_id = "guest_" + str(uuid.uuid4())[:8]
    additional_claims = {
        "is_guest": True,
        "tries_left": 5
    }
    token = create_access_token(
        identity=guest_id,
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=8)
    )
    return token

def decrement_tries(token: str):
    try:
        decoded = decode_token(token)
        if not decoded.get("is_guest"):
            raise ValueError("Not a guest token.")

        tries_left = decoded.get("tries_left", 0)

        if tries_left > 0:
            decoded["tries_left"] = tries_left - 1
        else:
            return token

        new_token = create_access_token(
            identity=decoded["sub"],
            additional_claims=decoded,
            expires_delta=timedelta(minutes=30)
        )

        return new_token

    except Exception as e:
        return str(e)
