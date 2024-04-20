import pytest
from src.game.asset import *
from src.game.coin import COIN

@pytest.fixture(scope='session')
def basic_stock():
    return Asset(name='', price=0, interest_rate=0, type='stock')

@pytest.fixture(scope='session')
def bitcoin():
    return Asset(name='Bitcoin', price=1000, interest_rate=0.8, type='crypto')


def test_asset_type(basic_stock, bitcoin):
    assert basic_stock.type == AssetType.STOCK and bitcoin.type == AssetType.CRYPTO

def test_asset_switch(basic_stock):
    asset = basic_stock
    current_status = asset.status
    asset.change_status()
    new_status = asset.status
    assert isinstance(current_status, Active) and isinstance(new_status, OnHold) and current_status != asset.change_status()

def test_investment_status_switch(basic_stock):
    asset = basic_stock
    current_status = asset.investment_strategy
    asset.change_investment_strategy(current_turn=1)
    new_status = asset.investment_strategy
    assert isinstance(current_status, Long) and isinstance(new_status, Short) and current_status != asset.change_investment_strategy(current_turn=5)

def test_interest(bitcoin):
    amount = 100
    bitcoin.invest(amount)
    COIN.toss()
    bitcoin.change_investment_strategy(current_turn=1)
    assert bitcoin.calculate_interest() == 0
    bitcoin.change_status()
    multiplier = 1 if COIN.get_trend() == Trend.DOWN else -1
    assert  bitcoin.calculate_interest() == math.ceil(amount * bitcoin.interest_rate) * multiplier