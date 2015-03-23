__author__ = 'robdefeo'
def get_env_setting(env_variable_name, default):
    if env_variable_name in os.environ:
        return os.environ[env_variable_name]
    else:
        return default


import os

PORT = int(get_env_setting("SUGGEST_PORT", 14999))
CONTEXT_URL = get_env_setting("SUGGEST_CONTEXT_URL", "http://content.jemboo.com/suggest/")