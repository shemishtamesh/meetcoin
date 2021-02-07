from Crypto.Hash import SHA256  # Secure Hash Algorithm (of size) 256 (bits)
from Crypto.PublicKey import ECC  # Eliptic Curve Cryptography
from Crypto.Signature import DSS  # Digital Stardard Signature
import uuid  # Universally Uniqe IDentifier
import re  # for regex


class Constants:
    CURVE_FOR_KEYS = 'NIST P-256'
    STANDARD_FOR_SIGNATURES = 'fips-186-3'
    STAKE_ADDRESS = "STAKE_ADDRESS"
    TRANSACTION_FEE = 1
    EXPORT_IMPORT_KEY_FORMAT = 'PEM'


def sha256_hash(*args):
    """return a sha256 hash of a concatenation of the input input"""
    str_rep = ""
    for arg in args:
        str_rep += str(arg)
    return SHA256.new(str_rep.encode()).hexdigest()


class Transaction:
    def __init__(self,
                 receiver,
                 sender,
                 amount,
                 signature,
                 id=str(uuid.uuid4())):
        self.id = id
        self.signature = signature  # signature of the wallet that looses money from the transaction
        self.sender = sender # sender's wallet's public key
        self.receiver = receiver # receiver's wallet's public key
        self.amount = amount
        self.fee = Constants.TRANSACTION_FEE

    def is_valid(self, blockchain):
        """returns true iff the transaction is valid"""
        # check signature against sender and rest of transaction:
        hash_of_transaction = self.hash_transaction()
        verifier = DSS.new(ECC.import_key(self.sender), Constants.STANDARD_FOR_SIGNATURES)
        try:
            verifier.verify(hash_of_transaction, eval(self.signature))
        except ValueError:
            return False

        # check if the amount can be sent by sender:
        if blockchain.get_balance(self.sender) < self.amount:
            return False

        # check if the id is valid:
        regex_for_uuids = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
        if not re.match(regex_for_uuids, str(self.id)):
            return False

        # check if the receiver and sender are valid (if it's a point on the elliptic curve):
        # is receiver valid:
        if self.receiver != Constants.STAKE_ADDRESS:
            receiver_key = ECC.import_key(self.receiver)
            p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
            b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
            a = -3
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

        if self.receiver == Constants.STAKE_ADDRESS and self.amount <= 0: # check if valid for stake transaction:
            return False

        # check if fee is valid:
        if int(self.fee) != Constants.TRANSACTION_FEE:
            return False

        return True

    def __str__(self):
        return f"id: {self.id}\n" \
               + f"signature: {self.signature}\n" \
               + f"sender: {self.sender}\n" \
               + f"receiver: {self.receiver}\n" \
               + f"amount: {self.amount}\n" \
               + f"fee: {self.fee}\n"

    def hash_transaction(self):
        return sha256_hash(self.id, self.sender, self.receiver, self.amount, self.fee)


class Block:
    def __init__(self,
                 number="0",
                 prev_hash="",
                 data="",
                 validator="",
                 signature=""):
        self.block_number = number
        self.prev_hash = prev_hash
        self.data = data
        self.validator = validator
        self.signature = signature

    def __str__(self):
        return f"created at: {self.block_number}\n" \
               + f"previous hash: {self.prev_hash}\n" \
               + f"current hash: {self.hash_block()}\n" \
               + f"data: {self.data}\n" \
               + f"validator: {self.validator}\n" \
               + f"signature: {self.signature}\n"

    def hash_block(self):
        """returns the hash of the block"""
        return sha256_hash(self.block_number, self.prev_hash, self.data, self.validator, self.signature)

    def is_valid(self):
        pass #TODO: impliment this


class Blockchain:
    def __init__(self):
        self.chain = [Block()]

    def __str__(self):
        ret_str = ""
        for indx, block in enumerate(self.chain):
            ret_str += f"block number: {indx}\n{block}\n"
        return ret_str[:-1]

    def next_block(self, data):
        """creates the next block in the chain, add it to the chain, and return it"""
        block_number = str(int(self.chain[-1].block_number) + 1)
        prev_hash = self.chain[-1].hash_block()
        block = Block(block_number, prev_hash, data)
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
            if curr_block.prev_hash != prev_block.hash_block():
                return False
        return True

    def get_balance(self, public_key):
        ret_value = 0
        for block in self.chain:
            for transaction in block.data:
                if transaction.receiver != Constants.STAKE_ADDRESS:
                    if block.validator == public_key:
                        ret_value += transaction.fee

                    if transaction.receiver == public_key:
                        ret_value += (transaction.amount + transaction.fee)

                if transaction.sender == public_key:
                    ret_value -= (transaction.amount + transaction.fee)

        return ret_value

    def get_validators(self):
        """returns a dict of all addresses that have coins staked and how many coins they have staked"""
        validators = {}
        for block in self.chain:
            for transaction in block.data:
                if transaction.receiver == Constants.STAKE_ADDRESS:
                    if not (transaction.sender in validators):
                        validators[transaction.sender] = transaction.amount
                    else:
                        validators[transaction.sender] += transaction.amount

        return validators

    def get_leader(self):
        validators = self.get_validators()
        return max(validators.items(), key=(lambda key: validators[key])) #TODO: change this to a better ellection system


class Wallet:
    def __init__(self, secret_key=ECC.generate(curve=Constants.CURVE_FOR_KEYS)):
        self.secret_key = secret_key # secret key = private key
        self.public_key = self.secret_key.public_key()
        self.blockchain = Blockchain()
        self.transaction_pool = []

    def hash_for_block_signature(self, block):
        return sha256_hash(block.block_number, block.prev_hash, block.data, self.public_key)

    def make_transaction(self, receiver, amount):
        """gets a receiver (exported public key) and an amount (int), returns a transaction (Transaction)"""
        id = str(uuid.uuid4())
        sender = self.public_key.export_key(format=Constants.EXPORT_IMPORT_KEY_FORMAT)
        fee = str(Constants.TRANSACTION_FEE)
        transaction_hash = sha256_hash(id, sender, receiver, amount, fee)
        signer = DSS.new(self.secret_key, Constants.STANDARD_FOR_SIGNATURES)
        signature = str(signer.sign(transaction_hash))
        return Transaction(receiver, sender, amount, signature, id)

    def __str__(self):
        return f"secret_key: {self.secret_key}"\
              +f"public_key: {self.public_key}"\
              +f"blockchain: {self.blockchain}"


def main():
    pass

if __name__ == "__main__":
    main()
