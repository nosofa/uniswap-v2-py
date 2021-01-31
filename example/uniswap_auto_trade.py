import json
import logging
import traceback
from urllib.request import urlopen, Request
from uniswap.uniswap import UniswapV2Client
import os
from web3 import Web3
import time
from datetime import datetime
import math


logger = logging.getLogger(__name__)

ACC = 'xxx'
PRIVATE_KEY = 'xxx'
API = 'xxx'
NETWORK = 'https://mainnet.infura.io/v3/' + API
NETWORK_WSS = 'wss://mainnet.infura.io/ws/v3/' + API
WETH_ADDRESS = ''


'''Add your info here'''
B_TOKEN = '0xae1eaae3f627aaca434127644371b67b18444051'
ESTIMATED_LIQUID = 300 * (10 ** 18)

buy = True
price_to_buy = 1
price_to_sell = 2
ETH_PRICE = 1390

def get_gwei():
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}

    req = Request("https://ethgasstation.info/api/ethgasAPI.json", headers=headers, method='GET')

    with urlopen(req) as json_resp:
        gwei_data = json.loads(json_resp.read())

    return gwei_data['fast'], gwei_data['fastest']


def get_my_balance():
    my_provider = Web3.HTTPProvider(NETWORK)
    w3 = Web3(my_provider)
    return w3.eth.getBalance(Web3.toChecksumAddress(ACC))

def get_my_token_balance():
    minABI = [
    {
        "constant": "true",
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": "true",
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
    ]

    my_provider = Web3.HTTPProvider(NETWORK)
    w3 = Web3(my_provider)
    return w3.eth.contract(Web3.toChecksumAddress(ACC), abi=minABI)


if __name__ == "__main__":
    print("bot start!!!")

    client = UniswapV2Client(ACC, PRIVATE_KEY, provider=NETWORK_WSS)

    my_balance = get_my_balance()
    print('my balance: ' + str(my_balance))

    b_token_balance = get_my_token_balance()
    print("B token = " + B_TOKEN)
    print("B token balance: " + str(b_token_balance))

    '''get W-eth token'''
    WETH_ADDRESS = client.get_weth_address()
    print("W-eth address = " + WETH_ADDRESS)

    ''' check liquid added or not'''
    while True:
        pair = client.get_pair(WETH_ADDRESS, B_TOKEN)

        if pair == '0x0000000000000000000000000000000000000000':
            time.sleep(3)
            continue
        else:
            print("pair = " + pair)
            while True:

                try:
                    fast, fastest = get_gwei()
                    estimate_wei = (fast + fastest) / 2
                except:
                    print("can't get gwei, try again")
                    continue

                print("estimate Gwei = " + str(estimate_wei))


                while True:
                    try:
                        reverse_weth, reverse_b, liquidity = client.get_reserves((Web3.toChecksumAddress(WETH_ADDRESS)), Web3.toChecksumAddress(B_TOKEN))
                        break
                    except:
                        print("network error!!!")
                        time.sleep(3)
                        continue

                print("Current ETH in pool (by wei) = " + str(reverse_weth) + ", current B token in pool (10^18) = " + str(reverse_b) + ", total liquid (10^18) = " + str(liquidity))
                price_token = ( reverse_weth/reverse_b)*ETH_PRICE
                print(price_token)

                if reverse_weth == 0:
                    time.sleep(0.1)
                    continue
                elif reverse_weth < ESTIMATED_LIQUID:
                    print("not enough liquid, estimated liquid = " + str(ESTIMATED_LIQUID))
                    try:
                        fast, fastest = get_gwei()
                        estimate_wei = fast
                    except:
                        estimate_wei = estimate_wei
                    time.sleep(0.1)
                    continue
                else:
                    print("Liquid is added, start trading")

                    gas_price = math.floor( estimate_wei*(10**8))

                    now = datetime.now()

                    '''20 mins'''
                    timestamp = math.floor(datetime.timestamp(now)) + 72000

                    print(timestamp)


                    while True:

                        if buy:

                            if price_token > price_to_buy:
                                continue

                            try:

                                print("on buy tx")
                                slip_page = math.floor(estimate_wei * (10 ** 8) * 250000)
                                amount_in = math.floor(my_balance - (slip_page * 1.5))

                                path = [
                                    Web3.toChecksumAddress(WETH_ADDRESS),
                                    Web3.toChecksumAddress(B_TOKEN)
                                ]
                                print("gas price = " + str(gas_price) + " amount_in = " + str(
                                    amount_in) + " time " + str(now))

                                '''print(tx)'''
                                tx = client.swap_exact_eth_for_tokens(amount_in, 0, path, Web3.toChecksumAddress(ACC), timestamp, gas_price)
                                print("transaction created:")
                                print("https://etherscan.io/tx/" + str(Web3.toHex(tx)))


                                break
                            except Exception:
                                traceback.print_exc()
                                continue

                        else:

                            if price_token < price_to_sell:
                                continue

                            try:
                                print("on sell tx")
                                amount_in = math.floor(b_token_balance)

                                path = [
                                    Web3.toChecksumAddress(B_TOKEN),
                                    Web3.toChecksumAddress(WETH_ADDRESS)
                                ]
                                client.gasPrice = gas_price
                                tx = client.swap_exact_tokens_for_eth(amount_in, 0, path, Web3.toChecksumAddress(ACC), timestamp)
                                print("transaction created:")
                                print("https://etherscan.io/tx/" + str(Web3.toHex(tx)))

                            except Exception:
                                traceback.print_exc()

        continue
