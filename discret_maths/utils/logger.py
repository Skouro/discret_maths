import logging

_FORMAT: str = '# [%(levelname)s] %(message)s'
logging.basicConfig(format=_FORMAT)
LOGGER: logging.Logger = logging.getLogger('relationalship')
LOGGER.setLevel(logging.DEBUG)
