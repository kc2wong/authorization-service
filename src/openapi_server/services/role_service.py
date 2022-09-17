from typing import List
from generated.openapi_server.models.role import Role

from openapi_server.config.mongdb import get_database
from openapi_server.config.logging import logger
from openapi_server.util.dictionary_util import camelize_keys

def find_role(application_code:str=None, role_code:List[str]=None):
    database = get_database()

    filter = {}
    if application_code is not None:
        filter["application_code"] = application_code
    if role_code is not None:
        filter["role_code"] = {"$in": role_code}
    logger.debug("find_role(), filter = {0}".format(filter))

    documents = database["role"].find(filter)
    result = list(map(lambda e: Role.from_dict(camelize_keys(e)), documents))

    return list(result)
