// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ModelVerification {
    mapping(string => bool) private verifiedModels;

    function verifyModel(string memory modelHash) public {
        verifiedModels[modelHash] = true;
    }

    function isModelVerified(string memory modelHash) public view returns (bool) {
        return verifiedModels[modelHash];
    }
}
