from enum import Enum
from random import shuffle
from typing import Iterable
from src.game.player import Player
from src.game.phase import Phase
from src.game.asset import OnHold
from src.utils.settings import NUM_PLAYERS, CAPITAL_THRESHOLD_TO_WIN, MIN_DIFFERENT_SECTORS_TO_WIN

class GameStatus(Enum):
    OK = 0
    ERROR = 1


class Game(object):
    def __new__(cls):
        pass
        
    def __init__(self) -> None:
        self._current_turn = 1
        self._players: Iterable[Player] = [Player()]*NUM_PLAYERS
        self._current_player: Player = next(self.players)
        self._phases: Iterable[Phase] = iter([Phase(), Phase(), Phase()])
        self._current_phase: Player = next(self.phases)
        self._winner: Player = None

    def start(self) -> GameStatus:
        self._assign_players_names()
        self._resolve_players_order()
        while not self._check_victory():
            self.current_phase.play()
            self._advance_turn()
        return self._end()

    # Private methods
    def _assign_players_names(self) -> None:
        # TODO get names from controller when implementing model-view architecture
        for name in ['Ste', 'Ciccio', 'Ale']:
            player = next(self._players)
            player.name = name

    def _resolve_players_order(self) -> None:
        if self._current_turn == 1:
            shuffle(self._players)
        else:
            # The order is decided by the player with the highest capital, and in case of ties by the player with the highest capital invested (in case of tie, then the previous turn order is preserved) 
            self._players.sort(key = lambda p: (p.capital, p.capital_invested), reverse=True)

    def _advance_turn(self) -> int:      
        # Change status of assets on hold to active if at least one turn has passed since they went on hold
        [asset.change_status() for player in self._players for asset in player.assets if not asset.is_active() and asset.last_strategy_change_turn < self.current_turn]

        # Advance to next turn
        self._current_turn += 1

    def _check_victory(self) -> bool:      
        """
            Victory is triggered when any player has reached the capital threshold with a diversified portfolio, i.e. with at least one asset of each type and one for the minimum number of required sectors.
            In addition, none of their assets must be on hold.
        """
        highest_capital: int = 0
        for p in self._players:
            if (
                p.capital >= CAPITAL_THRESHOLD_TO_WIN
                and p.num_sector_investments >= MIN_DIFFERENT_SECTORS_TO_WIN
                and p.is_portfolio_diversified
                and len([asset for asset in p.assets if isinstance(asset.status, OnHold)]) == 0
            ):
                self.winner = p
                return True
            elif p.capital > highest_capital:
                self.winner = p
                highest_capital = p.capital
        return True

    def _end(self) -> GameStatus:
        # TODO: send messages to players when implementing GUI
        return GameStatus.OK
    

    @property
    def current_turn(self) -> int:
        return self._current_turn

    @property
    def players(self) -> Iterable[Player]:
        return self._players

    @property
    def current_player(self) -> Player:
        return self._current_player

    @property
    def phases(self) -> Iterable[Phase]:
        return self._phases

    @property
    def current_phase(self) -> Player:
        return self._current_phase

    @property
    def winner(self) -> Player:
        return self._winner