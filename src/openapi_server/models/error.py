from typing import List
from generated.openapi_server.models.error_response import ErrorResponse

error_code_unauthorized = 'UNAUTHORIZED'
error_code_profile_already_exists = 'PROFILE_ALREADY_EXISTS'
error_code_profile_not_found = 'PROFILE_NOT_FOUND'
error_code_role_not_found = 'ROLE_NOT_FOUND'
error_code_user_not_found = 'USER_NOT_FOUND'
error_code_user_already_exists = 'USER_ALREADY_EXISTS'
error_code_version_not_match = 'VERSION_NOT_MATCH'

class ProfileAlreadyExistsException(ErrorResponse):
    """Exception raised for when profile with same code already exists

    Attributes:
        application_code -- applicationCode of input profile
        profile_code -- profileCode of input profile
    """

    def __init__(self, application_code, profile_code):
        super().__init__(error_code_profile_already_exists, [application_code, profile_code], 'Profile [{0}] already exists in application [{1}]'.format(profile_code, application_code))

    def to_dict(self):
        return self.__dict__


class ProfileNotFoundException(ErrorResponse):
    """Exception raised for when profile with input code is not found

    Attributes:
        profile_code -- profileCode of input profile
    """

    def __init__(self, profile_codes:List[str]):
        super().__init__(error_code_profile_not_found, [",".join(profile_codes)], 'Profile [{0}] is not found'.format(profile_codes))

    def to_dict(self):
        return self.__dict__


class RoleNotFoundException(ErrorResponse):
    """Exception raised for when user is not found.

    Attributes:
        role_codes -- list of roles that are not found
    """

    def __init__(self, role_codes:List[str]):
        super().__init__(error_code_role_not_found, [",".join(role_codes)], 'User [{0}] not found'.format(",".join(role_codes)))

    def to_dict(self):
        return self.__dict__


class UserAlreadyExistsException(ErrorResponse):
    """Exception raised for when user with same id already exists

    Attributes:
        user_id -- profileCode of input profile
    """

    def __init__(self, user_id):
        super().__init__(error_code_user_already_exists, [user_id], 'User [{0}] already exists'.format(user_id))

    def to_dict(self):
        return self.__dict__


class UserNotFoundException(ErrorResponse):
    """Exception raised for when user is not found.

    Attributes:
        user_id -- input userId which caused the error
    """

    def __init__(self, user_id):
        super().__init__(error_code_user_not_found, [user_id], 'User [{0}] not found'.format(user_id))

    def to_dict(self):
        return self.__dict__


class VersionNotMatchException(Exception):
    """Exception raised for when version of record to update is different from latest version

    Attributes:
        input_version -- version of input record
        expected_version -- latest version of the record in database
    """
    def __init__(self, input_version, expected_version):
        super().__init__()
        self.error_code = error_code_version_not_match
        self.param = [input_version, expected_version]
        self.message = 'Version not match, input version = [{0}], expected version = [{1}]'.format(input_version, expected_version)


class UnauthorizedException(Exception):
    """Exception raised for when input request does not contain an valid authorization header

    """

    def __init__(self):
        super().__init__()
        self.param = []
        self.message = 'No valid Authorization header is provided'

    def to_dict(self):
        return self.__dict__
