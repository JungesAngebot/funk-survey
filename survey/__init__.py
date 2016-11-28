import os

from flask.ext.login import LoginManager

from survey.config import YamlConfiguration

APP_ROOT = os.path.dirname(os.path.abspath(__file__)).replace(os.sep + 'survey', '')

config = YamlConfiguration.create_from_file('%s/config/config.yml' % APP_ROOT)

login_manager = LoginManager()
