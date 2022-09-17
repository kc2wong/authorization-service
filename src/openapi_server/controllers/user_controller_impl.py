from flask import request as http_request

from openapi_server.models.error import UserNotFoundException

from generated.openapi_server.models import UpdateUserRequest, ErrorResponse

from openapi_server.models.error import error_code_unauthorized
from openapi_server.models.error import UnauthorizedException, UserAlreadyExistsException, UserNotFoundException, ProfileNotFoundException, VersionNotMatchException
from openapi_server.services import user_service, profile_service, key_service

from openapi_server.config.logging import logger

def create_user(update_user_request: dict):  # noqa: E501
    logger.info("create_user() starts with update_user_request = {0}".format(
        update_user_request))

    try:        
        current_user_id = _get_current_user_id()
    except UnauthorizedException as ex:
        return ErrorResponse(code=error_code_unauthorized, param=ex.param, message=ex.message), 401

    # Check if profile already exist
    request = UpdateUserRequest.from_dict(update_user_request)
    result = user_service.get_user_by_id(request.user_id)
    if result is not None:
        return UserAlreadyExistsException(request.user_id), 400

    # Check if any input profile is invalid
    error = _validate_profiles(request)
    if error is not None:
        return error, 400

    result = user_service.create_user(update_user_request=request, current_user_id=current_user_id)
    logger.info(
        "create_user() finishes, result = {0}".format(result))
    return result, 201


def update_user(user_id, update_user_request: dict):
    logger.info("update_user() starts with update_user_request = {0}".format(
        update_user_request))

    # Check if user already exist
    request = UpdateUserRequest.from_dict(update_user_request)
    result = user_service.get_user_by_id(user_id)
    if result is None:
        return UserNotFoundException(request.user_id), 400

    # Check if any input role is invalid
    error = _validate_profiles(request)
    if error is not None:
        return error, 400

    try:
        current_user_id = _get_current_user_id()
        result = user_service.update_user(user=result, update_user_request=request, current_user_id=current_user_id)
    except VersionNotMatchException as ex:
        return ErrorResponse(code=ex.error_code, param=ex.param, message=ex.message), 400

    logger.info(
        "update_user() finishes, result = {0}".format(result))
    return result, 200


def get_user_by_id(user_id):  # noqa: E501
    logger.info('/getUserById starts, user_id = {0}'.format(user_id))
    user = user_service.get_user_by_id(user_id)
    if user is None:
        return UserNotFoundException(user_id=user_id), 404
    else:
        return user, 200


def _get_current_user_id() -> str:
    authorization = http_request.headers.get('Authorization')
    return key_service.decode_jwt(bearer_token=authorization, verify_signature=False).get('sub')


def _validate_profiles(request:UpdateUserRequest):
    found_profiles = set(map(lambda e: e.profile_code, profile_service.find_profile(
        profile_code=request.profile_code)))
    profiles_not_found = set(request.profile_code).difference(found_profiles)
    if len(profiles_not_found) != 0:
        return ProfileNotFoundException(profile_codes=profiles_not_found)
    else:
        return None