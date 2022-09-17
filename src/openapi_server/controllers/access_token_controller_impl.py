from generated.openapi_server.models import CreateAccessToken200Response, ErrorResponse

from openapi_server.config.logging import logger
from openapi_server.models.error import UserNotFoundException
from openapi_server.services import user_service, profile_service, role_service, key_service

from openapi_server.util import datetime_util

def create_access_token(user_id:str, site_code:str=None):  # noqa: E501
    user = user_service.get_user_by_id(user_id)
    if user is None:
        return UserNotFoundException(user_id=user_id), 404
    logger.info("profiles of user [{0}] = {1}".format(user_id, user.profile_code))

    all_role_codes = set()
    profiles = filter(lambda p: site_code is None or site_code in p.site_code, profile_service.find_profile(profile_code=user.profile_code))
    for p in profiles:
        all_role_codes.update(p.role_code)
    logger.info("roles of user [{0}] = {1}".format(user_id, all_role_codes))

    all_end_point_id = set()
    roles = role_service.find_role(role_code=list(all_role_codes))
    for r in roles:
        all_end_point_id.update(r.end_point_id)
    logger.info("end_point_ids of user [{0}] = {1}".format(user_id, all_end_point_id))

    payload = {
        "sub": user_id, 
        "firstName": user.first_name, 
        "lastName": user.last_name, 
        "email": user.email, 
        "role": list(all_role_codes), 
        "endPointId": list(all_end_point_id)
    }

    access_token = key_service.encode_jwt(payload)
    return CreateAccessToken200Response(access_token="Bearer {0}".format(access_token)), 200
