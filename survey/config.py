import os

import yaml


class YamlConfiguration(object):
    """ Reads yaml based configuration files. """

    def __init__(self, yaml_content):
        self.config = yaml.load(yaml_content)

    def property(self, key):
        value = YamlConfiguration.from_environment(key)
        if value is not None:
            return value
        if '.' in key:
            key_chain = key.split('.')
            return self._nested_property(key_chain)
        return self.config.get(key)

    @staticmethod
    def from_environment(key):
        env_key = key.replace('.', '_')
        return os.environ.get(env_key, None)

    def _nested_property(self, key_chain):
        config = self.config
        for key in key_chain:
            if isinstance(config, dict):
                config = config.get(key)
        return config

    @classmethod
    def create_from_file(cls, file):
        if not os.path.isfile(file):
            raise Exception('Not a valid file!')
        with open(file) as file:
            content = file.read()
        return cls(content)
