import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS


class Blockchain(object):
    def __init__(self):
        # read from chain_seed file and set it as chain
        with open("chain_seed.py", "r") as f:
            # f.read() returns a string, pass it to json.loads to convert it to python object
            self.chain = json.loads(f.read())

        self.current_transactions = []

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)

        # write the chain to the chain_seed.py file
        with open("chain_seed.py", "w") as f:
            # since f.write takes a string, convert the object to string with json.dumps
            f.write(json.dumps(self.chain))

        # Return the new block
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the BLock that will hold this transaction
        """
        # append the sender, recipient and amount to the current transactions
        self.current_transactions.append(
            {'sender': sender, 'recipient': recipient, 'amount': amount})

        # return the last blocks index + 1
        return self.last_block['index'] + 1

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # Create the block_string
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        # Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        hex_hash = raw_hash.hexdigest()

        # Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 6
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        # return True or False
        return guess_hash[:6] == "000000"


# Instantiate our Node
app = Flask(__name__)
# allow cross origin across all route
CORS(app)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    """Validates if a clients proof it correct

    Returns:
        json -- message depending on if the proof is valid or not
    """
    # get the request body
    data = request.get_json()
    # check that proof and id are present in the data
    if not data.get("id") or not data.get("proof"):
        # if not return a 400 with a message
        return jsonify({
            "message": "Request body must have id and proof"
        }), 400

    # find the string of the last block
    last_block_string = json.dumps(
        blockchain.last_block, sort_keys=True).encode()
    # verify if proof is valid
    is_valid = blockchain.valid_proof(last_block_string, data["proof"])

    # return a message indicating success or failure
    if is_valid:
        # reward the miner for work so it can be part of the new block
        blockchain.new_transaction(
            sender="0", recipient=data["id"], amount=1)

        # create a new block and add it to the chain
        block = blockchain.new_block(data["proof"])

        return jsonify({
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }), 201
    else:
        return jsonify({
            "message": "Unable to forge block!"
        }), 400


@app.route('/chain', methods=['GET'])
def full_chain():
    """Returns the length and the blocks in the chain

    Returns:
        json -- A JSON object with the length and the blocks in the chain
    """
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain,
    }

    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def last_block():
    """Returns the last block in the chain

    Returns:
        json -- the last block in the chain
    """
    return jsonify(blockchain.last_block)


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # get the values in json format
    values = request.get_json()
    # check that the required fields exist
    required_fields = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required_fields):
        response = {'message': 'Error Missing values'}
        return jsonify(response), 400

    # create a new transaction
    index = blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount'])

    # set the response object with a message that the transaction will be added at the index
    response = {'message': f'Transaction will be added to Block {index}'}

    # return the response
    return jsonify(response), 201


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
