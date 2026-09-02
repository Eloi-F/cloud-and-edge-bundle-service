import logging_config
import colorlog


class LevelPaddingFilter(logging_config.Filter):
    def filter(self, record):
        record.levelname_padded = f"{record.levelname}:".ljust(9)
        return True


def setup_logging():
    handler = colorlog.StreamHandler()

    handler.addFilter(LevelPaddingFilter())

    formatter = colorlog.ColoredFormatter(
        fmt=(
            "%(log_color)s%(levelname_padded)s%(reset)s"
            "%(blue)s%(filename)s%(reset)s "
            "[%(asctime)s] "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)

    root = logging_config.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging_config.DEBUG)
