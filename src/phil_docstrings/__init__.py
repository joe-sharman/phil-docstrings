import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("google").setLevel(logging.WARNING)
