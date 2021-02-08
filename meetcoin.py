from Crypto.Hash import SHA256  # Secure Hash Algorithm (of size) 256 (bits)
from Crypto.PublicKey import ECC  # Eliptic Curve Cryptography
from Crypto.Signature import DSS  # Digital Stardard Signature
import uuid  # Universally Uniqe IDentifier
import re  # for regex
from utils import *  # utils & constants
import json


class Transaction:
    def __init__(self,
                 receiver=INITIAL_COIN_HOLDER,
                 sender=None,
                 amount=NUMBER_OF_COINS,
                 signature=None,
                 transaction_id=INITIAL_TRANSACTION_ID):
        self.transaction_id = transaction_id
        self.signature = signature  # signature of the wallet that looses money from the transaction
        self.sender = sender  # sender's wallet's public key
        self.receiver = receiver  # receiver's wallet's public key
        self.amount = amount
        self.fee = TRANSACTION_FEE

    def is_valid(self, blockchain):
        """returns true iff the transaction is valid"""
        if self != Transaction() and self in blockchain.chain[0]:  # unless initial transaction for initial coin offering
            # check signature against sender and rest of transaction:
            hash_of_transaction = self.hash_transaction()
            verifier = DSS.new(ECC.import_key(self.sender), STANDARD_FOR_SIGNATURES)
            try:
                verifier.verify(hash_of_transaction, eval(self.signature))
            except ValueError:
                return False

            # check if the id is valid:
            regex_for_uuids = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
            if not re.match(regex_for_uuids, str(self.transaction_id)):
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
            if int(self.fee) != TRANSACTION_FEE:
                return False

            # check if the amount can be sent by sender:
            if blockchain.get_balance(self.sender) < (self.amount + self.fee):
                return False

        return True

    def __str__(self):
        return f"id: {self.transaction_id}\n" \
               + f"signature: {self.signature}\n" \
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
                    data_dict["transaction_id"])

    def hash_transaction(self):
        return sha256_hash(self.transaction_id, self.sender, self.receiver, self.amount, self.fee)


class Block:
    def __init__(self,
                 number="0",
                 prev_hash=None,
                 data=None,
                 validator=None,
                 signature=None):
        self.block_number = number
        self.prev_hash = prev_hash
        if not data:
            self.data = [Transaction()]
        else:
            self.data = data
        self.validator = validator
        self.signature = signature

    def __str__(self):
        return f"created at: {self.block_number}\n" \
               + f"previous hash: {self.prev_hash}\n" \
               + f"current hash: {self.hash_block().hexdigest()}\n" \
               + f"data: {self.data}\n" \
               + f"validator: {self.validator}\n" \
               + f"signature: {self.signature}\n"

    def hash_block(self):
        """returns the hash of the block"""
        return sha256_hash(self.block_number, self.prev_hash, self.data, self.validator, self.signature)

    def is_valid(self):
        if self != Block():
            for transaction in self.data:
                if not transaction.is_valid():
                    return False

            hash_of_block_content = sha256_hash(self.block_number, self.prev_hash, self.data)
            verifier = DSS.new(ECC.import_key(self.validator), STANDARD_FOR_SIGNATURES)
            try:
                verifier.verify(hash_of_block_content, eval(self.signature))
            except ValueError:
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
        for indx, block in enumerate(self.chain):
            ret_str += f"block number: {indx}\n{block}\n"
        return ret_str[:-1]

    def next_block(self, data=None, validator=None, signature=None):
        """creates the next block in the chain, add it to the chain, and return it"""
        block_number = str(int(self.chain[-1].block_number) + 1)
        prev_hash = self.chain[-1].hash_block().hexdigest()
        block = Block(block_number, prev_hash, data, validator, signature)
        self.chain.append(block)
        return block

    def replace_chain_if_more_reliable(self, new_chain):
        """replaces the chain if the new chain is longer and valid"""
        if len(new_chain) > len(self.chain) and \
                self.is_chain_valid(new_chain):
            self.chain = new_chain
            return True
        else:
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
            for transaction in block.data:
                if transaction.receiver != STAKE_ADDRESS:
                    if block.validator == public_key:
                        ret_value += transaction.fee

                    if transaction.receiver == public_key:
                        ret_value += transaction.amount

                if transaction.sender == public_key:
                    ret_value -= (transaction.amount + transaction.fee)

        return ret_value

    def get_validators(self):
        """returns a dict of all addresses that have coins staked and how many coins they have staked"""
        validators = {}
        for block in self.chain:
            for transaction in block.data:
                if transaction.receiver == STAKE_ADDRESS:
                    if not (transaction.sender in validators):
                        validators[transaction.sender] = transaction.amount
                    else:
                        validators[transaction.sender] += transaction.amount

        return validators

    def get_leader(self):
        validators = self.get_validators()
        return max(validators.items(), key=(lambda key: validators[key])) #TODO: change this to a better ellection system

    def serialize(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def deserialize(data):
        data_dict = json.loads(data)
        return Blockchain(data_dict["chain"])



class Wallet:
    def __init__(self, secret_key=ECC.generate(curve=CURVE_FOR_KEYS)):
        self.secret_key = secret_key # secret key = private key
        self.public_key = self.secret_key.public_key()
        self.blockchain = Blockchain()
        self.transaction_pool = []

    def hash_for_block_signature(self, block):
        return sha256_hash(block.block_number, block.prev_hash, block.data, self.public_key)

    def add_transaction_to_pool(self, transaction):
        self.transaction_pool.append(transaction)

    def make_transaction(self, receiver, amount):
        """gets a receiver (exported public key) and an amount (int), returns a transaction (Transaction)"""
        transaction_id = str(uuid.uuid4())
        sender = self.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)
        fee = str(TRANSACTION_FEE)
        transaction_hash = sha256_hash(transaction_id, sender, receiver, amount, fee)
        signer = DSS.new(self.secret_key, STANDARD_FOR_SIGNATURES)
        signature = str(signer.sign(transaction_hash))
        self.transaction_pool.append(Transaction(receiver, sender, amount, signature, transaction_id))
        return self.transaction_pool[-1]

    def make_block(self):
        new_block = self.blockchain.next_block(self.transaction_pool)
        block_hash = sha256_hash(new_block.block_number, new_block.prev_hash, new_block.data)
        signer = DSS.new(self.secret_key, STANDARD_FOR_SIGNATURES)
        signature = str(signer.sign(block_hash))
        new_block.validator = self.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)
        new_block.signature = signature
        self.transaction_pool = []
        return new_block

    def add_block(self, block):
        if block.is_valid() and block.validator == self.blockchain.get_leader:
            self.blockchain.chain.append(block)

    def get_balance(self):
        return self.blockchain.get_balance(self.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT))

    def __str__(self):
        return f"secret_key: {self.secret_key}"\
              +f"public_key: {self.public_key}"\
              +f"blockchain: {self.blockchain}"


def main():
    pass


if __name__ == "__main__":
    main()
