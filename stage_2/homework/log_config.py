from logging import handlers, getLogger, Formatter, \
    DEBUG, INFO, StreamHandler
from sys import stderr
from functools import wraps


class Logger():
    def __init__(self):
        self.app_log = None
        self.app_log = getLogger('app')

        if __debug__:
            self.app_log.setLevel(DEBUG)
        else:
            self.app_log.setLevel(INFO)

    def enable_stream(self):
        log = StreamHandler(stderr)
        log.setLevel(DEBUG)
        self.app_log.addHandler(log)

    def enable_tr_file(self, filename):
        if filename:
            log = handlers.TimedRotatingFileHandler(filename,
                                                    when='d',
                                                    interval=1,
                                                    utc=False,
                                                    backupCount=5)
            log.setLevel(DEBUG)
            self.app_log.addHandler(log)

    def info(self, message):
        self.app_log.info(message)

    def set_format(self, format):
        for h in self.app_log.handlers:
            h.setFormatter(Formatter(format))


class Log():
    def __init__(self, filename):
        self.filename = filename
        self.func_name = None
        self.log = Logger()
        self.log.enable_stream()
        self.log.enable_tr_file(filename)

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            self.func_name = func.__name__
            self.log.set_format('%(levelname)-10s  %(asctime)s {} %(message)s'.format(func.__name__))
            res = func(*args, **kwargs)
            self.log.info(res)
            return res

        return decorated


@Log('server.log')
def printer(word=None):
    print(word)
    if word:
        return 'OK'
    else:
        return 'NOT OK'


if __name__ == '__main__':
    printer()
