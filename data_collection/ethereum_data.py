from web3 import Web3

class EthereumDataCollector:
    def __init__(self, alchemy_url):
        self.web3 = Web3(Web3.HTTPProvider(alchemy_url))

    def get_latest_block(self):
        if self.web3.is_connected():
            return self.web3.eth.get_block('latest')
        else:
            raise ConnectionError("Not connected to Ethereum network")