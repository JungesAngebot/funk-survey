#!/usr/bin/env python3
"""

Command details:
    devserver           Run the application using the Flask Development
                        Server. Auto-reloads files when they change.
    tornadoserver       Run the application with Facebook's Tornado web
                        server. Forks into multiple processes to handle
                        several requests.

Usage:
    manage.py devserver [-p NUM] [-l DIR] [--config_prod] [--autoreload]
    manage.py tornadoserver [-p NUM] [-l DIR] [--config_prod] [--autoreload]

Options:
    --config_prod               Load the production configuration instead of
                                development.
    --autoreload                Enables autoreload of scripts for dev
    -l DIR --log_dir=DIR        Log all statements to file in this directory
                                instead of stdout.
                                Only ERROR statements will go to stdout. stderr
                                is not used.
    -n NUM --name=NUM           Celery Worker name integer.
                                [default: 1]
    --pid=FILE                  Celery Beat PID file.
                                [default: ./celery_beat.pid]
    -p NUM --port=NUM           Flask will listen on this port number.
                                [default: 5000]
    -s FILE --schedule=FILE     Celery Beat schedule database file.
                                [default: ./celery_beat.db]
"""

import sys
from functools import wraps

from commonspy.logging import change_log_location
from docopt import docopt
from tornado import wsgi
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, FallbackHandler

from survey.app import create_app

OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()


def command(func):
    @wraps(func)
    def wrapped():
        return func()

    if func.__name__ not in OPTIONS:
        raise KeyError('Cannot register %s, not mentioned in docstring/docopt.' % func.__name__)
    if OPTIONS[func.__name__]:
        command.chosen = func
    return wrapped


@command
def devserver():
    app = create_app()
    app.run(host='0.0.0.0', port=int(OPTIONS['--port']), use_reloader=True)


@command
def tornadoserver():
    app = create_app()

    container = wsgi.WSGIContainer(app)
    application = Application([(r'.*', FallbackHandler, dict(fallback=container))], autoreload=True if OPTIONS['--autoreload'] else False)
    http_server = HTTPServer(application)
    http_server.bind(OPTIONS['--port'])

    http_server.start(1 if OPTIONS['--autoreload'] else 0)
    IOLoop.instance().start()


if __name__ == '__main__':
    if not OPTIONS['--port'].isdigit():
        print('ERROR: Port should be a number.')
        sys.exit(1)
    getattr(command, 'chosen')()
