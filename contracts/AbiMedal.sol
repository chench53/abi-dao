// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/draft-ERC721Votes.sol"; // openzeppelin@v4.5.0 draft
import "@openzeppelin/contracts/utils/cryptography/draft-EIP712.sol";


contract AbiMedal is  ERC721URIStorage, ERC721Burnable,  EIP712, ERC721Votes {

    uint256 public initialSupply;
    uint256 public tokenCounter;

    constructor() ERC721("AbiMedal", "ABI") EIP712("AbiMedal", "1") {
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
        _safeMint(to, newTokenId);
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "caller is not owner no approved");
        _setTokenURI(tokenId, _tokenURI);
    }

    // nft is not transferable
    function _beforeTokenTransfer(address from, address to, uint256 tokenId)
        internal
        virtual
        override(ERC721)
    {
        require(from == address(0) || to == address(0), "nft is not transferrable");
        super._beforeTokenTransfer(from, to, tokenId);
    }

    // The following functions are overrides required by Solidity.

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function _afterTokenTransfer(address from, address to, uint256 tokenId)
        internal
        override(ERC721, ERC721Votes)
    {
        super._afterTokenTransfer(from, to, tokenId);
    }
}
