// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/governance/Governor.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorSettings.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorCountingSimple.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotesQuorumFraction.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorTimelockControl.sol";

import "./AbiMedal.sol";
import "./AbiToken.sol";

contract AbiDao is Governor, GovernorSettings, GovernorCountingSimple, GovernorVotes, GovernorVotesQuorumFraction, GovernorTimelockControl {

    AbiMedal abi_medal;
    AbiToken abi_token;
    mapping(address => address[]) public inviteMembersMap;
    uint32 public invite_nft_requirement;
    uint256 public invite_token_requirement;

    event inviteEvent(
        uint256 tokenBalace,
        uint256 tokenBurn
    );

    constructor(
        IVotes _nft, 
        AbiMedal _nft_, 
        AbiToken _abi_token,
        TimelockController _timelock, 
        uint32 _inviteNftRequirement, 
        uint256 _inviteTokenRequirement
    )
        Governor("AbiDao")
        GovernorSettings(1 /* 1 block */, 45818 /* 1 week */, 1)
        GovernorVotes(_nft)
        GovernorVotesQuorumFraction(66)
        GovernorTimelockControl(_timelock)
    {
        abi_medal = AbiMedal(_nft_);
        abi_token = AbiToken(_abi_token);
        invite_nft_requirement = _inviteNftRequirement;
        invite_token_requirement = _inviteTokenRequirement;
    }

    function inviteNewMember(address to) external {

        uint256 token_owned = abi_medal.balanceOf(msg.sender);
        require(token_owned == 1, "requires 1 nft");
        
        uint256 token_owned_by_to = abi_medal.balanceOf(to);
        require(token_owned_by_to == 0, "already got nft");

        for (uint i; i<inviteMembersMap[to].length; i++) {
            require(inviteMembersMap[to][i] != (msg.sender), "already invited");
        }

        emit inviteEvent(abi_token.balanceOf(msg.sender), invite_token_requirement * 10 ** 18);

        abi_token.burn(invite_token_requirement * 10 ** 18);

        inviteMembersMap[to].push(msg.sender);
        if (inviteMembersMap[to].length >= invite_nft_requirement) {
            abi_medal.createNew(to);
            delete inviteMembersMap[to];
        }
    }

    // The following functions are overrides required by Solidity.

    function votingDelay()
        public
        view
        override(IGovernor, GovernorSettings)
        returns (uint256)
    {
        return super.votingDelay();
    }

    function votingPeriod()
        public
        view
        override(IGovernor, GovernorSettings)
        returns (uint256)
    {
        return super.votingPeriod();
    }

    function quorum(uint256 blockNumber)
        public
        view
        override(IGovernor, GovernorVotesQuorumFraction)
        returns (uint256)
    {
        return super.quorum(blockNumber);
    }

    function getVotes(address account, uint256 blockNumber)
        public
        view
        override(IGovernor, GovernorVotes)
        returns (uint256)
    {
        return super.getVotes(account, blockNumber);
    }

    function state(uint256 proposalId)
        public
        view
        override(Governor, GovernorTimelockControl)
        returns (ProposalState)
    {
        return super.state(proposalId);
    }

    function propose(address[] memory targets, uint256[] memory values, bytes[] memory calldatas, string memory description)
        public
        override(Governor, IGovernor)
        returns (uint256)
    {
        return super.propose(targets, values, calldatas, description);
    }

    function proposalThreshold()
        public
        view
        override(Governor, GovernorSettings)
        returns (uint256)
    {
        return super.proposalThreshold();
    }

    function _execute(uint256 proposalId, address[] memory targets, uint256[] memory values, bytes[] memory calldatas, bytes32 descriptionHash)
        internal
        override(Governor, GovernorTimelockControl)
    {
        super._execute(proposalId, targets, values, calldatas, descriptionHash);
    }

    function _cancel(address[] memory targets, uint256[] memory values, bytes[] memory calldatas, bytes32 descriptionHash)
        internal
        override(Governor, GovernorTimelockControl)
        returns (uint256)
    {
        return super._cancel(targets, values, calldatas, descriptionHash);
    }

    function _executor()
        internal
        view
        override(Governor, GovernorTimelockControl)
        returns (address)
    {
        return super._executor();
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(Governor, GovernorTimelockControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

}