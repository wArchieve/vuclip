import logging

logger = logging.getLogger("default")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/home/box/content/default.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

