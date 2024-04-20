from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Callable, Iterable, Set
from src.game.asset import Asset
from src.game.event import Event, EventType
from src.utils.settings import EVENTS_PATH
import json

class Phase(ABC):
    def __init__(self, assets) -> None:
        super().__init__()
        self.__assets_in_game: Set[Asset] = assets

    @abstractmethod
    def play(self) -> None:
        raise NotImplementedError()
    
    @abstractproperty
    def assets_in_game(self) -> Set[Asset]:
        return self.__assets_in_game


class PurchasePhase(Phase):
    def __init__(self, assets) -> None:
        super().__init__(assets)

    def play(self) -> None:
        pass

class InvestmentPhase(Phase):
    def __init__(self, assets) -> None:
        super().__init__(assets)

    def play(self) -> None:
        pass

class EventsPhase(Phase):
    def __init__(self, assets) -> None:
        super().__init__(assets)
        self.__init_events()

    def __init_events(self) -> None:
        events: Set[Event] = set([Event(descriptors['name'], descriptors['description'], descriptors['type'], descriptors['impacted_assets']) for _, descriptors in json.load(open(EVENTS_PATH, 'r')).items()])
        is_micro_economic: Callable[[dict[str, Any]], bool] = lambda e: e['type'] == EventType.MICRO_ECONOMIC
        micro_economic_events: Set[dict[str, Any]] = set(filter(is_micro_economic, events))
        macro_economic_events: Set[dict[str, Any]] = events.difference(micro_economic_events)
        self.micro_economic_events: Iterable[Event] = iter(micro_economic_events)
        self.micro_economic_events: Iterable[Event] = iter(macro_economic_events)

    def play(self) -> None:
        pass