import logging


class Logger(object):
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "crit": logging.CRITICAL,
    }

    def __init__(
        self, filepath, level="info", fmt="%(asctime)s - %(levelname)s : %(message)s"
    ):
        self.logger = logging.getLogger(filepath)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))

        terminal = logging.StreamHandler()
        terminal.setFormatter(format_str)
        handler = logging.FileHandler(filepath)
        handler.setFormatter(format_str)

        self.logger.addHandler(handler)
        self.logger.addHandler(terminal)

    def getLogger(self) -> logging.Logger:
        return self.logger

    def setLevel(self, level):
        self.logger.setLevel(self.level_relations.get(level))
