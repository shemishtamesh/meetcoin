from meetcoin import Blockchain
from meetcoin import Block
import unittest


class Test_Blockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()

    def test_Blockchain_init(self):
        self.assertEqual(str(self.blockchain.chain[0]), str(Block()))

    def test_replace_chain_fail(self):
        self.blockchain.next_block(["tansaction 1", "tansaction 2", "tansaction 3"])
        self.blockchain.chain[1].time = "2021-01-04 10:22:04.425252"  # hard coding the timestamp to make the demo deterministic
        blockchain1 = Blockchain()
        self.assertEqual(self.blockchain.replace_chain_if_more_reliable(blockchain1.chain), False)

    def test_replace_chain_success(self):
        self.blockchain.next_block(["tansaction 1", "tansaction 2", "tansaction 3"])
        self.blockchain.chain[1].time = "2021-01-04 10:22:04.425252"  # hard coding the timestamp to make the demo deterministic
        blockchain1 = Blockchain()
        blockchain1.next_block(["a", "b", "c", "d"])
        blockchain1.next_block(["1", "2", "3", "4"])
        blockchain1.next_block(["1", "2", "3", "4"])
        self.assertEqual(self.blockchain.replace_chain_if_more_reliable(blockchain1.chain), True)

if __name__ == "__main__":
    unittest.main()