from meetcoin import Block
import unittest

class Test_block(unittest.TestCase):
    def test_block_hash(self):
        self.assertEqual(Block().hash_block(), "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9")

        block = Block("4", Block().hash_block(), "test data", "", "")
        self.assertEqual(block.hash_block(), "c0f1337a3f9dc5cdb79845f3720ca120639fc5c4e1b0bb69b01ba592c9916f22")

if __name__ == "__main__":
    unittest.main()