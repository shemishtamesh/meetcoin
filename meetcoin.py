from meetcoin_utils import *  # utils & constants
from Crypto.PublicKey import ECC  # Elliptic Curve Cryptography
from Crypto.Signature import DSS  # Digital Standard Signature
import json  # for serialization
from math import sqrt  # for choosing leader


class Transaction:
    """represents a transaction (used for all transactions), the default is the initial transaction"""
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
        if not (self.serialize() == Transaction().serialize() and self in blockchain.chain[0].data):  # unless initial transaction for initial coin offering
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

            # check if fee is valid:
            if float(self.fee) != TRANSACTION_FEE:
                return False

            # check if amount is more than 0, or different than zero in case of retrieving stake:
            if (self.receiver != STAKE_ADDRESS and float(self.amount) <= 0) or (self.receiver == STAKE_ADDRESS and float(self.amount) == 0):
                return False

            # check if the amount can be sent by sender:
            if blockchain.get_balance(self.sender) < (float(self.amount) + float(self.fee)):
                return False

            if (self.receiver == STAKE_ADDRESS) and (self.amount < 0) and (blockchain.get_validators()[self.sender] < -self.amount):
                return False

            # check if transaction is a duplicate of an existing transaction:
            for block in blockchain.chain:
                for transaction in block.data:
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
        """returns a json string of the transaction, can be used for sending."""
        return str(json.dumps(self.__dict__, indent=4))

    @staticmethod
    def deserialize(data):
        """takes a serialized (json string of a) transaction and returns a transaction object"""
        if type(data) == str:
            data_dict = json.loads(data)
        elif type(data) == dict:
            data_dict = data
        return Transaction(data_dict["receiver"],
                           data_dict["sender"],
                           data_dict["amount"],
                           data_dict["signature"],
                           data_dict["fee"])

    def hash_transaction(self):
        """returns a hash of the sender, receiver, amount, and fee"""
        return sha256_hash(self.sender, self.receiver, self.amount, self.fee)


class Block:
    """represents a block and used to store transaction and to separate them, the default block is the genesis block"""
    def __init__(self,
                 number=0,
                 prev_hash="",
                 data="",
                 validator="",
                 signature=""):
        self.block_number = number
        self.prev_hash = prev_hash
        if data == "":
            first_transaction = Transaction()
            second_transaction = Transaction.deserialize(INITIAL_STAKE_TRANSACTION)
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
        """returns true iff the block is valid"""
        if self != Block():  # allow the genesis block
            # check transactions:
            for transaction in self.data:
                if not transaction.is_valid(blockchain):
                    return False

            # check signature:
            serialized_data = []
            for transaction in self.data:
                serialized_data.append(transaction.serialize())  # serialize data so that it won't be an object, but a string
            hash_of_block_content = sha256_hash(self.block_number, self.prev_hash, serialized_data)
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
            for transaction in self.data:
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
        """returns a (json) string representation of the block"""
        block_dict = dict(self.__dict__)
        transaction_list = []
        for transaction in block_dict["data"]:
            transaction_list.append(transaction.__dict__)
        block_dict["data"] = transaction_list
        return str(json.dumps(block_dict, indent=4))

    @staticmethod
    def deserialize(data):
        """takes a json representation of a block and returns the represented block"""
        if type(data) == str:
            data_dict = json.loads(data)
        else:
            data_dict = data
        transaction_list = []
        for transaction in data_dict["data"]:
            transaction_list.append(Transaction.deserialize(transaction))
        return Block(data_dict["block_number"],
                     data_dict["prev_hash"],
                     transaction_list,
                     data_dict["validator"],
                     data_dict["signature"])


class Blockchain:
    """represents a blockchain, used to store blocks and to derive information from them"""
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

    # TODO: maybe delete this
    # def replace_chain_if_more_reliable(self, new_chain):
    #     # to do: update_particle this to something secure, longer isn't necessarily more secure in pos, probably get more than one chain compare them and choose the best
    #     """replaces the chain if the new chain is longer and valid"""
    #     if len(new_chain) > len(self.chain) and \
    #             self.is_chain_valid(new_chain):
    #         self.chain = new_chain
    #         return True
    #     return False

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
        """gets a public_key and returns the balance associated with it"""
        ret_value = 0
        formatted_public_key = public_key.replace('\n', '\\n')
        for block in self.chain:
            for transaction in block.data:
                if block.validator == public_key:
                    ret_value += transaction.fee

                if transaction.receiver == formatted_public_key:
                    ret_value += transaction.amount

                if transaction.sender == public_key:
                    ret_value -= (transaction.amount + transaction.fee)

        return ret_value

    def get_validators(self):
        """returns a dict of all addresses that have staked coins and how many coins they have staked"""
        validators = {}
        for block in self.chain:
            for transaction in block.data:
                if transaction.receiver == STAKE_ADDRESS:
                    if not (transaction.sender in validators):
                        validators[transaction.sender] = transaction.amount
                    else:
                        validators[transaction.sender] += transaction.amount

        return validators

    def serialize(self):
        """returns a json representation of the blockchain"""
        blockchain_dict = dict(self.__dict__)
        block_list = []
        for block in blockchain_dict["chain"]:
            block_dict = dict(block.__dict__)
            transaction_list = []
            for transaction in block_dict["data"]:
                transaction_list.append(transaction.__dict__)
            block_dict["data"] = transaction_list
            block_list.append(block_dict)
        blockchain_dict["chain"] = block_list
        return str(json.dumps(blockchain_dict, indent=4))

    @staticmethod
    def deserialize(data):
        """takes a json representation of a blockchain (str) and returns a blockchain (Blockchain)"""
        data_dict = json.loads(data)
        block_list = []
        for block in data_dict["chain"]:
            block_list.append(Block.deserialize(block))
        return Blockchain(block_list)


class Wallet:
    """used to store a blockchain, and to interact with it"""
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
        """returns a hash used for signing blocks"""
        return sha256_hash(block.block_number, block.prev_hash, block.data, self.public_key)

    def add_transaction_to_pool(self, transaction):
        """adds a transaction to the transaction pool if it's valid"""
        if transaction.is_valid(self.blockchain):
            self.transaction_pool.append(transaction)
            return True
        return False

    def make_transaction(self, receiver, amount):
        """gets a receiver (exported public key) and an amount (float), returns a transaction (Transaction)"""
        if (receiver == STAKE_ADDRESS) and (amount < 0)\
                and (self.blockchain.get_validators()[self.public_key.export_key(format=PUBLIC_KEY_FORMAT)] < -amount):
            return False

        if self.get_balance() >= amount + TRANSACTION_FEE:
            sender = self.public_key.export_key(format=PUBLIC_KEY_FORMAT)
            fee = TRANSACTION_FEE
            transaction_hash = sha256_hash(sender, receiver, amount, fee)
            signer = DSS.new(self.secret_key, STANDARD_FOR_SIGNATURES)
            signature = str(signer.sign(transaction_hash))
            return Transaction(receiver, sender, amount, signature, fee)
        else:
            return False

    def make_block(self):
        """makes a block, empties the transaction pool, and appends the proposed blocks list with the new block"""
        if len(self.transaction_pool) >= NUM_OF_TRANSACTIONS_IN_BLOCK:
            new_block = self.blockchain.next_block(self.transaction_pool[:NUM_OF_TRANSACTIONS_IN_BLOCK])
            serialized_data = []
            for transaction in new_block.data:
                serialized_data.append(transaction.serialize())  # serialize data so that it won't be an object, but a string
            block_hash = sha256_hash(new_block.block_number, new_block.prev_hash, serialized_data)  # for signature, not really the block's hash
            signer = DSS.new(self.secret_key, STANDARD_FOR_SIGNATURES)
            signature = str(signer.sign(block_hash))
            new_block.validator = self.public_key.export_key(format=PUBLIC_KEY_FORMAT)
            new_block.signature = signature
            self.transaction_pool = []
            return new_block

    def add_proposed_block(self, block):
        """adds a block the the proposed blocks list"""
        self.proposed_blocks.append(block)

    def add_a_block_to_chain(self):
        """adds a block from the proposed blocks to the blockchain iff the block is valid and its validator is the current leader, also empties the transaction pool and the proposed blocks list"""
        # if len(self.proposed_blocks) > 10:
        current_leader = self.get_leader()
        for block in self.proposed_blocks:
            if block.is_valid(self.blockchain) and block.validator == current_leader:
                self.blockchain.chain.append(block)
                self.transaction_pool = []
                self.proposed_blocks = []
                return True

        return False

    def get_leader(self):
        """returns the current leader"""
        validators = self.blockchain.get_validators()
        block_hash_values = [int(block.hash_block().hexdigest(), 16) for block in self.proposed_blocks]
        validator_values = {}
        for block_hash_value, block in zip(block_hash_values, self.proposed_blocks):
            if block.validator in validators:
                validator_values[block.validator] = block_hash_value * sqrt(validators[block.validator])
            else:
                validator_values[block.validator] = 0

        if validator_values:
            leader = max(validator_values, key=(lambda key: validator_values[key]))
            return leader
        else:
            return None

    def get_balance(self):
        """returns the balance of self"""
        return self.blockchain.get_balance(self.public_key.export_key(format=PUBLIC_KEY_FORMAT))

    def __str__(self):
        return f"secret_key: {self.secret_key}"\
             + f"public_key: {self.public_key}"\
             + f"blockchain: {self.blockchain}"


def main():
    pass

if __name__ == "__main__":
    main()
