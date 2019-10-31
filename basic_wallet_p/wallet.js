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

// saves the id when the save button is clicked
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
const transactionsTable = document.querySelector('#transaction table');

// fetch the full chain and find the users transactions
fetch(`${URL}/chain`)
  .then(res => res.json())
  .then(data => {
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
          // create tr
          const trade = createNode('tr');

          // create sender td, set the value and append to tr
          const sender = createNode('td');
          sender.textContent = transactions[i]['sender'];
          appendNode(trade, sender);

          // create recipient td, set the value and append to tr
          const recipient = createNode('td');
          recipient.textContent = transactions[i]['recipient'];
          appendNode(trade, recipient);

          // create amount td, set the value and append to tr
          const amount = createNode('td');
          amount.textContent = transactions[i]['amount'];
          appendNode(trade, amount);

          // add tr to table
          appendNode(transactionsTable, trade);
        }
      }
    }
  })
  .catch(err => console.log(err));
