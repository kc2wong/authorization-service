from dotenv import dotenv_values

def get_environment(env_name:str, default_value:str=None) -> str:
    config = dotenv_values(".env")
    return config.get(env_name) or default_value