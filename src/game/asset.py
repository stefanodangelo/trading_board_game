from abc import ABC, abstractmethod
from enum import Enum
import math
from src.game.coin import COIN, Trend
from src.utils.settings import STRATEGY_CHANGE_INTERVAL

# AssetStatus (state pattern)
class AssetStatus(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def switch(self, asset) -> None:
        pass

class OnHold(AssetStatus):
    def __init__(self) -> None:
        super().__init__()

    def switch(self, asset) -> None:
        asset._status = Active()

class Active(AssetStatus):
    def __init__(self) -> None:
        super().__init__()
        
    def switch(self, asset) -> None:
        asset._status = OnHold()



# InvestmentStrategy (state pattern)
class InvestmentStrategy(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def switch(self):
        raise NotImplementedError()

class Long(InvestmentStrategy):
    def __init__(self) -> None:
        super().__init__()
        
    def switch(self, asset) -> None:
        asset._investment_strategy = Short()

class Short(InvestmentStrategy):
    def __init__(self) -> None:
        super().__init__()

    def switch(self, asset) -> None:
        asset._investment_strategy = Long()



# Asset types
class AssetType(Enum):
    BOND = "Bond"
    STOCK = "Stock"
    CRYPTO = "Crypto"


# Sectors
class Sector(Enum):
    ENERGY = "Energy"
    MATERIALS = "Materials"
    HEALTHCARE = "Healthcare"
    FINANCE = "Finance"
    TECH = "Technology"
    SEMICONDUCTORS = "Semiconductors"
    COMMUNICATION = "CommunicationServices"
    REAL_ESTATE = "RealEstate"
    CONSUMER_GOODS = "ConsumerGoods"



# Asset
class Asset(object):
    def __init__(self, name: str, price: int, interest_rate: float, type: str, sector: str) -> None:
        super().__init__()
        self._status: AssetStatus = Active()
        self._investment_strategy: InvestmentStrategy = Long()
        self._name: str = name
        self._price: int = price
        self._interest_rate: float = interest_rate
        self._type: AssetType = AssetType(type.capitalize())
        self._sector: Sector = Sector(sector)
        self._invested_amount: int = 0
        self._last_strategy_change_turn: int = -STRATEGY_CHANGE_INTERVAL

    def action(self, type: str, *args) -> None:
        method = getattr(self, type)
        method(*args)

    def invest(self, amount: int) -> None:
        self._invested_amount += amount
    
    def disinvest(self, amount: int) -> None:
        if amount > self._invested_amount:
            raise ValueError("You can't disinvest more than you have invested")
        self._invested_amount -= amount

    def calculate_interest(self) -> int:
        """
            If investment strategy is long and trend is going down, or if investment strategy is short and trend is going up, then interest is negative
        """
        trend_multiplier: int = 1

        if not self.is_active():
            trend_multiplier = 0
        elif (COIN.get_trend() == Trend.DOWN and isinstance(self._investment_strategy, Long)) or (COIN.get_trend() == Trend.UP and isinstance(self._investment_strategy, Short)):
            trend_multiplier = -1
            
        return math.ceil(self.invested_amount * self.interest_rate) * trend_multiplier
    
    def change_investment_strategy(self, current_turn: int) -> None:
        if current_turn - self._last_strategy_change_turn < STRATEGY_CHANGE_INTERVAL:
            raise ValueError(f"You must wait {self._last_strategy_change_turn + STRATEGY_CHANGE_INTERVAL - current_turn} more turns before you can change investment strategy on {asset.name}.")                    
        # change strategy   
        self._investment_strategy.switch(self)
        # put asset on hold
        if self.is_active():
            self.change_status() 
        # update last turn when a change occurred to be the current turn
        self._last_strategy_change_turn = current_turn

    def change_status(self) -> None:
        self._status.switch(self)

    def is_impacted_by_event(self, impacted_types: list[str]) -> bool:
        return type(self.type).__name__ in [t.capitalize() for t in impacted_types]
    
    def is_active(self) -> bool:
        return isinstance(self._status, Active)

    @property
    def status(self) -> AssetStatus:
        return self._status
        
    @property
    def investment_strategy(self) -> InvestmentStrategy:
        return self._investment_strategy
        
    @property
    def type(self) -> AssetType:
        return self._type
        
    @property
    def name(self) -> str:
        return self._name
        
    @property
    def price(self) -> int:
        return self._price

    @property
    def sector(self) -> Sector:
        return self._sector
        
    @property
    def interest_rate(self) -> float:
        return self._interest_rate
        
    @property
    def invested_amount(self) -> int:
        return self._invested_amount
    
    @property
    def last_strategy_change_turn(self) -> int:
        return self._last_strategy_change_turn    