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
    return Path(__file__).resolve().parent.parent

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
            self.project_root = get_project_root()
            self._custom_base_dir = base_dir is not None
            if base_dir is not None:
                self.base_dir = Path(base_dir).resolve()
                self._log_dir = self.base_dir/"logs"
                self._history_dir = self.base_dir/"history"
            else:
                 self.base_dir=self.project_root
                 self._log_dir = Path(os.getenv('CALCULATOR_LOG_DIR', str(self.project_root/"calcLog"))).resolve()
                 self._history_dir = Path(os.getenv('CALCULATOR_HISTORY_DIR', str(self.project_root/'calcHistory'))).resolve()                    
            self.max_history = int(os.getenv('CALCULATOR_MAX_HISTORY', 20))
            self.auto_save = os.getenv('CALCULATOR_AUTO_SAVE', 'True').lower() in ('true', '1', 'yes')
            self.precision = precision if precision is not None else int(
    os.getenv("CALCULATOR_PRECISION", 2)
)
            self.max_input_value = (
    max_input_value
    if max_input_value is not None
    else Decimal(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000"))
)
            self.default_encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
    @property
    def log_dir(self) -> Path:
       return self._log_dir
    @property
    def history_dir(self) -> Path:
        return self._history_dir

    @property
    def history_file(self) -> Path:
        if self._custom_base_dir:
            return (self.history_dir/ 'history.csv').resolve()
        return Path(os.getenv("CALCULATOR_HISTORY_File", str(self.history_dir/ 'history.csv'))).resolve()

    @property
    def log_file(self) -> Path:
        if self._custom_base_dir:
            return(self._log_dir / "app.log").resolve()
        return Path(os.getenv('CALCULATOR_LOG_FILE', str(self.log_dir / 'app.log')))
    def validate(self) -> None:
         if self.max_history <= 0:
            raise ConfigurationError("max_history must be a positive integer.")
         if self.precision < 0:
            raise ConfigurationError("precision can't be 0 or negative")
         if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be a positive number.")
         if not self.base_dir.exists():
            raise ConfigurationError(f"Base directory {self.base_dir} does not exist.")