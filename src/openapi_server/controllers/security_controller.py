from openapi_server.services import key_service

def decode_jwt(bearerToken: str) -> dict:
    try:
        return key_service.decode_jwt(bearer_token=bearerToken)
    except Exception:
        return None
