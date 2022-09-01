import os

from app.app import create_app
from app.config import DevConfig, ProdConfig
from logger import create_logger

logger = create_logger(__name__)


match os.environ.get('FLASK_ENV'):
    case 'development':
        app = create_app(DevConfig)
        logger.info('FLASK_ENV set on development')
    case 'production':
        app = create_app(ProdConfig)
        logger.info('FLASK_ENV set on production')
    case _:
        logger.critical('FLASK_ENV dont set')
        raise RuntimeError('Need to set environment variable FLASK_ENV')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
