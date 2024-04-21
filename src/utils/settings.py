from typing import Set

NUM_PLAYERS: int = 2
MAX_PLAYERS: int = 5
# MAX_TURNS: int = 20
INITIAL_CAPITAL: int = 1000 # How much money every player starts with
STRATEGY_CHANGE_INTERVAL: int = 3 # How many turns to wait to change a strategy
CAPITAL_THRESHOLD_TO_WIN: int = 10000
MIN_DIFFERENT_SECTORS_TO_WIN: int = 3

# ACTIONS_SET: Set = set(['invest', 'disinvest'])
ACTIONS_PATH: str = './src/utils/assets.json' 
EVENTS_PATH: str = './src/utils/events.json' 