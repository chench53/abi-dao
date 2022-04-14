"""
    brownie test tests/test_abi_dao.py -s
"""
from brownie import (
    AbiToken, 
    AbiMedal, 
    AbiDao, 
    config, 
    exceptions,
    network
)
from eth_typing import Address
import pytest
from web3 import Web3

from scripts.deploy import deplopy_contract, _deploy
from scripts.tools import LOCAL_BLOCKCHAIN, get_account

def test_abi_dao_invite():
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    abi_dao_contract, nft_contract, token_contract = _deploy(2)

    a0 = get_account()

    users = [get_account(i) for i in range(4)] # invite user[3]

    with pytest.raises(exceptions.VirtualMachineError, match='requires 1 nft'): # requires 1 nft
        abi_dao_contract.inviteNewMember(users[3], {'from': users[1]})

    nft_contract.createNew(users[1], {'from': a0}).wait(1)
    with pytest.raises(exceptions.VirtualMachineError, match='already got nft'): # already got nft
        abi_dao_contract.inviteNewMember(users[1], {'from': users[1]})

    with pytest.raises(exceptions.VirtualMachineError, match='burn amount exceeds balance'):
        abi_dao_contract.inviteNewMember(users[3], {'from': users[1]})

    # get some tokens
    token_contract.reward(users[1]).wait(1) 
    breakpoint()
    abi_dao_contract.inviteNewMember(users[3], {'from': users[1]}).wait(1)

    inviteFrom = abi_dao_contract.inviteMembersMap(users[3].address, 0)
    assert inviteFrom == users[1].address

    # another inviter
    nft_contract.createNew(users[2], {'from': a0}).wait(1)
    token_contract.reward(users[2]).wait(1)
    abi_dao_contract.inviteNewMember(users[3], {'from': users[2]}).wait(1)

    with pytest.raises(exceptions.VirtualMachineError, match='already invited'): # already invited
        tx = abi_dao_contract.inviteNewMember(users[3], {'from': users[1]})

    assert nft_contract.balanceOf(users[3]) == 1

    # inviteFrom = abi_dao_contract.inviteMembersMap(users[3].address, 0)
    # print(inviteFrom)
