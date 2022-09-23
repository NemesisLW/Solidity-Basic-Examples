// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";


contract Allowance is Ownable {

    function isOwner() internal view returns(bool) {
        return owner() == msg.sender;
    }

    event UpdatedAllowance(address indexed _for, address indexed _by, uint _oldAmount, uint _newAmount);
    mapping(address => uint) allowance;

    modifier ownerOrAllowed(uint _amount) {
        require(isOwner() || allowance[msg.sender] >= _amount, "Not Allowed");
        _;
    }

    function setAllowance(address _beneficiary, uint _amount) public onlyOwner {
        emit UpdatedAllowance(_beneficiary, msg.sender, allowance[_beneficiary], _amount);
        allowance[_beneficiary] = _amount;
    }

    function addAllowance(address _beneficiary, uint _amount) public onlyOwner {
        emit UpdatedAllowance(_beneficiary, msg.sender, allowance[_beneficiary], allowance[_beneficiary] + _amount);
        allowance[_beneficiary] += _amount;
    }

    function reduceAllowance(address _beneficiary, uint _amount) internal {
        emit UpdatedAllowance(_beneficiary, msg.sender, allowance[_beneficiary], allowance[_beneficiary] - _amount);
        allowance[_beneficiary] -= _amount;
    }
}