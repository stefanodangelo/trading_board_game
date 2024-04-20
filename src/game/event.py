from typing import Set
from enum import Enum

class EventType(Enum):
    """
    Types of events
    """
    MICRO_ECONOMIC = "micro"
    MACRO_ECONOMIC = "macro"

class Event(object):
    # Events only impact active assets

    def __init__(self, name: str, description: str, type_: str, impacted_asset_types: Set[str]) -> None:
        self.name: str = name
        self.description: str = description
        self.type: EventType = EventType(type_.capitalize())
        self.impacted_asset_types: Set[str] = impacted_asset_types

    def take_place(self) -> None:
        pass