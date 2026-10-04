pragma solidity ^0.8.0;

contract DataTypesDemo {
    bool public flag;
    int256 public signedNum;
    uint256 public unsignedNum;
    address public owner;
    string public name;
    bytes32 public fixedBytes;

    constructor() {
        owner = msg.sender;
        flag = true;
        signedNum = -10;
        unsignedNum = 10;
        name = "Blockchain Lab";
        fixedBytes = keccak256(abi.encodePacked(name));
    }

    function updateValues(bool _flag, int256 _s, uint256 _u, string memory _name) public {
        string memory prefix = "Updated: ";
        flag = _flag;
        signedNum = _s;
        unsignedNum = _u;
        name = string(abi.encodePacked(prefix, _name));
        fixedBytes = keccak256(abi.encodePacked(name));
    }

    function readAll() public view returns (bool, int256, uint256, address, string memory, bytes32) {
        return (flag, signedNum, unsignedNum, owner, name, fixedBytes);
    }
}
