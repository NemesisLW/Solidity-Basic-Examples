// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "./SimpleStorage.sol";

contract StorageFactory is SimpleStorage {

    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    function sfStore(uint _index, uint _storageNum) public {
        SimpleStorage(address(simpleStorageArray[_index])).store(_storageNum);
    }

    function sfGet(uint _index) public view returns(uint) {
    return SimpleStorage(address(simpleStorageArray[_index])).retrieve();
    }
}