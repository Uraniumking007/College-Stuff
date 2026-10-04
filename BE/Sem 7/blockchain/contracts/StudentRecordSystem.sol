pragma solidity ^0.8.0;

contract StudentRecordSystem {
    address public admin;
    uint256 public studentCount;
    uint256 public registrationFee;

    struct Student {
        uint256 id;
        string name;
        string course;
        uint256 marks;
        bool exists;
        address wallet;
    }

    mapping(uint256 => Student) public students;
    mapping(address => uint256) public walletToStudentId;

    event StudentRegistered(uint256 indexed id, string name, address wallet);
    event MarksUpdated(uint256 indexed id, uint256 marks);
    event FeePaid(address indexed payer, uint256 amount);

    constructor(uint256 _feeWei) {
        admin = msg.sender;
        registrationFee = _feeWei;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Not admin");
        _;
    }

    function registerStudent(string memory name, string memory course) public payable {
        require(msg.value >= registrationFee, "Pay registration fee");
        require(walletToStudentId[msg.sender] == 0, "Already registered");
        studentCount += 1;
        students[studentCount] = Student(studentCount, name, course, 0, true, msg.sender);
        walletToStudentId[msg.sender] = studentCount;
        emit StudentRegistered(studentCount, name, msg.sender);
        emit FeePaid(msg.sender, msg.value);
    }

    function updateMarks(uint256 id, uint256 marks) public onlyAdmin {
        require(students[id].exists, "No student");
        students[id].marks = marks;
        emit MarksUpdated(id, marks);
    }

    function getStudent(uint256 id) public view returns (uint256, string memory, string memory, uint256, address) {
        Student memory s = students[id];
        require(s.exists, "No student");
        return (s.id, s.name, s.course, s.marks, s.wallet);
    }

    function contractBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function withdrawFees() public onlyAdmin {
        payable(admin).transfer(address(this).balance);
    }
}
