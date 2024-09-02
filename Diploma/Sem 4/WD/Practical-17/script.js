let input = document.getElementById('inpput');
let addBtn = document.getElementById('add');
let removeBtn = document.getElementById('remove');
let insertHere = document.querySelector('.insert-here');

addBtn.addEventListener('click', insertNow);

function insertNow() {
  let input = document.getElementById('inpput');
  let div = document.createElement('div');
  div.innerText = input.value;
  insertHere.append(div);
  input.value = '';
}

removeBtn.addEventListener('click', removeOnclick);
function removeOnclick() {
  let removeHere = document.querySelector('.insert-here');
  removeHere.removeChild(removeHere.lastElementChild);
}
