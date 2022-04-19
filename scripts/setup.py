import time

from brownie import (
    AbiToken, 
    AbiMedal, 
    AbiDao,
    TimeLock,
    config, 
    network
)
from web3 import Web3


def create_and_delegate(nft_contract, account, *users):
    """create nft for new user and delegate vote right to self
    """
    for user in users:
        nft_contract.createNew(user, {'from': account})
        tx = nft_contract.delegate(user, {'from': user}) # delegate required to vote
    tx.wait(1)

def approve_reward_tokens(token_contract, tokens_owner, executor, to):
    tx = token_contract.gerRewardAmount(to)
    reward_amount = tx.return_value
    token_contract.approve(executor, reward_amount, {'from': tokens_owner})

def reward_tokens(token_contract, tokens_owner, executor, to):
    approve_reward_tokens(token_contract, tokens_owner, executor, to)
    token_contract.reward(to, {'from': tokens_owner}).wait(1)

def queue_and_execute(governor_contract, account, targets, values, calldatas, description):
    """execute succeed proposal"""
    description_hash = Web3.keccak(text=description).hex()
    tx = governor_contract.queue(
        targets,
        values,
        calldatas,
        description_hash,
        {"from": account},
    )
    tx.wait(1)
    time.sleep(2)
    tx = governor_contract.execute(
        targets,
        values,
        calldatas,
        description_hash,
        {"from": account},
    )
    tx.wait(1)
