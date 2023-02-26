"""ZCrypto bot helpers."""
from decimal import Decimal


def decimal_price(api, coin):
    """get decimal price for order acceptance in Binance """

    return abs(Decimal(api.get_symbol_info(coin)['filters'][0]['tickSize']).normalize().as_tuple().exponent)


def decimal_quantity(api, coin):
    """get decimal quantity  for order acceptance in Binance """

    return abs(Decimal(api.get_symbol_info(coin)['filters'][1]['stepSize']).normalize().as_tuple().exponent)


def get_commission(api, coin, order):
    """Get the commission taken from the order to deduct it and calculate the correct selling quantity"""

    trades = api.get_my_trades(symbol=coin, orderId=order)

    # Reverse the list of trades
    trades = trades[::-1]

    # Initialize a variable to store the total commission
    total_commission = 0

    # Iterate over the trades
    for trade in trades:
        # Add the commission for this trade to the total
        total_commission += float(trade["commission"])

    # Convert the total to a float
    total_commission = float(total_commission)
    return total_commission


def binance_pair(pair):
    pair = pair.upper() + "USDT"
    return pair
