// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "./Allowance.sol";

contract SharedWallet is Allowance {
    event MoneySent(address indexed _beneficiary, uint _amount);
    event MoneyReceived(address indexed _from, uint _amount);


    function withdrawMoney(address payable _to, uint _amount) public ownerOrAllowed(_amount) {
        require(address(this).balance >= _amount, "Not Enough Money.");
        if (!isOwner()){
            reduceAllowance(_to, _amount);
        }
        emit MoneySent(_to, _amount);
        _to.transfer(_amount);
    }

    receive() external payable {
        emit MoneyReceived(msg.sender, msg.value);
    }

    function renounceOwnership() public view override onlyOwner {
        revert("Can't Strip Ownership.");
    }
}