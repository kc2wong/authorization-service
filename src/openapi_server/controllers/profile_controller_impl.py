from flask import request as http_request

from generated.openapi_server.models import UpdateProfileRequest, ErrorResponse

from openapi_server.config.logging import logger
from openapi_server.models.error import error_code_unauthorized
from openapi_server.models.error import UnauthorizedException, ProfileAlreadyExistsException, ProfileNotFoundException, RoleNotFoundException, VersionNotMatchException
from openapi_server.services import profile_service, role_service, key_service

def create_profile(update_profile_request: dict):
    logger.info("create_profile() starts with update_profile_request = {0}".format(
        update_profile_request))

    # Check if profile already exist
    request = UpdateProfileRequest.from_dict(update_profile_request)
    result = profile_service.find_profile(
        request.application_code, [request.profile_code])
    logger.info("number of existing profiles = {0}".format(len(result)))
    if len(result) != 0:
        return ProfileAlreadyExistsException(
            request.application_code, request.profile_code), 400

    # Check if any input role is invalid
    error = _validate_roles(request)
    if error is not None:
        return error, 400

    current_user_id = _get_current_user_id()    
    result = profile_service.create_profile(update_profile_request=request, current_user_id=current_user_id)
    logger.info(
        "create_profile() finishes, result = {0}".format(result))
    return result, 201


def find_profile(application_code, profile_code):
    logger.info("find_profile() starts with application_code = {0}, profile_code = {1}".format(
        application_code, profile_code))

    result = profile_service.find_profile(application_code, profile_code)

    logger.info(
        "find_profile() finishes, number of records found = {0}".format(len(result)))

    return result, 200


def update_profile(profile_code, update_profile_request: dict):
    logger.info("update_profile() starts with update_profile_request = {0}".format(
        update_profile_request))

    # Check if profile already exist
    request = UpdateProfileRequest.from_dict(update_profile_request)
    result = profile_service.find_profile(profile_code=[profile_code])
    logger.info("number of existing profiles = {0}".format(len(result)))
    if len(result) != 1:
        return ProfileNotFoundException([request.profile_code]), 400

    # Check if any input role is invalid
    error = _validate_roles(request)
    if error is not None:
        return error, 400

    try:
        current_user_id = _get_current_user_id()    
        result = profile_service.update_profile(profile=result[0], update_profile_request=request, current_user_id=current_user_id)
    except VersionNotMatchException as ex:
        return ErrorResponse(code=ex.error_code, param=ex.param, message=ex.message), 400

    logger.info(
        "update_profile() finishes, result = {0}".format(result))
    return result, 200


def _get_current_user_id() -> str:
    authorization = http_request.headers.get('Authorization')
    return key_service.decode_jwt(bearer_token=authorization, verify_signature=False).get('sub')


def _validate_roles(request:UpdateProfileRequest):
    found_roles = set(map(lambda e: e.role_code, role_service.find_role(
        application_code=request.application_code, role_code=request.role_code)))
    roles_not_found = set(request.role_code).difference(found_roles)
    if len(roles_not_found) != 0:
        return RoleNotFoundException(roles_not_found)
    else:
        return None
