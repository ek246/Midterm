import logging
from pathlib import Path

def setup_logger(log_file: Path, log_level: int = logging.INFO) -> None:
    """
    Set up the logger for the application.

    Args:
        log_file (Path): The path to the log file.
        log_level (int): The logging level (default is logging.INFO).
    """
    # Ensure the log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Configure the logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
        force=True  # Ensure that the logging configuration is applied even if logging has been configured before
    )
