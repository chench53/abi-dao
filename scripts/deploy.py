from brownie import AbiToken, config, network
from web3 import Web3

from .tools import INITIAL_SUPPLE, get_account

def deploy():
    # account = get_account(id="me")
    account = get_account()
    token = AbiToken.deploy(
        # Web3.toWei(INITIAL_SUPPLE, "ether"),
        {
            "from": account
        },
        publish_source = config["networks"][network.show_active()].get("verify", False)
    )
    print("deployed abi token at {}".format(token.address))
    return token

def main():
    deploy()
