from projcoin import Block
from projcoin import Blockchain
#from projcoin import sha256_hash
def main():
    print(f"####################### creating a chian ########################\n")
    blockchain = Blockchain()
    print(blockchain)

    print(f"####################### adding a block ########################\n")
    blockchain.next_block(["tansaction 1", "tansaction 2", "tansaction 3"])
    blockchain.chain[1].time = "2021-01-04 10:22:04.425252" # hard coding the timestamp to make the demo deterministic
    print(blockchain)

    print(f"####################### failing to replace the chain ########################\n")
    blockchain1 = Blockchain()
    blockchain.replace_chain(blockchain1.chain)
    print(blockchain)

    print(f"####################### replacing the chain ########################\n")
    blockchain1.next_block(["a", "b", "c", "d"])
    blockchain1.next_block(["1", "2", "3", "4"])
    blockchain1.next_block(["1", "2", "3", "4"])
    blockchain.replace_chain(blockchain1.chain)
    print(blockchain)

if __name__ == "__main__":
    main()