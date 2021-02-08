from meetcoin import Block
import unittest

class Test_block(unittest.TestCase):
    def test_block_hash(self):
        self.assertEqual(Block().hash_block().hexdigest(), "35412b6d682496bdbc3ea1f60e3e1a29275b9069206a1dcf010a75c02a9b3b35")

        block = Block("4", Block().hash_block().hexdigest(), "test data", "", "")
        self.assertEqual(block.hash_block().hexdigest(), "8ea556abc1e68ba94d772bd71da761ebbd31c01743c18d82339ea0ce3b2cd1a0")

if __name__ == "__main__":
    unittest.main()