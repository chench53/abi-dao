"""
    brownie test tests/test_abi_dao.py -s
    brownie test tests/test_abi_dao.py -k test_abi_dao_vote -s
"""
import time

from brownie import (
    AbiToken, 
    AbiMedal, 
    AbiDao, 
    config, 
    exceptions,
    network,
)
import pytest
from web3 import Web3

from scripts.deploy import deplopy_contract, _deploy
from scripts.setup import (
    create_and_delegate, 
    reward_tokens, 
    approve_reward_tokens,
    queue_and_execute
)
from scripts.tools import LOCAL_BLOCKCHAIN, get_account, move_blocks

def test_abi_dao_invite():
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    abi_dao_contract, nft_contract, token_contract, _ = _deploy(2)

    admin = get_account()

    users = [get_account(i) for i in range(4)] # invite user[3]

    with pytest.raises(exceptions.VirtualMachineError, match='requires 1 nft'): # requires 1 nft
        abi_dao_contract.inviteNewMember(users[3], {'from': users[1]})

    nft_contract.createNew(users[1], {'from': admin}).wait(1)
    token_contract.approve(abi_dao_contract, 100 * 10 ** 18, {'from': users[1]}).wait(1)

    with pytest.raises(exceptions.VirtualMachineError, match='amount exceeds balance'):
        abi_dao_contract.inviteNewMember(users[3], {'from': users[1]})

    # get some tokens
    reward_tokens(token_contract, admin, admin, users[1])
    abi_dao_contract.inviteNewMember(users[3], {'from': users[1]}).wait(1)

    inviteFrom = abi_dao_contract.inviteMembersMap(users[3].address, 0)
    assert inviteFrom == users[1].address

    with pytest.raises(exceptions.VirtualMachineError, match='already invited'): # already invited
        abi_dao_contract.inviteNewMember(users[3], {'from': users[1]})
    
    # another inviter
    nft_contract.createNew(users[2], {'from': admin}).wait(1)
    reward_tokens(token_contract, admin, admin, users[2])
    token_contract.approve(abi_dao_contract, 100 * 10 ** 18, {'from': users[2]}).wait(1)
    abi_dao_contract.inviteNewMember(users[3], {'from': users[2]}).wait(1)

    with pytest.raises(exceptions.VirtualMachineError, match='already got nft'): # already got nft
        abi_dao_contract.inviteNewMember(users[3], {'from': users[1]})

    assert nft_contract.balanceOf(users[3]) == 1


def test_abi_dao_vote():
    testing_voting_period = 3
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    abi_dao_contract, nft_contract, token_contract, time_lock_contract = _deploy(2, _voting_period=testing_voting_period)

    admin = get_account()
    users = [get_account(i) for i in range(5)] 

    # Create a Proposal
    print("Create a Proposal")
    reward_calldata = token_contract.reward.encode_input(users[4])
    # reward_calldata = token_contract.addSupply.encode_input()
    targets, values, calldatas, description = [token_contract], [0], [reward_calldata], "Proposal: Give users4 some tokens"

    assert token_contract.balanceOf(admin) == Web3.toWei(1000000, 'ether')
    assert token_contract.balanceOf(users[4]) == 0

    create_and_delegate(nft_contract, admin, *[users[i] for i in range(1, 5)])

    tx = abi_dao_contract.propose(targets, values, calldatas, description, {'from': users[1]})

    if network.show_active() in LOCAL_BLOCKCHAIN:
        users[1].transfer(users[1], 0) # ??? https://github.com/brownie-mix/dao-mix/blob/main/scripts/governance_standard/deploy_and_run.py
    tx.wait(2)
    propose_id = tx.return_value
    # print(abi_dao_contract.state(propose_id))
    assert abi_dao_contract.state(propose_id) == 0 # Pending

    # Cast a Vote
    print("Cast a Vote")
    abi_dao_contract.castVote(propose_id, 1, {'from': users[1]}).wait(1)
    tx = abi_dao_contract.castVote(propose_id, 1, {'from': users[2]})
    tx.wait(1)
    assert tx.events["VoteCast"]['weight'] == 1
    assert abi_dao_contract.state(propose_id) == 1 # Active

    # Execute the Proposal
    print("Execute the Proposal")
    if network.show_active() in LOCAL_BLOCKCHAIN:
        move_blocks(testing_voting_period)
    assert abi_dao_contract.state(propose_id) == 4 # Succeeded

    approve_reward_tokens(token_contract, admin, time_lock_contract, users[4])
    queue_and_execute(abi_dao_contract, admin, targets, values, calldatas, description)
    assert token_contract.balanceOf(admin) == Web3.toWei(999500, 'ether')
    assert token_contract.balanceOf(users[4]) == Web3.toWei(500, 'ether') # users4 reward
