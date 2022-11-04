import base64
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

CURRENT_PATH = Path(__file__).parent.parent
DATA_BASE_PATH = Path.joinpath(CURRENT_PATH, 'app', 'movies.db')

DEBUG_LOG_PATH = Path.joinpath(CURRENT_PATH, 'debug_log.log')
ERROR_LOG_PATH = Path.joinpath(CURRENT_PATH, 'errors_log.log')
ALGORITHMS = "HS256"
PWD_HASH_ITERATIONS = 100_000
PWD_HASH_SALT = base64.b64decode(os.getenv('PWD_HASH_SALT', 'salt'))
SECRET = os.environ.get('SECRET', 'secret')
