"""
    brownie test tests/test_abi_dao.py 
"""
from brownie import AbiToken, AbiMedal, AbiDao, config, network
import pytest
from web3 import Web3

from scripts.deploy import deplopy_contract, _deploy
from scripts.tools import LOCAL_BLOCKCHAIN, get_account

def test_abi_dao_invite():
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    abi_dao_contract, nft_contract, token_contract = _deploy()

    a0 = get_account()
    a1 = get_account(1)
    a2 = get_account(2)
    a3 = get_account(3)
    a4 = get_account(4) # invite this member

    tx = abi_dao_contract.inviteNewMember(a4, {'from': a1})
    tx.waits(1)
