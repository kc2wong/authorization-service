from typing import List

from generated.openapi_server.models.end_point import EndPoint

from openapi_server.config.mongdb import get_database
from openapi_server.config.logging import logger
from openapi_server.util.dictionary_util import camelize_keys

def find_end_point(application_code:str=None, end_point_id:str=None) -> List[EndPoint]:
    database = get_database()

    filter = {}
    if end_point_id is not None:
        filter["end_point_id"] = {"$in": end_point_id}
    if application_code is not None:
        filter["application_code"] = application_code
    logger.debug("find_end_point(), filter = {0}".format(filter))

    documents = database["end-point"].find(filter)
    result = list(map(lambda e: EndPoint.from_dict(camelize_keys(e)), documents))
    
    return list(result)
