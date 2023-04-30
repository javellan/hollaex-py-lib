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
        url = f"{self.api_url}{self.base_url}/order"
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

    def get_exchange_balance(self):
        url = f"{self.api_url}{self.base_url}/admin/balance"
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "GET")
        response = requests.get(url, headers=headers)
        return response.json() 
       
    def transfer_exchange_asset(self, senderId, receiverId, currency, amount, opts={}):
       url = f"{self.api_url}{self.base_url}/admin/transfer?"
       data = {
        'sender_id':senderId,
        'receiver_id':receiverId,
        'currency':currency,
        'amount':amount
        }
       if isinstance(opts.get('description'), str):
        data['description'] = opts['description']
        
       if isinstance(opts.get('email'), bool):
        data['email'] = opts['email']
       
       path = url.replace(f"{self.api_url}{self.base_url}", '')
       print(path)

       headers = self.auth_me(path.rstrip("?"), "POST", params=data )
       response = requests.post(url, headers=headers,json=data)
       return response.json() 

    def create_exchange_deposit(self,userId, currency, amount, opts=None):
    
       url = f"{self.api_url}{self.base_url}/admin/mint"
       data = {
        'user_id': userId,
        'currency': currency,
        'amount': amount
        }

       if opts is not None:
          if isinstance(opts['transactionId'], str):
             data['transaction_id'] = opts['transactionId']

          if isinstance(opts['status'], bool):
            data['status'] = opts['status']

          if isinstance(opts['email'], bool):
            data['email'] = opts['email']

          if isinstance(opts['fee'], int) or isinstance(opts['fee'], float):
            data['fee'] = opts['fee']

       path = url.replace(f"{self.api_url}{self.base_url}", '')
       print(path)
       headers = self.auth_me(path, "POST",  params=data )
       response = requests.post(url, headers=headers,json=data)
       return response.json() 
    
    def update_exchange_deposit(self,
        transactionId,
        updatedTransactionId=None,
        updatedAddress=None,
        status=None,
        rejected=None,
        dismissed=None,
        processing=None,
        waiting=None,
        email=None,
        description=None
    ):
        url = f"{self.api_url}{self.base_url}/admin/mint?"
        data = {
            'transaction_id': transactionId
        }
    
        if isinstance(updatedTransactionId, str):
            data['updated_transaction_id'] = updatedTransactionId
    
        if isinstance(updatedAddress, str):
            data['updated_address'] = updatedAddress
    
        if isinstance(status, bool):
            data['status'] = status
    
        if isinstance(rejected, bool):
            data['rejected'] = rejected
    
        if isinstance(dismissed, bool):
            data['dismissed'] = dismissed
    
        if isinstance(processing, bool):
            data['processing'] = processing
    
        if isinstance(waiting, bool):
            data['waiting'] = waiting
    
        if isinstance(email, bool):
            data['email'] = email
    
        if isinstance(description, str):
            data['description'] = description
    
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        print(path)
        print(url)
        headers = self.auth_me(path.rstrip("?"), "PUT",  params=data )
        response = requests.put(url, headers=headers,json=data)
        return response.json()
    
    def create_exchange_withdrawal(self,userId, currency, amount, transactionId=None, status=None, email=None, fee=None):
        url = f"{self.api_url}{self.base_url}/admin/burn?"
        data = {
            'user_id': userId,
            'currency': currency,
            'amount': amount
        }
        
        if isinstance(transactionId, str):
            data['transaction_id'] = transactionId
        
        if isinstance(status, bool):
            data['status'] = status
        
        if isinstance(email, bool):
            data['email'] = email
        
        if isinstance(fee, int) or isinstance(fee, float):
            data['fee'] = fee
        
        path = url.replace(f"{self.api_url}{self.base_url}", '')

        headers = self.auth_me(path.rstrip("?"), "POST",  params=data )
        response = requests.post(url, headers=headers,json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.text}')
            return None
    
    def update_exchange_withdrawal(self, transactionId, updatedTransactionId=None, updatedAddress=None, status=None, rejected=None, dismissed=None, processing=None, waiting=None, email=None, description=None):
        url = f"{self.api_url}{self.base_url}/admin/burn?"
        data = {
            'transaction_id': transactionId
        }

        if isinstance(updatedTransactionId, str):
            data['updated_transaction_id'] = updatedTransactionId

        if isinstance(updatedAddress, str):
            data['updated_address'] = updatedAddress

        if isinstance(status, bool):
            data['status'] = status

        if isinstance(rejected, bool):
            data['rejected'] = rejected

        if isinstance(dismissed, bool):
            data['dismissed'] = dismissed

        if isinstance(processing, bool):
            data['processing'] = processing

        if isinstance(waiting, bool):
            data['waiting'] = waiting

        if isinstance(email, bool):
            data['email'] = email

        if isinstance(description, str):
            data['description'] = description

        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path.rstrip("?"), "PUT", params=data)
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.text}')
            return None
    
    def check_exchange_deposit_status(self,currency, transactionId, address, network, opts={"isTestnet": None}):
        url = f"{self.api_url}{self.base_url}/admin/check-transaction?"
        if isinstance(currency, str):
            url += f"&currency={currency}"        

        if isinstance(transactionId, str):
            url += f"&transaction_id={transactionId}"        

        if isinstance(address, str):
            url += f"&address={address}"        

        if isinstance(network, str):
            url += f"&network={network}"        

        if isinstance(opts["isTestnet"], bool):
            url += f"&is_testnet={opts['isTestnet']}"        

        path = url.replace(f"{self.api_url}{self.base_url}", '')

        headers = self.auth_me(path.rstrip('?'), "GET",  params=opts )
        response = requests.get(url, headers=headers,json=opts)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.text}')
            return None
    
    def settle_exchange_fees(self, opts = {"userId": None}):
        url = f"{self.api_url}{self.base_url}/admin/fees/settle"
        if isinstance(opts['userId'], int):
            url += f"?user_id={opts['userId']}"
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        print(path)
        print(url)
        headers = self.auth_me(path, "GET" )
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.text}')
            return None
    
    def get_exchange_trades(self,userId=None, limit=None, page=None, symbol=None, orderBy=None, order=None, startDate=None, format=None):
        url = f"{self.api_url}{self.base_url}/admin/trades?"
        if isinstance(userId, int):
            url += f"&user_id={userId}"

        if isinstance(limit, int):
            url += f"&limit={limit}"

        if isinstance(page, int):
            url += f"&page={page}"
        
        if isinstance(symbol, str):
            url += f"&symbol={symbol}"
        
        if isinstance(orderBy, str):
            url += f"&order_by={orderBy}"
        
        if isinstance(order, str) and (order == 'asc' or order == 'desc'):
            url += f"&order={order}"
        
        if isinstance(startDate, str):
            url += f"&start_date={(startDate)}"
        
        if isinstance(startDate, str):
            url += f"&end_date={(startDate)}"
        
        if isinstance(format, str) and format == 'csv':
            url += f"&format={format}"
        
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path.rstrip("?"), "GET")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.text}')
            return None
  
    def get_exchange_orders(self, userId=None, side=None, status=None, open=None, limit=None, page=None, symbol=None, orderBy=None, order=None, startDate=None, endDate=None):
        url = f"{self.api_url}{self.base_url}/admin/orders?"
        
        if isinstance(userId, int):
            url += f"&user_id={userId}"
        
        if isinstance(side, str) and (side == 'buy' or side == 'sell'):
            url += f"&side={side}"
            
        if isinstance(status, str):
            url += f"&status={status}"
        
        if isinstance(open, bool):
            url += f"&open={open}"
        
        if isinstance(limit, int):
            url += f"&limit={limit}"
        
        if isinstance(page, int):
            url += f"&page={page}"
        
        if isinstance(symbol, str):
            url += f"&symbol={symbol}"
        
        if isinstance(orderBy, str):
            url += f"&order_by={orderBy}"
        
        if isinstance(order, str) and (order == 'asc' or order == 'desc'):
            url += f"&order={order}"
        
        if isinstance(startDate, str):
            url += f"&start_date={(startDate)}"
        
        if isinstance(endDate, str):
            url += f"&end_date={(endDate)}"
        
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path.rstrip("?"), "GET")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.text}')
            return None

    def cancel_exchange_user_order(self, userId, orderId):
        
        url = f"{self.api_url}{self.base_url}/admin/order?"

        if isinstance(orderId, str):
             url += f'&order_id={orderId}'

        if isinstance(userId, int):
             url += f'&user_id={userId}'

        path = url.replace(f"{self.api_url}{self.base_url}", '')
        print(path)
        print(url)
        headers = self.auth_me(path.rstrip("?"), "DELETE")
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.text}')
            return None

    def get_exchange_users(self, userId=None, search=None, type=None, pending=None, pendingType=None,
                            limit=None, page=None, orderBy=None, order=None, startDate=None, endDate=None, format=None):
             
        url = f"{self.api_url}{self.base_url}/admin/users?"
             
        if isinstance(userId, int):
            url += f"&id={userId}"
             
        if isinstance(search, str):
            url += f"&search={search}"
             
        if isinstance(type, str):
            url += f"&type={type}"
             
        if isinstance(pending, bool):
            url += f"&pending={pending}"
             
        if isinstance(pendingType, str) and (pendingType == 'id' or pendingType == 'bank'):
            url += f"&pending_type={pendingType}"
             
        if isinstance(limit, int):
            url += f"&limit={limit}"
             
        if isinstance(page, int):
            url += f"&page={page}"
             
        if isinstance(orderBy, str):
            url += f"&order_by={orderBy}"
             
        if isinstance(order, str) and (order == 'asc' or order == 'desc'):
            url += f"&order={order}"
             
        if isinstance(startDate, str):
            url += f"&start_date={(startDate)}"
             
        if isinstance(endDate, str):
            url += f"&end_date={(endDate)}"
             
        if isinstance(format, str) and format == 'csv':
            url += f"&format={format}"
            
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        print(path)
        print(url)
        headers = self.auth_me(path.rstrip("?"), "GET")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.text}')
            return None
   
    def create_exchange_user(self, email, password):
        
        url = f"{self.api_url}{self.base_url}/admin/user"
        data = {
        'email': email,
        'password': password
         }
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "POST", params=data)
        response = requests.post(url, headers=headers,json=data)
        print(response.json())
        return response 
    #test
    def update_exchange_user(self,userId, opts={
        'role': None,
        'meta': None,
        'overwrite': None,
        'discount': None,
        'note': None,
        'verification_level': None
        }):
        if isinstance(opts['role'], str) and opts['role'] in ['admin', 'supervisor', 'support', 'kyc', 'communicator', 'user']:
             url = f"{self.api_url}{self.base_url}/admin/user/role"
        if isinstance(userId, int):
            url += f"?user_id={userId}"
            data = {'role': opts['role']}
            path = url.replace(f"{self.api_url}{self.base_url}", '')
            print(path)
            print(url)
            headers = self.auth_me(path, "PUT", params=data)
            response = requests.put(url, headers=headers,json=data)
            print(headers)
            print(response.json())
            return response 
    
        if isinstance(opts['meta'], dict):
           
           url = f"{self.api_url}{self.base_url}/admin/user/meta"
           if isinstance(userId, int):
             url += f"?user_id={userId}"
             data = {'meta': opts['meta'],
              **({'overwrite': opts['overwrite']} if isinstance(opts['overwrite'], bool) else {}), }
             path = url.replace(f"{self.api_url}{self.base_url}", '')
             print(path)
             print(url)
             headers = self.auth_me(path, "PUT", params=data)
             response = requests.put(url, headers=headers,json=data)
             print(headers)
             print(response.json())
             return response 
           
        if isinstance(opts['discount'], int) and opts['discount'] <= 100 and opts['discount'] >= 0:
            url = f"{self.api_url}{self.base_url}/admin/user/discount"
            if isinstance(userId, int):
               url += f"?user_id={userId}"
               data = {'discount': opts['discount'] }
               path = url.replace(f"{self.api_url}{self.base_url}", '')
               print(path)
               print(url)
               headers = self.auth_me(path, "PUT", params=data)
               response = requests.put(url, headers=headers,json=data)
               print(headers)
               print(response.json())
               return response        
    
        if isinstance(opts['note'], str):
            
            url = f"{self.api_url}{self.base_url}/admin/user/note"
            if isinstance(userId, int):
                url += f"?user_id={userId}"
                data = {'note': opts['note'] }
                path = url.replace(f"{self.api_url}{self.base_url}", '')
                print(path)
                print(url)
                headers = self.auth_me(path, "PUT", params=data)
                response = requests.put(url, headers=headers,json=data)
                print(headers)
                print(response.json())
                return response
    
        if isinstance(opts['verification_level'], int):
            
            url = f"{self.api_url}{self.base_url}/admin/upgrade-user"
            data = {
                'user_id': userId,
                'verification_level': opts['verification_level']
            }
            path = url.replace(f"{self.api_url}{self.base_url}", '')
            print(path)
            print(url)
            headers = self.auth_me(path, "PUT", params=data)
            response = requests.put(url, headers=headers,json=data)
            print(headers)
            print(response.json())
            return response
        
    def create_exchange_user_wallet(self, userId, crypto, opts={"network": None}):
        url = f"{self.api_url}{self.base_url}/admin/user/wallet"
        data = {"user_id": userId, "crypto": crypto}
     
        if isinstance(opts.get("network"), str):
            data["network"] = opts["network"]
 
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        print(path)
        print(url)
        headers = self.auth_me(path, "POST", params=data)
        response = requests.post(url, headers=headers,json=data)
        print(headers)
        print(response.json())
        return response
     
    def get_exchange_user_wallet(self, userId=None, limit=None, page=None, currency=None, orderBy=None, order=None, startDate=None, endDate=None, address=None, isValid=None, network=None, format=None):
            
        url = f"{self.api_url}{self.base_url}/admin/user/wallet?"
        
        if isinstance(userId, int):
            url += f"&user_id={userId}"
            
        if isinstance(currency, str):
            url += f"&currency={currency}"
            
        if isinstance(address, str):
            url += f"&address={address}"
            
        if isinstance(network, str):
            url += f"&network={network}"
            
        if isinstance(isValid, bool):
            url += f"&is_valid={str(isValid).lower()}"
            
        if isinstance(limit, int):
            url += f"&limit={limit}"
            
        if isinstance(page, int):
            url += f"&page={page}"
            
        if isinstance(orderBy, str):
            url += f"&order_by={orderBy}"
            
        if isinstance(order, str) and (order == 'asc' or order == 'desc'):
            url += f"&order={order}"
            
        if isinstance(startDate, str):
            url += f"&start_date={(startDate)}"
            
        if isinstance(endDate, str):
            url += f"&end_date={(endDate)}"
            
        if isinstance(format, str) and format == 'csv':
            url += f"&format={format}"
            
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        print(path)
        print(url)
        headers = self.auth_me(path.rstrip("?"), "GET")
        response = requests.get(url, headers=headers)
        print(headers)
        print(response.json())
        return response
     
    def get_exchange_user_balance(self, userId):
        url = f"{self.api_url}{self.base_url}/admin/user/balance?user_id={userId}"
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        print(path)
        print(url)
        headers = self.auth_me(path, "GET")
        response = requests.get(url, headers=headers)
        print(headers)
        print(response.json())
        return response
    #test
    def create_exchange_user_bank(self,userId, bankAccount):
        url = f"{self.api_url}{self.base_url}/admin/user/bank"
    
        if isinstance(userId, int):
            url += f'?id={userId}'
    
        data = {
            'bank_account': bankAccount
        }
    
        path = url.replace(f"{self.api_url}{self.base_url}", '')

        headers = self.auth_me(path, "POST",params=data)
        response = requests.post(url, headers=headers,json=data)
        print(headers)
        print(response.json())
        return response
     #test
   
    def get_exchange_user_logins(self, userId=None, limit=None, page=None, orderBy=None, order=None, startDate=None, endDate=None, format=None):
        url = f"{self.api_url}{self.base_url}/admin/logins?"
        if isinstance(userId, int):
            url += f"&user_id={userId}"
        if isinstance(limit, int):
            url += f"&limit={limit}"
        if isinstance(page, int):
            url += f"&page={page}"
        if isinstance(orderBy, str):
            url += f"&order_by={orderBy}"
        if isinstance(order, str) and (order == 'asc' or order == 'desc'):
            url += f"&order={order}"
        if isinstance(startDate, str):
            url += f"&start_date={startDate}"
        if isinstance(endDate, str):
            url += f"&end_date={endDate}"
        if isinstance(format, str) and format == 'csv':
            url += f"&format={format}"
            
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path.rstrip("?"), "GET")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.text}')
            return None
     #tested
    
    def deactivate_exchange_user(self, user_id):
        url = f"{self.api_url}{self.base_url}/admin/user/activate"
        data = {
            'user_id': user_id,
            'activated': False
        }
        path = url.replace(f"{self.api_url}{self.base_url}", '')

        headers = self.auth_me(path, "POST",params=data)
        response = requests.post(url, headers=headers,json=data)
        return response
    #test
    def deactivate_exchange_user_otp(self, userId):
        url = f"{self.api_url}{self.base_url}/admin/deactivate-otp"
        data = { 'user_id': userId   }
        path = url.replace(f"{self.api_url}{self.base_url}", '')

        headers = self.auth_me(path, "POST",params=data)
        response = requests.post(url, headers=headers,json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.text}')
            return None
    #test
    def get_exchange_user_referrals1(self, userId = None, opts = {'limit': None, 'page': None, 'orderBy': None, 'order': None, 'startDate': None, 'endDate': None}):
        url = f"{self.api_url}{self.base_url}/admin/user/affiliation?"
        
        if isinstance(userId, int):
            url += f"&user_id={userId}"
        
        if isinstance(opts['limit'], int):
            url += f"&limit={opts['limit']}"
        
        if isinstance(opts['page'], int):
            url += f"&page={opts['page']}"
        
        if isinstance(opts['orderBy'], str):
            url += f"&order_by={opts['orderBy']}"
        
        if isinstance(opts['order'], str) and (opts['order'] == 'asc' or opts['order'] == 'desc'):
            url += f"&order={opts['order']}"
        
        if isinstance(opts['startDate'], str):
            url += f"&start_date={(opts['startDate'])}"
        
        if isinstance(opts['endDate'], str):
            url += f"&end_date={(opts['endDate'])}"
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "GET")
        response = requests.get(url, headers=headers)
        return response
    #test
    def get_exchange_user_referrer(self, user_id):
        url = f"{self.api_url}{self.base_url}/admin/user/referer?user_id={user_id}"
        path = url.replace(f"{self.api_url}{self.base_url}", '')
        headers = self.auth_me(path, "GET")
        response = requests.get(url, headers=headers,)
        return response

     
