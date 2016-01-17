from two1.commands import buy
from two1.commands.config import Config
from two1.commands.config import TWO1_MERCHANT_HOST
from two1.commands.formatters import search_formatter
from two1.commands.formatters import sms_formatter
from two1.lib.bitrequests import BitTransferRequests
from two1.lib.bitrequests import OnChainRequests
from two1.lib.bitrequests import ChannelRequests
from two1.lib.util.uxstring import UxString
from two1.lib.channels.statemachine import PaymentChannelStateMachine
import re

from two1.lib.wallet.utxo_selectors import DEFAULT_INPUT_FEE
from two1.lib.wallet.utxo_selectors import DEFAULT_OUTPUT_FEE

# Two UTXO with one Output
DEFAULT_ONCHAIN_BUY_FEE = (DEFAULT_INPUT_FEE * 2) + DEFAULT_OUTPUT_FEE

conf = Config()

URL_REGEXP = re.compile(
    r'^(?:http)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

DEMOS = {
    "search": {"path": "/search/bing", "formatter": search_formatter},
    "sms": {"path": "/phone/send-sms", "formatter": sms_formatter}
}

class two1lib(object):

    @staticmethod
    def buy(config, resource, data, method, data_file, output_file,
         payment_method, max_price, info_only):
        """Buy from any machine payable endpoint

           Note: The two1lib _buy function does not support simply returning an object,
                 until then, include a local copy here
        """
        # If resource is a URL string, then bypass seller search
        if URL_REGEXP.match(resource):
            target_url = resource
            seller = target_url
        elif resource in DEMOS:
            target_url = TWO1_MERCHANT_HOST + DEMOS[resource]["path"]
            data = json.dumps(data)
        else:
            raise NotImplementedError('Endpoint search is not implemented!')
        
        # Change default HTTP method from "GET" to "POST", if we have data
        if method == "GET" and (data or data_file):
            method = "POST"
        
        # Set default headers for making bitrequests with JSON-like data
        headers = {'Content-Type': 'application/json'}

        try:
        # Find the correct payment method
            if payment_method == 'offchain':
                bit_req = BitTransferRequests(config.machine_auth, config.username)
            elif payment_method == 'onchain':
                bit_req = OnChainRequests(config.wallet)
            elif payment_method == 'channel':
                bit_req = ChannelRequests(config.wallet)
                channel_list = bit_req._channelclient.list()
                if not channel_list:
                    confirmed = click.confirm(UxString.buy_channel_warning.format(
                        bit_req.DEFAULT_DEPOSIT_AMOUNT,
                        PaymentChannelStateMachine.PAYMENT_TX_MIN_OUTPUT_AMOUNT), default=True)
                    if not confirmed:
                        raise Exception(UxString.buy_channel_aborted)
                    
            else:
                raise Exception('Payment method does not exist.')
                    
            # Make the request
            if info_only:
                res = bit_req.get_402_info(target_url)
            else:
                res = bit_req.request(
                    method.lower(), target_url, max_price=max_price,
                    data=data or data_file, headers=headers)
        except ResourcePriceGreaterThanMaxPriceError as e:
            config.log(UxString.Error.resource_price_greater_than_max_price.format(e))
            return
        except Exception as e:
            if 'Insufficient funds.' in str(e):
                config.log(UxString.Error.insufficient_funds_mine_more.format(
                    DEFAULT_ONCHAIN_BUY_FEE
                ))
            else:
                config.log(str(e), fg="red")
            return

        # Output results to user
        if output_file:
            # Write response output file
            output_file.write(res.content)
        elif info_only:
            # Print headers that are related to 402 payment required
            for key, val in res.items():
                config.log('{}: {}'.format(key, val))
        elif resource in DEMOS:
            config.log(DEMOS[resource]["formatter"](res))
        else:
            response = res.json()
            # Clean up names            
            for index, elem in enumerate(response):
                if elem['name'] is None:
                    response[index]['name'] = 'Please name me'
                elif len(elem['name']) == 0:
                    response[index]['name'] = 'Please name me'
                else:
                    response[index]['name'] = response[index]['name'].title()
                print(elem['description'])
                if elem['description'] is None:
                    try: 
                        response[index]['description'] = elem['owner'].title() + ' is a bad endpoint operator and forgot to place a description'
                    except:
                        response[index]['description'] = 'Anonymous is a bad endpoint operator and forgot to place a description'                        
                # Any description greater than 66 characters causes the text to overflow, this enforces a limit
                elif len(elem['description']) > 63:
                    response[index]['description'] = response[index]['description'][:63] + '...'
                    
            # Write response to console
            return response

        # Write the amount paid out if something was truly paid
        if not info_only and hasattr(res, 'amount_paid'):
            client = rest_client.TwentyOneRestClient(TWO1_HOST,
                                                     config.machine_auth,
                                                     config.username)
            user_balances = _get_balances(config, client)
            if payment_method == 'offchain':
                balance_amount = user_balances.twentyone
                balance_type = '21.co'
            elif payment_method == 'onchain':
                balance_amount = user_balances.onchain
                balance_type = 'blockchain'
            elif payment_method == 'channel':
                balance_amount = user_balances.channels
                balance_type = 'payment channels'
                config.log("You spent: %s Satoshis. Remaining %s balance: %s Satoshis." % (
                res.amount_paid, balance_type, balance_amount))

        # Record the transaction if it was a payable request
        if hasattr(res, 'paid_amount'):
            config.log_purchase(s=seller,
                                r=resource,
                                p=res.paid_amount,
                                d=str(datetime.datetime.today()))
            
    @staticmethod
    def get_quote():
        """Get list of active endpoints on the 21 marketplace
    
       Github Repo: https://github.com/weex/up
       
       Parameters: None
       Returns: Array containing marketplace endpoint data

        """

        url = 'http://10.244.34.100:21411/up-premium'
        price = 1000
        
        marketplaceInfo = two1lib.buy(conf, url, None, 'GET', None, None, 'offchain', price, False)
        
        return marketplaceInfo


