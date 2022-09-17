import logging

def config_logging():
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("authorization-serv")