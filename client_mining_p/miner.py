import hashlib
import requests

import sys
import json
from time import time


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True).encode()

    proof = 0
    # start the timer here
    start_time = time()

    while valid_proof(block_string, proof) is False:
        proof += 1

    # end time
    end_time = time()
    # print the time it took to find proof
    print('Done.')
    print(f"Took {end_time - start_time} seconds to mine.\n")

    return proof


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

    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    with open("my_id.txt", "r") as f:
        id = f.read()
        print("Miner ID is", id, "\n")

    # Keep track of the number of coin
    coin_count = 0

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")

        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Internal server error!")
            print("Response returned:")
            print(r)

            # continue mining
            continue

        # Get the block from `data` and use it to look for a new proof
        print('Started mining...')
        new_proof = proof_of_work(data)

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # If the server responds with a 201
        if r.status_code == 201:
            # add 1 to the number of coins mined and print it.  Otherwise,
            coin_count += 1
            print('*', data["message"], '*')
            print(f"=> You have {coin_count} coin[s]\n")
        elif r.status_code == 400:
            # print the message from the server.
            print('*', data["message"], '*')
