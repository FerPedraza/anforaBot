import logging.handlers

def logs(app):
    handler = logging.handlers.RotatingFileHandler(
        'log.txt',
        maxBytes=1024 * 1024)
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    handler = logging.handlers.RotatingFileHandler(
        'log_gunicorn.txt',
        maxBytes=1024 * 1024)
    # only use gunicorn.error logger for all logging
    logging.getLogger('gunicorn.error').setLevel(logging.DEBUG)
    logging.getLogger('gunicorn.error').addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)


    # this would write the log messages to error.log

    #gunicorn_error_handlers = logging.getLogger('gunicorn.error').handlers
    #app.logger.handlers.extend(gunicorn_error_handlers)
    #app.logger.addHandler(myhandler1)
    #app.logger.addHandler(myhandler2)
    #app.logger.info('my info')
    #app.logger.debug('debug message')