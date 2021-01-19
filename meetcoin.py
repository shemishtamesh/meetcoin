from Crypto.Hash import SHA256  # Secure Hash Algorithm (of size) 256 (bits)
from Crypto.PublicKey import ECC  # Eliptic Curve Cryptography
from Crypto.Signature import DSS  # Digital Stardard Signature
import uuid  # Universally Uniqe IDentifier
import re  # for regex
from datetime import datetime

CURVE_FOR_KEYS = 'NIST P-256'
STANDARD_FOR_SIGNATURES = 'fips-186-3'


def sha256_hash(*args):
    """return a sha256 hash of a concatenation of the input input"""
    str_rep = ""
    for arg in args:
        str_rep += str(arg)
    return SHA256.new(str_rep.encode())


class Transaction:
    def __init__(self,
                 receiver,
                 sender,
                 amount,
                 signature,
                 id=uuid.uuid4(),
                 time=datetime.now()):
        self.id = id
        self.time = time
        self.signature = signature  # signature of the wallet that looses money from the transaction
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = 0

    def is_valid(self):
        """returns true iff the transaction is valid"""
        # check signature against sender and rest of transaction:
        hash_of_transaction = self.hash_transaction()
        verifier = DSS.new(self.sender, STANDARD_FOR_SIGNATURES)
        try:
            verifier.verify(hash_of_transaction, self.signature)
        except ValueError:
            return False

        # check if the amount can be sent by sender: # TODO: implement this, decide on how to get the blockchain
        # get all transactions that include the address from self.blockchain
        # calculate the balance of the address from those transactions

        # check if the id is valid:
        regex_for_uuids = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
        if not re.match(regex_for_uuids, str(self.id)):
            return False

        # check if the receiver is valid:
        p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
        b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
        a = -3
        try:
            x = int(self.receiver.pointQ.x)
            y = int(self.receiver.pointQ.y)
        except AttributeError:
            return False
        if ((y ** 2) - ((x ** 3) - (a * x) + b)) % p == 0:
            return False

        # check if sender address is valid:
        try:
            x = int(self.sender.pointQ.x)
            y = int(self.sender.pointQ.y)
        except AttributeError:
            return False
        if ((y ** 2) - ((x ** 3) - (a * x) + b)) % p == 0:
            return False

        # check if fee is valid:
        pass  # TODO: change this (hadn't decided on a fee system yet)

        return True

    def __str__(self):
        return f"id: {self.id}\n" \
               + f"time: {self.time}\n" \
               + f"signature: {self.signature}\n" \
               + f"sender: {self.sender}\n" \
               + f"reveiver: {self.receiver}\n" \
               + f"amount: {self.amount}\n" \
               + f"fee: {self.fee}\n"

    def hash_transaction(self):
        return sha256_hash(self.id, self.time, self.sender, self.receiver, self.amount, self.fee)


class Block:
    def __init__(self,
                 time="0000-00-00 00:00:00.000000",
                 prev_hash=None,
                 data=[],
                 validator=None,
                 signature=None):
        self.time = time
        self.prev_hash = prev_hash
        self.data = data
        self.validator = validator
        self.signature = signature

    def __str__(self):
        return f"created at: {self.time}\n" \
               + f"previous hash: {self.prev_hash}\n" \
               + f"current hash: {self.hash_block()}\n" \
               + f"data: {self.data}\n" \
               + f"validator: {self.validator}\n" \
               + f"signature: {self.signature}\n"

    def hash_block(self):
        """returns the hash of the block"""
        # return sha256_hash(self.time, self.prev_hash, self.data, self.validator, self.signature)
        return sha256_hash(self.time, self.prev_hash, self.data)

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
        time = str(datetime.now())
        prev_hash = self.chain[-1].hash_block()
        block = Block(time, prev_hash, data)
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


class Wallet:
    def __init__(self, secret_key=ECC.generate(curve=CURVE_FOR_KEYS)):
        self.secret_key = secret_key # secret key = private key
        self.public_key = self.secret_key.public_key()
        self.blockchain = []

    def make_transaction(self, receiver, amount):
        """gets a receiver (public key) and an amount, returns a transaction"""
        id = uuid.uuid4()
        time = datetime.now()
        sender = self.public_key
        fee = 0  # TODO: change this to the decided fee system
        transaction_hash = sha256_hash(id, time, sender, receiver, amount, fee)
        signer = DSS.new(self.secret_key, STANDARD_FOR_SIGNATURES)
        signature = signer.sign(transaction_hash)
        return Transaction(receiver, sender, amount, signature, id, time)

    def __str__(self):
        return f"secret_key: {self.secret_key}"\
              +f"public_key: {self.public_key}"\
              +f"blockchain: {self.blockchain}"



def main():
    w = Wallet()
    print(type(w.make_transaction("a", 0).hash_transaction()))


if __name__ == "__main__":
    main()
