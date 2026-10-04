pragma solidity ^0.8.0;

contract Counter {
    address public owner;
    uint256 public count;

    constructor(uint256 start) {
        owner = msg.sender;
        count = start;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function increment() public onlyOwner {
        count += 1;
    }

    function decrement() public onlyOwner {
        require(count > 0, "Underflow");
        count -= 1;
    }

    function reset(uint256 value) public onlyOwner {
        count = value;
    }

    function getCount() public view returns (uint256) {
        return count;
    }
}
