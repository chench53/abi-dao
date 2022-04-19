from brownie import (
    AbiToken, 
    AbiMedal, 
    AbiDao, 
    TimeLock,
    config, 
    network
)
from web3 import constants, Web3

from .tools import get_account


def deplopy_contract(contact_container, *args):
    account = get_account()
    contract = contact_container.deploy(*args, {"from": account}, 
        publish_source = config["networks"][network.show_active()].get("verify", False)
    )
    print("deployed {} at {}".format(contact_container._name, contract.address))
    return contract

def _deploy(_inviteNftRequirement=5, _inviteTokenRequirement=100, _quorum_percentage=25, _voting_period=45818):
    """ 
        args:
            _voting_period=45818 # 1 week
    """
    account = get_account()
    token_contract = deplopy_contract(AbiToken, 500*10**18)
    nft_contract = deplopy_contract(AbiMedal)
    time_lock_contract = deplopy_contract(TimeLock, 1, [], [])

    abi_dao_contract = deplopy_contract(
        AbiDao, 
        nft_contract, 
        nft_contract, 
        token_contract,
        time_lock_contract, 
        _inviteNftRequirement, 
        _inviteTokenRequirement,
        _quorum_percentage,
        _voting_period
    )
    PROPOSER_ROLE = time_lock_contract.PROPOSER_ROLE()
    EXECUTOR_ROLE = time_lock_contract.EXECUTOR_ROLE()
    # print(PROPOSER_ROLE, EXECUTOR_ROLE)

    time_lock_contract.grantRole(PROPOSER_ROLE, abi_dao_contract,{"from": account}).wait(1)

    time_lock_contract.grantRole(
        EXECUTOR_ROLE, 
        # constants.ADDRESS_ZERO, # ?? not work
        abi_dao_contract,
        {"from": account}
    ).wait(1)
    # print(f'''
    #     grant executor role {EXECUTOR_ROLE} for {account}: 
    #     {time_lock_contract.hasRole(EXECUTOR_ROLE, account)}
    # ''')
    return (abi_dao_contract, nft_contract, token_contract, time_lock_contract)

def main():
    _deploy()
