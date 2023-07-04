function validateForm() {
  var studentName = document.getElementById('studentName').value;
  var bookName = document.getElementById('bookName').value;
  var authorName = document.getElementById('authorName').value;
  var issueDate = document.getElementById('issueDate').value;
  var returnDate = document.getElementById('returnDate').value;

  if (studentName == '') {
    alert('Please enter Student name');
  } else if (bookName == '') {
    alert('Please enter book name');
  } else if (authorName == '') {
    alert('Please enter author name');
  } else if (issueDate == '') {
    alert('Please enter issue date');
  } else if (returnDate == '') {
    alert('Please enter return date');
  } else if (new Date(returnDate) <= new Date(issueDate)) {
    alert('Return date should be after issue date');
  }
}
