import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    test += q
except Exception as e:
    logging.debug(e)