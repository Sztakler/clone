import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from enum import Enum


class LogLevel(str, Enum):
    INFO = "info"
    DEBUG = "debug"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    def __str__(self):
        return self.value.upper()

def configure_logging(
    log_level: LogLevel.INFO = LogLevel.INFO,
    log_file: str = "robot_monitor.log",
    max_log_size: int = 10 * 1024 * 1024,# 10 MB
    backup_count: int = 3
) -> None: 
    log_path = Path(log_file).parent
    log_path.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_log_size,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    log_level_mapping = {
        LogLevel.INFO: logging.INFO,
        LogLevel.DEBUG: logging.DEBUG,
        LogLevel.WARNING: logging.WARNING,
        LogLevel.ERROR: logging.ERROR,
    }
    logger.setLevel(log_level_mapping[log_level])
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info("Logging został skonfigurowany!")


