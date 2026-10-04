pragma solidity ^0.8.0;

contract SimpleWallet {
    address public owner;

    event Deposited(address indexed from, uint256 amount);
    event Withdrawn(address indexed to, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    receive() external payable {
        emit Deposited(msg.sender, msg.value);
    }

    function deposit() external payable {
        require(msg.value > 0, "Send ETH");
        emit Deposited(msg.sender, msg.value);
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function withdraw(uint256 amount) public onlyOwner {
        require(amount <= address(this).balance, "Insufficient");
        payable(owner).transfer(amount);
        emit Withdrawn(owner, amount);
    }

    function withdrawAll() public onlyOwner {
        uint256 bal = address(this).balance;
        payable(owner).transfer(bal);
        emit Withdrawn(owner, bal);
    }
}
