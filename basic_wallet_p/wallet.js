// get the id field
const idField = document.querySelector('#user-id h3');

// show the user id if available
if (localStorage.getItem('id')) {
  idField.textContent = localStorage.getItem('id');
} else {
  idField.textContent = 'No ID provided yet';
}

// gets and saves the id
const idSaveButton = document.querySelector('#user-id button');
const idInput = document.querySelector('#user-id input');

idSaveButton.addEventListener('click', () => {
  localStorage.setItem('id', idInput.value);

  idField.textContent = idInput.value;
});
