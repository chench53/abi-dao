// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";


contract AbiMedal is ERC721URIStorage {

    uint256 public initialSupply;
    uint256 public tokenCounter;

    constructor () ERC721("AbiMedal", "ABIMEDAL") {
        tokenCounter = 0;
        initialSupply = 21;
    }

    function createInitSupply() public {
        for (uint256 i; i < initialSupply; i++ ) {
            if (!_exists(i)) {
                createNew(msg.sender);
            }
        }
    }

    function createNew(address to) public returns(uint256) {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "caller is not owner no approved");
        _setTokenURI(tokenId, _tokenURI);
    }

    // function _transfer(uint256 tokenId) internal override(ERC721URIStorage) {
    //     require(false, "nft not transferable");
    // }
}