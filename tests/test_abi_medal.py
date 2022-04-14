"""
    brownie test tests/test_abi_medal.py -s
"""
from brownie import AbiMedal, config, network, exceptions
import pytest
from web3 import Web3

from scripts.deploy import deplopy_contract
from scripts.tools import LOCAL_BLOCKCHAIN, get_account

def test_abi_medal():
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    abi_medal = deplopy_contract(AbiMedal)

    account = get_account()
    users = [get_account(i) for i in range(1, 4)]

    abi_medal.createNew(users[1], {'from': account}).wait(1)
    # abi_medal.createNew(users[2], {'from': account}).wait(1)

    with pytest.raises(exceptions.VirtualMachineError, match='not transferrable'):
        abi_medal.safeTransferFrom(users[1], users[2], 0, {'from': users[1]})

    assert abi_medal.ownerOf(0) == users[1]
