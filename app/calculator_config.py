from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
from pathlib import Path
import os
from typing import Optional
from dotenv import load_dotenv
from app.exceptions import ConfigurationError

load_dotenv()

def get_project_root() -> Path:
    current_file = Path(__file__)
    return current_file.parent.parent

@dataclass
class CalculatorConfig:
    """
    Configuration class for the calculator application.
    Loads configuration values from environment variables.
    """

    # Load environment variables
    def __init__(self,
                base_dir: Optional[Path] = None,
                max_history: Optional[int] = None,
                auto_save: Optional[bool] = None,
                precision: Optional[int] = None,
                max_input_value: Optional[Number] = None,
                default_encoding: Optional[str] = None):
            project_root = get_project_root()
            self.base_dir = Path(os.getenv('CALCULATOR_LOG_DIR', project_root / 'logger.py'))
            self.history_dir = Path(os.getenv('CALCULATOR_HISTORY_DIR', project_root / 'calcHistory'))
            self.max_history = int(os.getenv('CALCULATOR_MAX_HISTORY', 20))
            self.auto_save = os.getenv('CALCULATOR_AUTO_SAVE', 'True').lower() in ('true', '1', 'yes')
            self.precision = int(os.getenv('CALCULATOR_PRECISION', 2))
            self.max_input_value = Decimal(os.getenv('CALCULATOR_MAX_INPUT_VALUE', 1000000))
            self.default_encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
    @property
    def log_dir(self) -> Path:
        return Path(os.getenv('CALCULATOR_LOG_DIR', get_project_root() / 'app'))

    @property
    def history_dir(self) -> Path:
        return Path(os.getenv('CALCULATOR_HISTORY_DIR', get_project_root() / 'calcHistory'))

    @property
    def history_file(self) -> Path:
        return Path(os.getenv('CALCULATOR_HISTORY_FILE', self.history_dir / 'history.txt'))

    @property
    def log_file(self) -> Path:
        return Path(os.getenv('CALCULATOR_LOG_FILE', self.log_dir / 'app/logger.py'))

    def validate(self) -> None:
         if self.max_history <= 0:
            raise ConfigurationError("max_history must be a positive integer.")
         if self.precision < 0:
            raise ConfigurationError("precision must be a non-negative integer.")
         if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be a positive number.")
         if not self.base_dir.exists():
            raise ConfigurationError(f"Base directory {self.base_dir} does not exist.")

