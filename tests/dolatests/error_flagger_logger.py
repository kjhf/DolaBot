import logging
from logging import StreamHandler


class ErrorFlaggerLogger(StreamHandler):
    errors = []

    def __init__(self):
        StreamHandler.__init__(self)
        logger = logging.getLogger()
        self.setLevel(logging.ERROR)
        logger.addHandler(self)

    def emit(self, record):
        self.errors.append(self.format(record))

    def __bool__(self):
        return len(self.errors) > 0

    def __len__(self):
        return len(self.errors)

    def clear(self):
        self.errors.clear()
