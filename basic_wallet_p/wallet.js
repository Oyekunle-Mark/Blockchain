const idField = document.querySelector('#user-id h4');

if (localStorage.getItem('id')) {
  idField.textContent = localStorage.getItem('id');
} else {
  idField.textContent = 'nope';
}

const idSaveButton = document.querySelector('#user-id button');
const idInput = document.querySelector('#user-id input');

idSaveButton.addEventListener('click', () => {
  localStorage.setItem('id', idInput.value);

  idField.textContent = idInput.value;
});
