pragma solidity ^0.8.0;

contract Voting {
    struct Candidate {
        string name;
        uint256 votes;
    }

    address public admin;
    mapping(uint256 => Candidate) public candidates;
    mapping(address => bool) public hasVoted;
    uint256 public candidateCount;

    event CandidateAdded(uint256 indexed id, string name);
    event Voted(address indexed voter, uint256 indexed candidateId);

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Not admin");
        _;
    }

    function addCandidate(string memory name) public onlyAdmin {
        candidateCount += 1;
        candidates[candidateCount] = Candidate(name, 0);
        emit CandidateAdded(candidateCount, name);
    }

    function vote(uint256 candidateId) public {
        require(!hasVoted[msg.sender], "Already voted");
        require(candidateId > 0 && candidateId <= candidateCount, "Invalid id");
        hasVoted[msg.sender] = true;
        candidates[candidateId].votes += 1;
        emit Voted(msg.sender, candidateId);
    }

    function getVotes(uint256 candidateId) public view returns (string memory, uint256) {
        Candidate memory c = candidates[candidateId];
        return (c.name, c.votes);
    }
}
