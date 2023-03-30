# hollaex-py-lib

Python library for HollaEx Kit enabled exchanges.

**This library is specifically for end users and traders to connect to HollaEx Kit exchanges. It connects to [HollaEx Pro](https://pro.hollaex.com/trade/xht-usdt) by default.**

## Usage

```python
import hollaex

client = hollaex.HollaEx()
```

You can pass the `api-url` and `base_url` of the HollaEx-Enabled exchange to connect to. You can also pass your `api_key` and `api_secret` generated from the HollaEx-Enabled exchange.

```python
from hollaex import HollaExAPI

client = HollaExAPI(api_url='<EXCHANGE_API_URL>', 
                       base_url='<EXCHANGE_BASE_URL>', 
                       api_key='<MY_API_KEY>', 
                       api_secret='<MY_API_SECRET>')
```

You can also pass the field `api_expires` which is the length of time in seconds each request is valid for. The default value is `60`.

### Example:

```python
import hollaex

client = hollaex.HollaExAPI(api_url='<EXCHANGE_API_URL>', 
                                base_url_='<EXCHANGE_BASE_URL>', 
                                api_key='<MY_API_KEY>', 
                                api_secret ='<MY_API_SECRET>')

try:
ticker = client.get_ticker(market='xht-usdt')
print('The volume is: ', ticker)
except Exception as e:
print(e)

try:
trades = client.get_trades(symbol='xht-usdt')
print('Public trades: ', trades)
except Exception as e:
print(e)

```

### Available functions:

| Command | Parameters | Description |
| - | - | - |
| `get_kit` | | Get exchange information e.g. name, valid languages, description, etc. |
| `get_constants` | | Tick size, min price, max price, min size and max size of each symbol pair and coin |
| `get_ticker` | <ul><li>**symbol**: HollaEx trading symbol e.g. `xht-usdt`</li></ul> | Last, high, low, open and close price and volume within the last 24 hours |
| `get_tickers` | | Last, high, low, open and close price and volume within the last 24 hours for all symbols |
| `get_rderbook` | <ul><li>**symbol**: HollaEx trading symbol e.g. `xht-usdt`</li></ul> | Orderbook containing list of bids and asks |
| `get_orderbooks` | | Orderbook containing list of bids and asks for all symbols |
| `get_trades` | <ul><li>**opts**: Object with additional params</li><li>**opts.symbol**: (_optional_) HollaEx trading symbol e.g. `xht-usdt`</li></ul> | List of last trades |
| `get_user` | | User's personal information |
| `get_balance` | | User's wallet balance |
| `get_deposits` | <ul><li>**opts**: Object with additional params</li><li>**opts.currency**: (_optional_) Filter data set by asset</li><li>**opts.status**: (_optional_) Filter data set `status`</li><li>**opts.dismissed**: (_optional_) Filter data set `dismissed`</li><li>**opts.rejected**: (_optional_) Filter data set `rejected`</li><li>**opts.processing**: (_optional_) Filter data set `processing`</li><li>**opts.waiting**: (_optional_) Filter data set `waiting`</li><li>**opts.limit**: (_optional_, _default_=`50`, _max_=`50`) Number of items to get</li><li>**opts.page**: (_optional_, _default_=`1`) Page number of data</li><li>**opts.orderBy**: (_optional_) Field to order data by</li><li>**opts.order**: (_optional_, _enum_=[`asc`, `desc`]) Specify ascending or descending order</li><li>**opts.startDate**: (_optional_, _format_=`ISO8601`) Start date of data set</li><li>**opts.endDate**: (_optional_,  _format_=`ISO8601`) End date of data set</li><li>**opts.transactionId**: (_optional_) Filter data set by TXID</li><li>**opts.address**: (_optional_) Filter data set by address</li></ul> | User's list of all deposits |
| `get_withdrawals` | <ul><li>**opts**: Object with additional params</li><li>**opts.currency**: (_optional_) Filter data set by asset</li><li>**opts.status**: (_optional_) Filter data set `status`</li><li>**opts.dismissed**: (_optional_) Filter data set `dismissed`</li><li>**opts.rejected**: (_optional_) Filter data set `rejected`</li><li>**opts.processing**: (_optional_) Filter data set `processing`</li><li>**opts.waiting**: (_optional_) Filter data set `waiting`</li><li>**opts.limit**: (_optional_, _default_=`50`, _max_=`50`) Number of items to get</li><li>**opts.page**: (_optional_, _default_=`1`) Page number of data</li><li>**opts.orderBy**: (_optional_) Field to order data by</li><li>**opts.order**: (_optional_, _enum_=[`asc`, `desc`]) Specify ascending or descending order</li><li>**opts.startDate**: (_optional_, _format_=`ISO8601`) Start date of data set</li><li>**opts.endDate**: (_optional_,  _format_=`ISO8601`) End date of data set</li><li>**opts.transactionId**: (_optional_) Filter data set by TXID</li><li>**opts.address**: (_optional_) Filter data set by address</li></ul> | User's list of all withdrawals |
| `make_withdrawal` | <ul><li>**currency**: Currency code e.g. `xht`</li><li>**amount**: Withdrawal amount</li><li>**address**: Address to withdrawal to</li><li>**opts**: Object with additional params</li><li>**opts.network**: (_required if asset has multiple networks_) Blockchain network to create address for e.g. `trx`</li></ul> | Create a new withdrawal request |
| `get_user_trades` | <ul><li>**opts**: Object with additional params</li><li>**opts.symbol**: (_optional_) HollaEx trading symbol e.g. `xht-usdt`</li><li>**opts.limit**: (_optional_, _default_=`50`, _max_=`50`) Number of items to get</li><li>**opts.page**: (_optional_, _default_=`1`) Page number of data</li><li>**opts.orderBy**: (_optional_) Field to order data by</li><li>**opts.order**: (_optional_, _enum_=[`asc`, `desc`]) Specify ascending or descending order</li><li>**opts.startDate**: (_optional_, _format_=`ISO8601`) Start date of data set</li><li>**opts.endDate**: (_optional_,  _format_=`ISO8601`) End date of data set</li></ul> | User's list of all trades |
| `get_order` | <ul><li>**orderId**: HollaEx Network Order ID</li></ul> | Get specific information about a certain order |
| `get_orders` | <ul><li>**opts**: Object with additional params</li><li>**opts.symbol**: (_optional_) HollaEx trading symbol e.g. `xht-usdt`</li><li>**opts.side**: (_optional_, _enum_=[`buy`, `sell`]) Order side</li><li>**opts.status**: (_optional_) Filter data set `status`</li><li>**opts.limit**: (_optional_, _default_=`50`, _max_=`50`) Number of items to get</li><li>**opts.page**: (_optional_, _default_=`1`) Page number of data</li><li>**opts.orderBy**: (_optional_) Field to order data by</li><li>**opts.order**: (_optional_, _enum_=[`asc`, `desc`])</li><li>**opts.startDate**: (_optional_, _format_=`ISO8601`) Start date of data set</li><li>**opts.endDate**: (_optional_,  _format_=`ISO8601`) End date of data set</li></ul> | Get the list of all user orders. It can be filter by passing the symbol |
| `create_order` | <ul><li>**symbol**: HollaEx trading symbol e.g. `xht-usdt`</li><li>**side** (_enum_=[`buy`, `sell`]): Order side</li><li>**size**: Size of order to place</li><li>**type**: (_enum_=[`market`, `limit`] Order type</li><li>**price**: (_required if limit order type_) Order price</li><li>**opts**: Object with additional params</li><li>**opts.stop**: (_optional_) Stop price for order</li><li>**opts.meta**: (_optional_) Object with additional meta configurations</li><li>**opts.meta.post_only**: (_optional_, _default_=`false`) Make post only order </li><li>**opts.meta.note**: (_optional_) Custom note for order</li></ul> | Create a new order |
| `cancel_order` | <ul><li>**orderId**: HollaEx Network order ID</li></ul> | Cancel a specific order with its ID |
| `cancel_all_orders` | <ul><li>**symbol**: HollaEx trading symbol e.g. `xht-usdt`</li></ul> | Cancel all the active orders of a user, filtered by currency pair symbol |

