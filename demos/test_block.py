from meetcoin import Block
import unittest

class Test_block(unittest.TestCase):
    def test_block_hash(self):
        self.assertEqual(Block().hash_block(), "b019ef27cd471a869b318760e442ab43e8053663ab1c18399baa58f73de19576")

        block = Block("2021-01-11 12:51:28.883485", Block().hash_block(), "test data", None, None)
        self.assertEqual(block.hash_block(), "87fe3e578725a6b8fa5aa0d7e865046592758711c6e3fb807b47adacd14167fa")

if __name__ == "__main__":
    unittest.main()