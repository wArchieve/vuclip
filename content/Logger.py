import logging

logger = logging.getLogger("default")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/home/pi/default.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

