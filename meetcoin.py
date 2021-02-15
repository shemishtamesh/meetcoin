from utils import *  # utils & constants
from Crypto.PublicKey import ECC  # Elliptic Curve Cryptography
from Crypto.Signature import DSS  # Digital Standard Signature
import json  # for serialization
from math import sqrt  # for choosing leader
import socket  # for peer to peer interaction


class Transaction:
    def __init__(self,
                 receiver=INITIAL_COIN_HOLDER,
                 sender="",
                 amount=NUMBER_OF_COINS + 1,  # +1 for fee second (initial stacking) transaction
                 signature="",
                 fee=0):
        self.signature = signature  # signature of the wallet that looses money from the transaction
        self.sender = sender  # sender's wallet's public key
        self.receiver = receiver  # receiver's wallet's public key
        self.amount = amount
        self.fee = fee

    def is_valid(self, blockchain):
        """returns true iff the transaction is valid"""
        if not (self == Transaction() and self in blockchain.chain[0].data):  # unless initial transaction for initial coin offering
            # check signature against sender and rest of transaction:
            hash_of_transaction = self.hash_transaction()
            verifier = DSS.new(ECC.import_key(self.sender), STANDARD_FOR_SIGNATURES)
            try:
                verifier.verify(hash_of_transaction, eval(self.signature))
            except ValueError:
                return False

            # check if the receiver and sender are valid (if it's a point on the elliptic curve):
            # is receiver valid:
            if self.receiver != STAKE_ADDRESS:
                receiver_key = ECC.import_key(self.receiver)
                try:
                    x = int(receiver_key.pointQ.x)
                    y = int(receiver_key.pointQ.y)
                except AttributeError:
                    return False
                if ((y ** 2) - ((x ** 3) - (a * x) + b)) % p == 0:
                    return False

            # is sender valid:
            sender_key = ECC.import_key(self.sender)
            try:
                x = int(sender_key.pointQ.x)
                y = int(sender_key.pointQ.y)
            except AttributeError:
                return False
            if ((y ** 2) - ((x ** 3) - (a * x) + b)) % p == 0:
                return False

            if self.receiver == STAKE_ADDRESS and self.amount <= 0:  # check if valid for stake transaction:
                return False

            # check if fee is valid:
            if float(self.fee) != TRANSACTION_FEE:
                return False

            # check if amount is more than 0:
            if self.amount <= 0:
                return False

            # check if the amount can be sent by sender:
            if blockchain.get_balance(self.sender) < (self.amount + self.fee):
                return False

            # check if transaction is a duplicate of an existing transaction:
            for block in blockchain.chain:
               for transaction_json in block.data:
                   transaction = Transaction.deserialize(transaction_json)
                   if transaction == self:
                       return False

        return True

    def __str__(self):
        return f"signature: {self.signature}\n" \
               + f"sender: {self.sender}\n" \
               + f"receiver: {self.receiver}\n" \
               + f"amount: {self.amount}\n" \
               + f"fee: {self.fee}\n"

    def serialize(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def deserialize(data):
        data_dict = json.loads(data)
        return Transaction(data_dict["receiver"],
                           data_dict["sender"],
                           data_dict["amount"],
                           data_dict["signature"],
                           data_dict["fee"])

    def hash_transaction(self):
        return sha256_hash(self.sender, self.receiver, self.amount, self.fee)


class Block:
    def __init__(self,
                 number=0,
                 prev_hash="",
                 data="",
                 validator="",
                 signature=""):
        self.block_number = number
        self.prev_hash = prev_hash
        if data == "":
            first_transaction = Transaction().serialize()
            second_transaction = INITIAL_STAKE_TRANSACTION
            self.data = [first_transaction, second_transaction]
        else:
            self.data = data
        self.validator = validator
        self.signature = signature

    def __str__(self):
        return f"block number: {self.block_number}\n" \
               + f"previous hash: {self.prev_hash}\n" \
               + f"current hash: {self.hash_block().hexdigest()}\n" \
               + f"data: {self.data}\n" \
               + f"validator: {self.validator}\n" \
               + f"signature: {self.signature}\n"

    def hash_block(self):
        """returns the hash of the block"""
        return sha256_hash(self.block_number, self.prev_hash, self.data, self.validator, self.signature)

    def is_valid(self, blockchain):
        if self != Block():  # allow the genesis block
            # check transactions:
            for transaction_json in self.data:
                transaction = Transaction.deserialize(transaction_json)
                if not transaction.is_valid(blockchain):
                    return False

            # check signature:
            hash_of_block_content = sha256_hash(self.block_number, self.prev_hash, self.data)
            verifier = DSS.new(ECC.import_key(self.validator), STANDARD_FOR_SIGNATURES)
            try:
                verifier.verify(hash_of_block_content, eval(self.signature))
            except ValueError:
                return False

            # check block number:
            if self.block_number != blockchain.chain[-1].block_number + 1:
                return False

            # check if everyone can pay all for all transactions in block:
            senders = {}
            for transaction_json in self.data:
                transaction = Transaction.deserialize(transaction_json)
                if transaction.sender not in senders:
                    senders[transaction.sender] = []
                senders[transaction.sender].append(transaction)

            for sender, transactions in senders.items():
                senders_balance = blockchain.get_balance(sender)
                total_amount = 0
                for transaction in transactions:
                    total_amount += (transaction.amount + transaction.fee)
                if total_amount > senders_balance:
                    return False

        return True

    def serialize(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def deserialize(data):
        data_dict = json.loads(data)
        return Block(data_dict["block_number"],
                     data_dict["prev_hash"],
                     data_dict["data"],
                     data_dict["validator"],
                     data_dict["signature"])


class Blockchain:
    def __init__(self, chain=None):
        if not chain:
            self.chain = [Block()]
        else:
            self.chain = chain

    def __str__(self):
        ret_str = ""
        for block in self.chain:
            ret_str += f"{block}\n"
        return ret_str[:-1]

    def next_block(self, data=None, validator="", signature=""):
        """creates the next block in the chain, add it to the chain, and return it"""
        if not data:
            data = []
        block_number = self.chain[-1].block_number + 1
        prev_hash = self.chain[-1].hash_block().hexdigest()
        block = Block(block_number, prev_hash, data, validator, signature)
        return block

    def replace_chain_if_more_reliable(self, new_chain):
        """replaces the chain if the new chain is longer and valid"""
        if len(new_chain) > len(self.chain) and \
                self.is_chain_valid(new_chain):
            self.chain = new_chain
            return True
        return False

    def is_valid(self):
        """checks if the chain is valid and returns the result"""
        return self.is_chain_valid(self.chain)

    @staticmethod
    def is_chain_valid(chain):
        """checks if a chain is valid and returns the result"""
        if str(chain[0]) != str(Block()):
            return False
        for i in range(1, len(chain)):
            curr_block = chain[i]
            prev_block = chain[i - 1]
            if (curr_block.prev_hash != prev_block.hash_block().hexdigest()) \
                    or not curr_block.is_valid() \
                    or curr_block == Block():
                return False
        return True

    def get_balance(self, public_key):
        ret_value = 0
        for block in self.chain:
            for transaction_json in block.data:
                transaction = Transaction.deserialize(transaction_json)
                if block.validator == public_key:
                    ret_value += transaction.fee

                if transaction.receiver == public_key:
                    ret_value += transaction.amount

                if transaction.sender == public_key:
                    ret_value -= (transaction.amount + transaction.fee)

        return ret_value

    def get_validators(self):
        """returns a dict of all addresses that have staked coins and how many coins they have staked"""
        validators = {}
        for block in self.chain:
            for transaction_json in block.data:
                transaction = Transaction.deserialize(transaction_json)
                if transaction.receiver == STAKE_ADDRESS:
                    if not (transaction.sender in validators):
                        validators[transaction.sender] = transaction.amount
                    else:
                        validators[transaction.sender] += transaction.amount

        return validators

    def serialize(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def deserialize(data):
        data_dict = json.loads(data)
        return Blockchain(data_dict["chain"])


class Wallet:
    def __init__(self, secret_key=None, blockchain=None):
        if not secret_key:  # secret key = private key
            self.secret_key = ECC.generate(curve=CURVE_FOR_KEYS)
        else:
            self.secret_key = secret_key

        self.public_key = self.secret_key.public_key()

        if not blockchain:
            self.blockchain = Blockchain()
        else:
            self.blockchain = blockchain

        self.transaction_pool = []
        self.proposed_blocks = []

    def hash_for_block_signature(self, block):
        return sha256_hash(block.block_number, block.prev_hash, block.data, self.public_key)

    def add_transaction_to_pool(self, transaction):
        if Transaction.deserialize(transaction).is_valid():
            self.transaction_pool.append(transaction)
            return True
        return False

    def make_transaction(self, receiver, amount):
        """gets a receiver (exported public key) and an amount (float), returns a transaction (Transaction)"""
        sender = self.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)
        fee = TRANSACTION_FEE
        transaction_hash = sha256_hash(sender, receiver, amount, fee)
        signer = DSS.new(self.secret_key, STANDARD_FOR_SIGNATURES)
        signature = str(signer.sign(transaction_hash))
        self.add_transaction_to_pool(Transaction(receiver, sender, amount, signature, fee).serialize())
        return self.transaction_pool[-1]

    def make_block(self):
        new_block = self.blockchain.next_block(self.transaction_pool[:MAX_TRANSACTIONS_IN_BLOCK])
        block_hash = sha256_hash(new_block.block_number, new_block.prev_hash, new_block.data)  # for signature, not really the block's hash
        signer = DSS.new(self.secret_key, STANDARD_FOR_SIGNATURES)
        signature = str(signer.sign(block_hash))
        new_block.validator = self.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)
        new_block.signature = signature
        self.transaction_pool = []
        self.add_proposed_block(new_block)
        return new_block

    def add_proposed_block(self, block):
        self.proposed_blocks.append(block)

    def add_a_block_to_chain(self):
        for block in self.proposed_blocks:
            if block.is_valid(self.blockchain) and block.validator == self.get_leader():
                self.blockchain.chain.append(block)
                self.transaction_pool = []
                self.proposed_blocks = []
                return True

        return False

    def get_leader(self):
        validators = self.blockchain.get_validators()
        block_hash_values = [int(block.hash_block().hexdigest(), 16) for block in self.proposed_blocks]
        validator_values = {}
        for value, block in zip(block_hash_values, self.proposed_blocks):
            validator_values[block.validator] = value * sqrt(validators[block.validator])

        if validator_values:
            return max(validator_values, key=(lambda key: validator_values[key]))
        else:
            return None

    def get_balance(self):
        return self.blockchain.get_balance(self.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT))

    def __str__(self):
        return f"secret_key: {self.secret_key}"\
             + f"public_key: {self.public_key}"\
             + f"blockchain: {self.blockchain}"


def main():
    pass


if __name__ == "__main__":
    main()
