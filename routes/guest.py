from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta
import uuid
from flask import request
from routes.db import mongo
import datetime

def create_guest_token():
    fingerprint = request.cookies.get('fingerprint')
    guest_id = "guest_" + str(uuid.uuid4())[:8]
    additional_claims = {
        "is_guest": True,
        "tries_left": 5
    }
    token = create_access_token(
        identity=guest_id,
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=8),
    )

    exists = mongo.steganographyProject.guest_id.find_one({"fingerprint": fingerprint},{"guest_token": 1})
    if exists:
        return exists["guest_token"]

    mongo.steganographyProject.guest_id.insert_one({
        "guest_id": guest_id,
        "fingerprint": fingerprint,
        "guest_token": token,
        "tries_left": 5,
        "created_at": datetime.datetime.now(datetime.UTC),
        "expires_at": datetime.datetime.now(datetime.UTC) + timedelta(hours=8)
    })
    return token

def decrement_tries(token: str):
    fingerprint = request.cookies.get('fingerprint')
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


        if fingerprint:
            user = mongo.steganographyProject.guest_id.find_one(
                {"fingerprint": fingerprint},
                {"tries_left": 1}
            )
            if user["tries_left"] > 0:
                mongo.steganographyProject.guest_id.update_one(
                    {"fingerprint": fingerprint},
                    {"$set": {"tries_left": user["tries_left"]-1, "guest_token": new_token}}
                )

        return new_token

    except Exception as e:
        return str(e)
