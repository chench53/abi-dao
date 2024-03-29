from brownie import accounts, network, config, chain
from web3 import Web3

FORKED_LOCAL_BLOCKCHAIN = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN = ['development', 'ganache-local']

DECIMALS = 8
INITIAL_SUPPLE = 1000000

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN + FORKED_LOCAL_BLOCKCHAIN:
        return accounts[0]

    return accounts.add(config['wallets']['from_key'])

def move_blocks(amount):
    for block in range(amount):
        get_account().transfer(get_account(), 0)
    print(chain.height)
