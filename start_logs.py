
def logs():
    handler = logging.handlers.RotatingFileHandler(
        'log.txt',
        maxBytes=1024 * 1024)
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)