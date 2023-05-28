# Import the HollaExAPI class from the lib.py in src directory, you can copy the file in the example directory
from lib.py  import HollaExAPI
# Set your API key and secret
API_KEY = 'your_api_key'
API_SECRET = 'your_secret_key'

# Create an instance of the HollaExAPI class with your API key and secret
kit = HollaExAPI(api_key=API_KEY, api_secret=API_SECRET)

# Place a sell order for 1 XHT at a price of 1 USDT create_order(market,amount,price,side)
kit.create_order('xht-usdt',1,1,'sell')

# Cancel all orders for the XHT/USDT market
kit.cancel_all_orders('xht-usdt')

# Cancel a specific order with the given order ID
kit.cancel_order('178a1b3b-27d4-4a57-a990-448ac61882cd')

# Get all open orders for the XHT/USDT market
print(kit.get_orders(symbol='xht-usdt'))

# Get a specific order with the given order ID
order = kit.get_order("178a1b3b-27d4-4a57-a990-448ac61882cd")
if order:
    print(order)
else:
    print("Failed to retrieve order.")

# Get all user trades for the XHT/USDT market
print(kit.get_user_trades(symbol='xht-usdt'))

# Withdraw 1 USDT to the specified address on the TRX network
kit.make_withdrawal(currency='usdt', amount=1, address='TFQ9gxeMEkmKoxgrbnHNdu4e3VdNL11vyy', network='trx')

# Get all withdrawals for the XHT currency that are not waiting for confirmation
print(kit.get_withdrawals(currency='xht', waiting='false'))

# Get the balance of XHT in your account
print(kit.get_balance())

# Get user information for your account
print(kit.get_user())

# Get all trades for your account
print(kit.get_trades())

# Get the order book for the XHT/USDT market
orderbooks = kit.get_orderbooks('xht-usdt')
print(orderbooks)

# Get the ticker for the XHT/USDT market
print(kit.get_ticker('xht-usdt'))

# Get all constants for the HollaEx API
print(kit.get_constants())

# Place a sell order for 1 XHT at a price of 1 USDT
kit.create_order("xht-usdt", 1, 1, "sell")
