import logging
import sys


TIME_COLOR = "\033[32m"
LEVEL_COLOR = "\033[33m"
RESET = "\033[0m"
LOG_FORMATE = f"{TIME_COLOR}%(asctime)s{RESET} - {LEVEL_COLOR}%(levelname)s{RESET} - %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMATE, stream=sys.stdout)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMATE))

logger = logging.getLogger("XTU-NETWORK")
logger.setLevel(logging.INFO)
# logger.handlers.clear()
# logger.addHandler(handler)

_logger = logging.getLogger("httpx")
_logger.setLevel(logging.WARNING)

__all__ = ["logger"]
