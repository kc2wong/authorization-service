from openapi_server.config.logging import logger
from openapi_server.services import key_service

from generated.openapi_server.models import SystemSetting, PublicKey

def get_system_setting():
    public_keys = [PublicKey(host=k, key_string=v) for k,v in key_service.get_all_public_key_str().items()]
    return SystemSetting(public_key=public_keys)
