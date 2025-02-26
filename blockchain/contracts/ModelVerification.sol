// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ModelVerification {
    mapping(bytes32 => bool) public modelHashes;

    function registerModel(bytes32 modelHash) public {
        modelHashes[modelHash] = true;
    }

    function verifyModel(bytes32 modelHash) public view returns (bool) {
        return modelHashes[modelHash];
    }
}
