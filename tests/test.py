import time
import unittest
from web3 import Web3

from uniswap.uniswap import UniswapV2Client, UniswapV2Utils


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.address = Web3.toChecksumAddress("0x09B487E73B4Ca5aEb7B108a9Ebd91d977Aa36648")
        cls.private_key = "fe7f7b941ee8a53d7da1d16e8d4093de26046e2566880e37611265f7c3813f2b"
        cls.provider = "https://ropsten.infura.io/v3/8ce5c9d6732945bd9e8baa57c6798e0b"

        cls.factory = Web3.toChecksumAddress("0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f")
        cls.link_token = Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280")
        cls.weth_token = Web3.toChecksumAddress("0xc778417E063141139Fce010982780140Aa0cD5Ab")
        cls.link_weth_pair = Web3.toChecksumAddress("0x98A608D3f29EebB496815901fcFe8eCcC32bE54a")


class UniswapV2ClientTest(BaseTest):
    def setUp(self):
        self.uniswap = UniswapV2Client(self.address, self.private_key, self.provider)

    def test_get_pair(self):
        link_token = Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280")
        weth_token = Web3.toChecksumAddress("0xc778417E063141139Fce010982780140Aa0cD5Ab")
        pair = self.uniswap.get_pair(link_token, weth_token)
        self.assertEqual(pair, "0x98A608D3f29EebB496815901fcFe8eCcC32bE54a")

    def test_get_pair_swapped_order(self):
        link_token = Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280")
        weth_token = Web3.toChecksumAddress("0xc778417E063141139Fce010982780140Aa0cD5Ab")
        pair = self.uniswap.get_pair(weth_token, link_token)
        self.assertEqual(pair, "0x98A608D3f29EebB496815901fcFe8eCcC32bE54a")

    def test_get_pair_not_found(self):
        link_token = Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280")
        rand_token = Web3.toChecksumAddress("0xAE14A3B9F6B333BfF64bEAe1C70a93c0781D6A3F")
        pair = self.uniswap.get_pair(link_token, rand_token)
        self.assertEqual(pair, "0x0000000000000000000000000000000000000000")

    def test_get_num_pairs(self):
        num_pairs = self.uniswap.get_num_pairs()
        self.assertGreaterEqual(num_pairs, 44)

    def test_get_pair_by_index(self):
        pair = self.uniswap.get_pair_by_index(42)
        self.assertEqual(pair, "0x98A608D3f29EebB496815901fcFe8eCcC32bE54a")

    def test_get_pair_by_index_not_found(self):
        pair = self.uniswap.get_pair_by_index(45)
        self.assertEqual(pair, "0x0000000000000000000000000000000000000000")

    def test_get_fee(self):
        fee = self.uniswap.get_fee()
        self.assertEqual(fee, "0x0000000000000000000000000000000000000000")

    def test_get_fee_setter(self):
        fee_setter = self.uniswap.get_fee()
        self.assertEqual(fee_setter, "0x0000000000000000000000000000000000000000")

    def test_get_weth_address(self):
        address = self.uniswap.get_weth_address()
        self.assertEqual(address, self.weth_token)

    def test_add_liquidity(self):
        token_a = Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280")
        token_b = Web3.toChecksumAddress("0xc778417E063141139Fce010982780140Aa0cD5Ab")
        amount_a = 1 * 10**15
        amount_b = 2 * 10**13
        min_a = int((amount_b / amount_a) * 1.01)  # allow 1% slippage on B/A
        min_b = int((amount_a / amount_b) * 1.01)  # allow 1% slippage on A/B
        deadline = int(time.time()) + 1000

        tx = self.uniswap.add_liquidity(token_a, token_b, amount_a, amount_b, min_a, min_b, self.address, deadline)
        receipt = self.uniswap.conn.eth.waitForTransactionReceipt(tx, timeout=2000)

        self.assertIsNotNone(receipt)
        self.assertTrue(receipt["status"])

    def test_add_liquidity_eth(self):
        token = Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280")
        amount_token = 1 * 10**15
        amount_eth = 2 * 10**13
        min_token = int((amount_eth/amount_token)*1.01)  # allow 1% slippage on B/A
        min_eth = int((amount_token/amount_eth)*1.01)  # allow 1% slippage on A/B
        deadline = int(time.time()) + 1000

        tx = self.uniswap.add_liquidity_eth(token, amount_token, amount_eth, min_token, min_eth, self.address, deadline)
        receipt = self.uniswap.conn.eth.waitForTransactionReceipt(tx, timeout=2000)

        self.assertIsNotNone(receipt)
        self.assertTrue(receipt["status"])

    def test_remove_liquidity(self):
        token_a = Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280")
        token_b = Web3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab")
        liquidity = 1 * 10**15
        min_a = 1 * 10**15
        min_b = 2 * 10**13
        deadline = int(time.time()) + 1000

        tx = self.uniswap.remove_liquidity(token_a, token_b, liquidity, min_a, min_b, self.address, deadline)
        receipt = self.uniswap.conn.eth.waitForTransactionReceipt(tx, timeout=2000)

        self.assertIsNotNone(receipt)
        self.assertTrue(receipt["status"])

    def test_remove_liquidity_eth(self):
        token = Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280")
        liquidity = 1 * 10 ** 15
        min_token = 1 * 10 ** 15
        min_eth = 2 * 10 ** 13
        deadline = int(time.time()) + 1000

        tx = self.uniswap.remove_liquidity_eth(token, liquidity, min_token, min_eth, self.address, deadline)
        receipt = self.uniswap.conn.eth.waitForTransactionReceipt(tx, timeout=2000)

        self.assertIsNotNone(receipt)
        self.assertTrue(receipt["status"])

    def test_remove_liquidity_with_permit(self):
        pass  # TODO

    def test_remove_liquidity_eth_with_permit(self):
        pass  # TODO

    def test_swap_exact_tokens_for_tokens(self):
        amount = 1 * 10**17
        min_out = 1 * 10**15
        path = [
            Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280"),
            Web3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab")
        ]
        deadline = int(time.time()) + 1000

        tx = self.uniswap.swap_exact_tokens_for_tokens(amount, min_out, path, self.address, deadline)
        receipt = self.uniswap.conn.eth.waitForTransactionReceipt(tx, timeout=2000)

        self.assertIsNotNone(receipt)
        self.assertTrue(receipt["status"])

    def test_swap_tokens_for_exact_tokens(self):
        amount_out = 1 * 10**15
        amount_in_max = 1 * 10**17
        path = [
            Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280"),
            Web3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab")
        ]
        deadline = int(time.time()) + 1000

        tx = self.uniswap.swap_tokens_for_exact_tokens(amount_out, amount_in_max, path, self.address, deadline)
        receipt = self.uniswap.conn.eth.waitForTransactionReceipt(tx, timeout=2000)

        self.assertIsNotNone(receipt)
        self.assertTrue(receipt["status"])

    def test_swap_exact_eth_for_tokens(self):
        amount = 1 * 10**15
        min_out = 1 * 10**16
        path = [
            Web3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab"),
            Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280")
        ]
        deadline = int(time.time()) + 1000

        tx = self.uniswap.swap_exact_eth_for_tokens(amount, min_out, path, self.address, deadline)
        receipt = self.uniswap.conn.eth.waitForTransactionReceipt(tx, timeout=2000)

        self.assertIsNotNone(receipt)
        self.assertTrue(receipt["status"])

    def test_swap_tokens_for_exact_eth(self):
        amount_out = 2 * 10**15  # 0.02 ether
        amount_in_max = 5 * 10**17  # 5 linkies
        path = [
            Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280"),
            Web3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab")
        ]
        deadline = int(time.time()) + 1000

        tx = self.uniswap.swap_tokens_for_exact_eth(amount_out, amount_in_max, path, self.address, deadline)
        receipt = self.uniswap.conn.eth.waitForTransactionReceipt(tx, timeout=2000)

        self.assertIsNotNone(receipt)
        self.assertTrue(receipt["status"])

    def test_swap_exact_tokens_for_eth(self):
        amount = 1 * 10**16  # 1 linkies
        min_out = 1 * 10**15  # 0.05 ether
        path = [
            Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280"),
            Web3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab")
        ]
        deadline = int(time.time()) + 1000

        tx = self.uniswap.swap_exact_tokens_for_eth(amount, min_out, path, self.address, deadline)
        receipt = self.uniswap.conn.eth.waitForTransactionReceipt(tx, timeout=2000)

        self.assertIsNotNone(receipt)
        self.assertTrue(receipt["status"])

    def test_swap_eth_for_exact_tokens(self):
        amount_out = 1 * 10**16
        amount = 1 * 10**15
        path = [
            Web3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab"),
            Web3.toChecksumAddress("0x20fe562d797a42dcb3399062ae9546cd06f63280")
        ]
        deadline = int(time.time()) + 1000

        tx = self.uniswap.swap_eth_for_exact_tokens(amount_out, amount, path, self.address, deadline)
        receipt = self.uniswap.conn.eth.waitForTransactionReceipt(tx, timeout=2000)

        self.assertIsNotNone(receipt)
        self.assertTrue(receipt["status"])


class UniswapV2UtilsTest(BaseTest):
    def setup(self):
        self.w3 = Web3(Web3.HTTPProvider(self.provider, request_kwargs={"timeout": 60}))

    def test_sort_tokens_1(self):
        token_0, token_1 = UniswapV2Utils.sort_tokens(self.link_token, self.weth_token)
        self.assertEqual(token_0, self.link_token)
        self.assertEqual(token_1, self.weth_token)

    def test_sort_tokens_2(self):
        token_0, token_1 = UniswapV2Utils.sort_tokens(self.weth_token, self.link_token)
        self.assertEqual(token_0, self.link_token)
        self.assertEqual(token_1, self.weth_token)

    def test_sort_tokens_equal(self):
        with self.assertRaises(AssertionError):
            UniswapV2Utils.sort_tokens(self.link_token, self.link_token)

    def test_sort_tokens_zero(self):
        with self.assertRaises(AssertionError):
            UniswapV2Utils.sort_tokens(Web3.toHex(0x0), self.link_token)

    def test_pair_for_1(self):
        pair = UniswapV2Utils.pair_for(self.factory, self.link_token, self.weth_token)
        self.assertEqual(pair, self.link_weth_pair)

    def test_pair_for_2(self):
        pair = UniswapV2Utils.pair_for(self.factory, self.weth_token, self.link_token)
        self.assertEqual(pair, self.link_weth_pair)

    def test_get_reserves(self):
        pass  # TODO

    def calculate_quote(self):
        pass  # TODO

    def test_get_amount_out(self):
        pass  # TODO

    def test_get_amount_in(self):
        pass  # TODO

    def test_get_amounts_out(self):
        pass  # TODO

    def test_get_amounts_in(self):
        pass  # TODO
