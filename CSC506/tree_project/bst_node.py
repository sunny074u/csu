from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class BSTNode:
    key: Any
    value: Any = None
    left: Optional["BSTNode"] = None
    right: Optional["BSTNode"] = None