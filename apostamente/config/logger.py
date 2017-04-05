import logging

from apostamente.config.settings import PATH_LOGS

logger = logging.getLogger('myapp')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

fh = logging.FileHandler(filename=PATH_LOGS + 'apostamente.log')
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)