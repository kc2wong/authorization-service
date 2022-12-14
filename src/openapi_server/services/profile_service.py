from typing import List
from generated.openapi_server.models.profile import UpdateProfileRequest, Profile
from openapi_server.config.mongdb import get_database
from openapi_server.util.datetime_util import current_datetime_utc
from openapi_server.util.dictionary_util import camelize_keys, remove_keys

from openapi_server.models.error import VersionNotMatchException
from openapi_server.config.logging import logger

def find_profile(application_code:str=None, profile_code:List[str]=None) -> List[Profile]:
    database = get_database()

    filter = {}
    if application_code is not None:
        filter["application_code"] = application_code
    if profile_code is not None:
        filter["profile_code"] = {"$in": profile_code}
    logger.debug("find_profile(), filter = {0}".format(filter))

    documents = database["profile"].find(filter)
    result = list(map(lambda e: Profile.from_dict(camelize_keys(e)), documents))
    return list(result)


def create_profile(update_profile_request: UpdateProfileRequest, current_user_id:str=None) -> Profile:
    current_datetime = current_datetime_utc()
    dict = camelize_keys(update_profile_request.to_dict())

    profile = Profile.from_dict(dict)
    profile.version = 1
    profile.created_by = current_user_id or "system"
    profile.created_date_time = current_datetime
    profile.updated_by = current_user_id or "system"
    profile.updated_date_time = current_datetime

    profile_dict = profile.to_dict();
    # Convert datetime to string when writing to database
    profile_dict["created_date_time"] = profile.created_date_time.isoformat() 
    profile_dict["updated_date_time"] = profile.updated_date_time.isoformat() 
    logger.debug("create_profile(), dict to insert = {0}".format(profile_dict))

    database = get_database()
    database["profile"].insert_one(profile_dict)
    return profile


def update_profile(profile: Profile, update_profile_request: UpdateProfileRequest, current_user_id:str=None) -> Profile:
    current_datetime = current_datetime_utc()

    if update_profile_request.version != profile.version: 
        raise VersionNotMatchException(
            update_profile_request.version, profile.version)

    current_version = profile.version

    # Merge existing profile with input request
    # to_dict() method generated by openapi generator does not format datetime to ISO string, need to exclude the datetime field
    profile_dict = remove_keys(profile.to_dict(), ["created_date_time", "updated_date_time"]) | remove_keys(update_profile_request.to_dict(), ["profile_code"])
    new_profile = Profile.from_dict(camelize_keys(profile_dict))
    new_profile.created_date_time = profile.created_date_time
    new_profile.version = profile.version + 1
    new_profile.updated_by = current_user_id or "system"
    new_profile.updated_date_time = current_datetime

    query = { "profile_code": profile.profile_code, "version": current_version }
    new_values = remove_keys(new_profile.to_dict(), ["created_by", "created_date_time"])
    # Convert datetime to string when writing to database
    new_values["updated_date_time"] = new_profile.updated_date_time.isoformat() 
    logger.info("update_profile(), dict to update = {0}".format(new_values))

    database = get_database()
    profile_collection = database["profile"]
    num_row_updated = profile_collection.update_one(query, { "$set": new_values }).matched_count
    logger.info("update_profile(), numOfRowUpdated = {0}".format(num_row_updated))
    if num_row_updated != 1:
        # For simplicity, assume the version in database is being incremented by 1
        raise VersionNotMatchException(
            update_profile_request.version, update_profile_request.version + 1)

    return new_profile