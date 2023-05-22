import time

import jwt
from decouple import config

JWT_SECRET =  str(config("secret"))
JWT_ALGORITHM = str(config("algorithm"))

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_id: str):
    payload = {
        "user_id": user_id,
        "expires": time.time() + 60 * 60 * 60
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
