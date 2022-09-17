from openapi_server.config.logging import logger
from openapi_server.services import role_service

def find_role(application_code=None, role_code=None):
    logger.info("find_role() starts with application_code = {0}, role_code = {1}".format(application_code, role_code))

    result = role_service.find_role(application_code, role_code)

    logger.info("find_role() finishes, number of records found = {0}".format(len(result)))

    return result, 200

