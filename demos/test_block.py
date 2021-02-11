from meetcoin import Block
import unittest

class Test_block(unittest.TestCase):
    def test_block_hash(self):
        self.assertEqual(Block().hash_block().hexdigest(), "13a30b73bd8229b0a82cfebfaec68ead5bc8654e78b7c9732104c62a7a5fe3c0")

        block = Block("4", Block().hash_block().hexdigest(), "test data", "", "")
        self.assertEqual(block.hash_block().hexdigest(), "0645c6617e413dec26de6c762d6da97fa226ec390f527b07700b036a8839a344")

if __name__ == "__main__":
    unittest.main()