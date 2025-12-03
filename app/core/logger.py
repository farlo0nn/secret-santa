import sys 

from loguru import logger

def setup_logger() -> None:
    """Configure loguru logger for the entire project"""
    
    logger.remove()
    
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    logger.add(
        "log.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )

setup_logger()