from loguru import logger
import sys

from app.common.config import Config
from app.start import run


def run_server():
    try:
        config = Config()
        run(config)
    except Exception:
        logger.exception("Run Failed")


if __name__ == "__main__":
    logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
    run_server()
