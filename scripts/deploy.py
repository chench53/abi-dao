from tkinter.messagebox import NO
from brownie import (
    AbiToken, 
    AbiMedal, 
    AbiDao, 
    TimeLock,
    config, 
    network
)
from web3 import Web3

from .tools import get_account


def deplopy_contract(contact_container, *args):
    account = get_account()
    # args = args or []
    print(contact_container._name, args)
    contract = contact_container.deploy(*args, {"from": account}, 
        publish_source = config["networks"][network.show_active()].get("verify", False)
    )
    print("deployed {} at {}".format(contact_container._name, contract.address))
    return contract

def _deploy():
    token_contract = deplopy_contract(AbiToken)
    nft_contract = deplopy_contract(AbiMedal)
    time_lock_contract = deplopy_contract(TimeLock, 3600, [], [])

    abi_dao_contract = deplopy_contract(AbiDao, nft_contract, time_lock_contract)

def main():
    _deploy()
