import logging

logging.basicConfig(
    filename="smpp_analysis.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_error(message):
    logging.error(message)

def log_info(message):
    logging.info(message)
