// set the url
const URL = 'http://localhost:5000';

// get the id field
const idField = document.querySelector('#user-id h3');

// show the user id if available
if (localStorage.getItem('id')) {
  idField.textContent = localStorage.getItem('id');
} else {
  idField.textContent = 'No ID provided yet';
}

// will hold the userId
let userId = idField.textContent;

// gets and saves the id
const idSaveButton = document.querySelector('#user-id button');
const idInput = document.querySelector('#user-id input');

idSaveButton.addEventListener('click', () => {
  localStorage.setItem('id', idInput.value);

  idField.textContent = idInput.value;
  userId = idInput.value;
});

// function to create element
const createNode = element => document.createElement(element);

// function to append node to another
const appendNode = (par, el) => par.appendChild(el);

// get the transactions table
const transactionsTable = document.querySelector('transaction table');

fetch(`${URL}/chain`)
  .then(res => res.json())
  .then(data => {
    console.log(data);

    const chain = data['chain'];
    // loop through the blocks in the chain
    for (let i = 0; i < chain.length; i++) {
      // loop through the transactions in the chain
      const transactions = chain[i]['transactions'];
      for (let i = 0; i < transactions.length; i++) {
        if (
          transactions[i]['sender'] === userId ||
          transactions[i]['recipient'] === userId
        ) {
          const trade = createNode('tr');
          const sender = createNode('td');
          sender.textContent = transactions[i]['sender'];
          appendNode(trade, sender);
          const recipient = createNode('td');
          sender.textContent = transactions[i]['recipient'];
          appendNode(trade, recipient);
          const amount = createNode('td');
          sender.textContent = transactions[i]['amount'];
          appendNode(trade, amount);
        }
      }
    }
  })
  .catch(err => console.log(err));
