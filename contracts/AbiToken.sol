// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract AbiToken is ERC20, Ownable {

    address public contractOwner;
    uint256 public initialSupply;
    uint256 public supplyIncrement; 

    // wei
    constructor() ERC20("AbiToken", "ABI") {
        contractOwner = msg.sender;
        initialSupply = 1000000;
        _mint(contractOwner, initialSupply);
    }

    function addSupply() public {
        _mint(contractOwner, supplyIncrement);
    }

    function setSupplyIncrement(uint256 newSupplyIncrement) public returns (uint256) {
        supplyIncrement = newSupplyIncrement;
        return supplyIncrement;
    }

    function rewward(address to) public {
        uint256 amount = _gerRewardAmount(to);
        transfer(to, amount);
    }

    function _gerRewardAmount(address to) internal returns (uint256 amount) {
        return 500;
    }

}