import os
import re
import json

_re_name = re.compile(r'[a-z][a-z0-9_]*')
_config = {}


def get_config(config_name):
    global _config
    if config_name in _config:
        return _config[config_name]

    _config[config_name] = _get_config_from_env(config_name)
    return _config[config_name]


def _get_config_from_env(config_name):
    if not _re_name.match(config_name):
        raise ImportError('Config name Error: {}!'.format(config_name))
    config = dict()
    config_name = config_name.upper() + '_'
    for raw_name, raw_value in os.environ.items():
        if raw_name.startswith(config_name) and raw_name != config_name:
            config[raw_name[len(config_name):]] = json.loads(raw_value)
    return config
