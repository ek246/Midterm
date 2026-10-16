from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List
from app.calculation import Calculation

@dataclass
class Memento:
    calcHistory: List[Calculation] 
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "calcHistory": [calc.to_dict() for calc in self.calcHistory],
            "calcTime": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Memento':
        calcHistory = [Calculation.from_dict(calc_data) for calc_data in data["calcHistory"]]
        timestamp = datetime.datetime.fromisoformat(data["calcTime"])
        return cls(calcHistory=calcHistory, timestamp=timestamp)
