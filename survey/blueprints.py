from flask import Blueprint

""" This module contains all blueprint and request mapping configuration and initialization for the flask app.

Blueprints will be added here with their actual package name. The flask configuration mechanism will automatically
import those blueprints and the connected handler modules.
"""


def _blprt_factory(partial_module_string, url_prefix):
    """ Factory to get blueprints for the api. """
    name = partial_module_string
    import_name = 'survey.{}'.format(partial_module_string)
    template_folder = 'templates'
    blueprint = Blueprint(name, import_name, template_folder=template_folder, url_prefix=url_prefix)
    return blueprint


app = _blprt_factory('handler', '')

all_blueprints = (app,)
