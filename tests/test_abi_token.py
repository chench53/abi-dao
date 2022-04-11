"""
    brownie test tests/test_abi_token.py 
"""
from brownie import AbiToken, config, network
import pytest
from web3 import Web3

# from .tools import INITIAL_SUPPLE, get_account, LOCAL_BLOCKCHAIN

from scripts.deploy import deploy
from scripts.tools import LOCAL_BLOCKCHAIN, get_account

def test_abi_token_supply():
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    abi_token = deploy()
    initialSupply = 1000000
    contractOwner = abi_token.contractOwner()
    # print(abi_token.balanceOf(contractOwner))
    assert abi_token.balanceOf(contractOwner) == initialSupply
    abi_token.addSupply()
    assert abi_token.balanceOf(contractOwner) == initialSupply + 500
    
    user = get_account(1)
    abi_token.rewward(user)
    assert abi_token.balanceOf(user) == 500
