import platform
import jwt

from typing import Dict
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from datetime import timedelta

from openapi_server.config.logging import logger
from openapi_server.config.environment import get_environment
from openapi_server.config.mongdb import get_database
from openapi_server.util import datetime_util

def get_private_key_str() -> str:

    database = get_database()

    filter = {"host": get_environment("NODE_NAME", platform.node())}

    key_pair = database["key-pair"].find_one(filter)
    if key_pair is not None:
        return key_pair["private"]
    else:
        return None


def get_private_key() -> rsa.RSAPrivateKey:
    private_key_str = get_private_key_str()
    logger.info("private_key_str = \n{}".format(private_key_str))

    if private_key_str is not None:
        return load_pem_private_key(bytes(private_key_str, "utf-8"), None, default_backend())
    else:
        return None


def get_all_public_key_str() -> Dict[str, str]:
    database = get_database()
    documents = list(database["key-pair"].find({}))
    return { doc["host"] : doc["public"] for doc in documents }


def get_all_public_key() -> Dict[str, rsa.RSAPublicKey]:
    documents = get_all_public_key_str()
    return { doc[0] : load_pem_public_key(bytes(doc[1], "utf-8"), default_backend()) for doc in documents.items() }


def encode_jwt(payload:dict) -> str:
    current_datetime = datetime_util.current_datetime_utc()
    system_payload = {
        "iss": get_environment("NODE_NAME", platform.node()),
        "iat": current_datetime,
        "exp": current_datetime + timedelta(hours=12),
    }

    return jwt.encode(payload | system_payload, get_private_key_str(), algorithm="RS256")


def decode_jwt(bearer_token:str, verify_signature:bool=True) -> dict:
    token = bearer_token
    if token.upper().startswith("BEARER "):        
        token = bearer_token[7:]
    logger.debug("token = {0}".format(token))   

    payload = jwt.decode(token, options={"verify_signature": False})

    if verify_signature:        
        issuer = payload.get("iss") or get_environment("NODE_NAME", platform.node())
        logger.info("issuer = {0}".format(issuer))
        public_key = get_all_public_key_str().get(issuer)
        return jwt.decode(token, public_key, algorithms=["RS256"])
    else:
        return payload
