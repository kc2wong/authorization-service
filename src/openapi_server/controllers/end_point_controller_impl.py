import re
from openapi_server.config.logging import logger
from openapi_server.services import end_point_service 

def find_end_point(application_code=None, end_point_id=None):
    logger.info("find_end_point() starts with application_code = {0}, end_point_id = {1}".format(application_code, end_point_id))
    
    result = end_point_service.find_end_point(application_code, end_point_id)

    logger.info("find_end_point() finishes, number of records found = {0}".format(len(result)))

    return result, 200