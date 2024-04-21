from src.game.asset import Asset, AssetType
from src.utils.settings import INITIAL_CAPITAL
from typing import Optional, Set


class Player(object):
    def __init__(self, name: Optional[str]):
        self._name: str = name
        self._capital: int = INITIAL_CAPITAL
        self._portfolio: dict[str, Asset] = dict()

    def buy(self, asset: Asset) -> None:
        # A player must have enough money to buy an asset 
        if self._capital < asset.price:
            raise ValueError(f"Player {self._name} does not have enough capital to buy {asset.name}.")
        
        # If the player can buy the asset, then add it to the portfolio and subtract the price from the capital
        self._portfolio[asset.name] = asset
        self._capital -= asset.price

    def sell(self, asset: Asset) -> None:
        self._capital += asset.invested_amount
        self._capital += asset.price
        del self._portfolio[asset.name]

    def invest(self, investment_plan: list[tuple[str, str, int]]) -> None:
        for asset, action_type, amount in investment_plan:
            self.__validate_asset_in_portfolio(asset)
            self._portfolio[asset].action(type=action_type, amount=amount)

    def change_strategy(self, assets: Set[str], current_turn: int) -> None:
        for asset in assets:
            self._validate_asset_in_portfolio(asset)
            asset.change_investment_strategy(current_turn)            

    def collect_income(self) -> None:
        for asset in self._portfolio:
            self.capital += asset.calculate_interest()

    def is_bankrupt(self) -> bool:
        """ 
            A player goes bankrupt when their portfolio is empty and their capital is negative.
        """  
        return len(self._portfolio) == 0 and self._capital < 0

    def __validate_asset_in_portfolio(self, asset: str) -> None:
        if asset not in self._portfolio.keys():
            raise ValueError(f"You do not own {asset}.")
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def capital(self) -> int:
        return self._capital
    
    @property
    def assets(self) -> Set[Asset]:
        return set(self._portfolio.values())
    
    @property
    def capital_invested(self) -> int:
        return sum([asset.invested_amount for asset in self._portfolio.values()])
    
    @property
    def is_portfolio_diversified(self) -> bool:
        # A portfolio is diversified when it has at least one asset of each type
        return len(set([asset.type for asset in self._portfolio.values()])) == len(AssetType)
    
    @property
    def num_sector_investments(self) -> int:
        return len(set([asset.sector for asset in self._portfolio.values()]))

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @capital.setter
    def capital(self, capital: int) -> None:
        self._capital = capital