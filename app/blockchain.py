import hashlib
import json
from time import time
from flask import Flask, jsonify, request

class Blockchain:
    def __init__(self):
        self.chain = []
        self.wallets = {}  # New: wallet balances
        self.transactions = []  # Pending transactions
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transactions  # include all pending tx
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        while True:
            hash_val = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_val[:4] == '0000':
                return new_proof
            new_proof += 1

    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender, 'receiver': receiver, 'amount': amount})
        self.wallets[sender] = self.wallets.get(sender, 0) - amount
        self.wallets[receiver] = self.wallets.get(receiver, 0) + amount
        return self.get_previous_block()['index'] + 1

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(prev_block['proof'])
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(proof, prev_hash)
    return jsonify(block), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    required_fields = ['sender', 'receiver', 'amount']
    if not all(field in data for field in required_fields):
        return 'Missing values', 400
    index = blockchain.add_transaction(data['sender'], data['receiver'], data['amount'])
    return jsonify({'message': f'Transaction will be added to Block {index}'}), 201

@app.route('/get_balance/<wallet_id>', methods=['GET'])
def get_balance(wallet_id):
    balance = blockchain.wallets.get(wallet_id, 0)
    return jsonify({'wallet': wallet_id, 'balance': balance}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
