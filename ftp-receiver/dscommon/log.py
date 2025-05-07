from loguru import logger

logger.level("HELLO", no=38, color="<m>", icon="👋")
logger.level("BYE", no=38, color="<m>", icon="👋")

def log_init(fpath="log/activity.log"):
    logger.add(fpath, rotation="6 MB", retention="14 days", compression="zip")

LOG = logger