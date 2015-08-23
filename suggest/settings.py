__author__ = 'robdefeo'
def get_env_setting(env_variable_name, default):
    if env_variable_name in os.environ:
        return os.environ[env_variable_name]
    else:
        return default


import os

PORT = int(get_env_setting("SUGGEST_PORT", 14999))

CONTENT_CACHE_SIZE = int(get_env_setting("SUGGEST_CONTENT_CACHE_SIZE", 256))
CONTENT_URL = get_env_setting("SUGGEST_CONTENT_GENERATED_URL", "http://content.jemboo.com/generated/")

MONGODB_HOST = get_env_setting("SUGGEST_MONGODB_HOST", "localhost")
MONGODB_PORT = int(get_env_setting("SUGGEST_MONGODB_PORT", 27017))
MONGODB_DB = get_env_setting("SUGGEST_MONGODB_DB", "suggest")
MONGODB_USER = get_env_setting("SUGGEST_MONGODB_USER", "suggest")
MONGODB_PASSWORD = get_env_setting("SUGGEST_MONGODB_PASSWORD", "jemboo")

DATA_CACHE_SIZE_SUGGESTION = 1024
