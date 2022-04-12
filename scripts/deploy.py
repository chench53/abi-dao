from brownie import AbiToken, config, network
from web3 import Web3

from .tools import get_account

def deploy():
    account = get_account()
    token = AbiToken.deploy(
        {
            "from": account
        },
        publish_source = config["networks"][network.show_active()].get("verify", False)
    )
    print("deployed abi token at {}".format(token.address))
    return token

def main():
    deploy()
