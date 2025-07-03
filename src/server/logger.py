import logging
from logging.handlers import RotatingFileHandler



filename = "logs"
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(
    filename, maxBytes=5 * 1024 * 1024, backupCount=3, encoding='utf-8'
)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)    
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


info = logger.info


def getLog() -> str:
    with open(filename, 'r', encoding='utf-8')as fr:
        return fr.read()