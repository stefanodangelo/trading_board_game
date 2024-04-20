from enum import Enum
from random import randint

class Trend(Enum):
    UP = 1
    DOWN = 0


# Singleton
class TrendCoin(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TrendCoin, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        self._trend: int = None

    def toss(self):
        self._trend = Trend(randint(Trend.DOWN.value, Trend.UP.value))

    def get_trend(self) -> int:
        return self._trend
    

COIN = TrendCoin()