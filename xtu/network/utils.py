import logging
import sys

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("XTU-NETWORK")

TIME_COLOR = "\033[32m"
LEVEL_COLOR = "\033[33m"
RESET = "\033[0m"
LOG_FORMATE = f"{TIME_COLOR}%(asctime)s{RESET} - {LEVEL_COLOR}%(levelname)s{RESET} - %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMATE, stream=sys.stdout)

logger = logging.getLogger("httpx")
logger.setLevel(logging.WARNING)

__all__ = ["logger"]
