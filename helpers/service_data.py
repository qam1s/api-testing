from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel


@dataclass
class ServiceDataModel:
    model: Optional[BaseModel] = None
    payloads: Optional[Any] = None
