// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract AbiToken is ERC20, ERC20Burnable {

    address public contractOwner;
    uint256 public initialSupply;
    uint256 public supplyIncrement; 
    // uint256 public rewardAmount;

    // wei
    constructor(uint256 _supply_increment) ERC20("AbiToken", "ABI") {
        contractOwner = msg.sender;
        initialSupply = 1000000 * 10 ** 18;
        supplyIncrement = _supply_increment;
        _mint(contractOwner, initialSupply);
    }

    function addSupply() public {
        _mint(contractOwner, supplyIncrement);
    }

    function setSupplyIncrement(uint256 newSupplyIncrement) public returns (uint256) {
        supplyIncrement = newSupplyIncrement;
        return supplyIncrement;
    }

    function reward(address to) public {
        uint256 amount = gerRewardAmount(to);
        // transfer(to, amount);
        transferFrom(contractOwner, to, amount);
    }

    function gerRewardAmount(address to) public returns (uint256 amount) {
        return 500 * 10 ** 18;
    }

}