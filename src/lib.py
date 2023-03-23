import json
import requests
import time
import hmac
import hashlib
import time
import hmac
import hashlib
import json


class HollaExAPI:
    def __init__(self, api_key, api_secret, api_url='https://api.hollaex.com',base_url='/v2'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url
        self.base_url= base_url

    def get_api_expires(self):
        return str(int(time.time() + 60))

    def generate_signature(self, path, method, api_expires, params=None):
        string_to_encode = method + path + api_expires
        if params:
            print(params)
            string_to_encode += json.dumps(params, separators=(',', ':'))
            print(string_to_encode)
        signature = hmac.new(self.api_secret.encode(), string_to_encode.encode(), hashlib.sha256).hexdigest()
        return signature

    def init_signature(self, path, method, is_ws=False):
        if is_ws:
            method = "CONNECT"
            path = '/stream'
        else:
            method = method
            path = f"{self.base_url}{path}"
        api_expires = self.get_api_expires()
        return method, path, api_expires

    def auth_me(self, path, method, is_ws=False, params=None):
        method, path, api_expires = self.init_signature(path, method, is_ws)
        signature = self.generate_signature(path, method, api_expires, params=params)
        headers = {
            "api-key": self.api_key,
            "api-signature": signature,
            "api-expires": api_expires
        }
        return headers

    def create_order(self, market, amount, price, side):
        url = f"{self.api_url}{self.base_url}/order"
        params = {
            'symbol': market,
            'size': amount,
            'price': price,
            'side': side,
            'type': 'limit' # or 'market' for a market order
        }
        headers = self.auth_me("/order", "POST", params=params)
        response = requests.post(url, json=params, headers=headers)
        if response.status_code == 200:
            order_id = response.json().get('id')
            return order_id
        else:
            print(f'Error creating order: {response.text}')
            return None
        
    def get_kit(self):
        url = f"{self.api_url}{self.base_url}/kit"
        headers = self.auth_me("/kit", "GET")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting kit: {response.text}')
            return None

    def get_constants(self):
        url = f"{self.api_url}{self.base_url}/constants"
        headers = self.auth_me("/constants", "GET")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting constants: {response.text}')
            return None

    def get_ticker(self,market):
        url = f"{self.api_url}{self.base_url}/ticker?symbol={market}"
        headers = self.auth_me("/ticker", "GET")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting ticker: {response.text}')
            return None
    
    def get_orderbooks(self,symbol=None):
        if symbol:
            url = f"{self.api_url}{self.base_url}/orderbooks?symbole={symbol}"
        else:
            url = f"{self.api_url}{self.base_url}/orderbooks"

        
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting orderbooks: {response.text}')
            return None

    def get_trades(self,symbol=None):
        url = f"{self.api_url}{self.base_url}/trades"
        if symbol:
            url += f"?symbol={symbol}"
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting trades: {response.text}')
            return None

    def get_user(self):
        url = f"{self.api_url}{self.base_url}/user"
        headers = self.auth_me("/user", "GET")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting user: {response.text}')

            return None

    def get_balance(self):
        url = f"{self.api_url}{self.base_url}/user/balance"
        headers = self.auth_me("/user/balance", "GET")

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting balance: {response.text}')
            return None

    def get_deposits(self,currency=None, status=None, dismissed=None, rejected=None, processing=None, waiting=None, limit=None, page=None, orderBy=None, order=None, startDate=None, endDate=None, transactionId=None, address=None):
        url = f"{self.api_url}{self.base_url}/user/deposits?"
        if currency:
            url += f"&currency={currency}"
        if limit:
            url += f"&limit={limit}"
        if page:
            url += f"&page={page}"
        if orderBy:
            url += f"&order_by={orderBy}"
        if order:
            url += f"&order={order}"
        if startDate:
            url += f"&start_date={(startDate)}"
        if endDate:
            url += f"&end_date={(endDate)}"
        if address:
            url += f"&address={address}"
        if transactionId:
            url += f"&transaction_id={transactionId}"
        if status is not None:
            url += f"&status={status}"
        if dismissed is not None:
            url += f"&dismissed={dismissed}"
        if rejected is not None:
            url += f"&rejected={rejected}"
        if processing is not None:
            url += f"&processing={processing}"
        if waiting is not None:
            url += f"&waiting={waiting}"
        
        path =url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "GET")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting deposits: {response.text}')
            return None

    def get_withdrawals(self,currency=None, status=None, dismissed=None, rejected=None, processing=None, waiting=None, limit=None, page=None, orderBy=None, order=None, startDate=None, endDate=None, transactionId=None, address=None):
        url = f"{self.api_url}{self.base_url}/user/withdrawals?"
        if currency:
            url += f"&currency={currency}"
        if limit:
            url += f"&limit={limit}"
        if page:
            url += f"&page={page}"
        if orderBy:
            url += f"&order_by={orderBy}"
        if order:
            url += f"&order={order}"
        if startDate:
            url += f"&start_date={(startDate)}"
        if endDate:
            url += f"&end_date={(endDate)}"
        if address:
            url += f"&address={address}"
        if transactionId:
            url += f"&transaction_id={transactionId}"
        if status is not None:
            url += f"&status={status}"
        if dismissed is not None:
            url += f"&dismissed={dismissed}"
        if rejected is not None:
            url += f"&rejected={rejected}"
        if processing is not None:
            url += f"&processing={processing}"
        if waiting is not None:
            url += f"&waiting={waiting}"
        
        path =url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "GET")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting withdrawals: {response.text}')
            return None

    def make_withdrawal(self, currency, amount, address, network=None):
        url = f"{self.api_url}{self.base_url}/user/withdrawal"
        params = {
            "currency": currency,
            "amount": amount,
            "address": address
        }
        if network:
            params["network"] = network
        
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "POST",  params=params)
        print(headers)
        print(params)
        response = requests.post(url, headers=headers, json=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error making withdrawal: {response.text}')
            return None

    def get_user_trades(self,symbol=None, limit=None, page=None, orderBy=None, order=None, startDate=None, endDate=None, format=None):
        url = f"{self.api_url}{self.base_url}/user/trades?"
        if symbol:
            url += f"&symbol={symbol}"
        if limit:
            url += f"&limit={limit}"
        if page:
            url += f"&page={page}"
        if orderBy:
            url += f"&order_by={orderBy}"
        if order:
            url += f"&order={order}"
        if startDate:
            url += f"&start_date={startDate}"
        if endDate:
            url += f"&end_date={endDate}"
        if format:
            url += f"&format={format}"
        
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "GET")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting user trades: {response.text}')
            return None
    import requests

    def get_order(self,order_id):
        url = f"{self.api_url}{self.base_url}/order?order_id={order_id}"
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "GET")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting order {order_id}: {response.text}")
            return None

    def get_orders(self,symbol=None, side=None, status=None, open=None, limit=None, page=None, orderBy=None, order=None, startDate=None, endDate=None):
        url = f"{self.api_url}{self.base_url}/orders?"
        if symbol:
            url += f"&symbol={symbol}"
        if side:
            url += f"&side={side}"
        if status:
            url += f"&status={status}"
        if open is not None:
            url += f"&open={open}"
        if limit:
            url += f"&limit={limit}"
        if page:
            url += f"&page={page}"
        if orderBy:
            url += f"&order_by={orderBy}"
        if order:
            url += f"&order={order}"
        if startDate:
            url += f"&start_date={(startDate)}"
        if endDate:
            url += f"&end_date={(endDate)}"
        
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "GET")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting orders: {response.text}')
            return None

    def create_order(self, symbol, side, size, type, price=0, opts=None):
        url = f"{self.apiUrl}{self.baseUrl}/order"
        data = {'symbol': symbol, 'side': side, 'size': size, 'type': type, 'price': price}

        if opts is not None:
            if 'stop' in opts and isinstance(opts['stop'], (int, float)):
                data['stop'] = opts['stop']
            if 'meta' in opts and isinstance(opts['meta'], dict):
                data['meta'] = opts['meta']
        headers = self.auth_me("/order", "POST", params=data)
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            order_id = response.json().get('id')
            return order_id
        else:
            print(f'Error creating order: {response.text}')
            return None

    def cancel_order(self,order_id):
        url = f"{self.api_url}{self.base_url}/order?order_id={order_id}"
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "DELETE")
        response = requests.delete(url,  headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f'Error cancelling order: {response.text}')
            return False
    def cancel_all_orders(self,symbol):
        if not isinstance(symbol, str):
            raise ValueError('You must provide a symbol to cancel all orders for')

        url = f"{self.api_url}{self.base_url}/order/all?symbol={symbol}"
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "DELETE")
        response = requests.delete(url,headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error cancelling all orders: {response.text}')
            return None


     
