from meetcoin import *
import unittest


class TestWalletInteraction(unittest.TestCase):
    def test_Blockchain_init(self):
        alice = Wallet(ECC.import_key(INITIAL_COIN_HOLDER_SECRET))

        self.assertEqual(alice.get_balance(), NUMBER_OF_COINS - 1)  # -1 because of alice's stake

    def test_coin_transfer_alice_to_bob(self):
        alice = Wallet(ECC.import_key(INITIAL_COIN_HOLDER_SECRET))
        bob = Wallet()

        alice_public = alice.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)
        bob_public = bob.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)

        alice.make_transaction(bob_public, 5)
        new_block = alice.make_block()
        alice.add_a_block_to_chain()
        bob.add_proposed_block(new_block)
        bob.add_a_block_to_chain()

        self.assertEqual(alice.get_balance(), NUMBER_OF_COINS - 1 - 5)  # -1 because of alice's stake
        self.assertEqual(alice.blockchain.get_balance(bob_public), 5)

        self.assertEqual(bob.blockchain.get_balance(alice_public), NUMBER_OF_COINS - 1 - 5)  # -1 because of alice's stake
        self.assertEqual(bob.get_balance(), 5)

    def test_coin_transfer_alice_to_bob_to_charlie(self):
        alice = Wallet(ECC.import_key(INITIAL_COIN_HOLDER_SECRET))
        bob = Wallet()
        charlie = Wallet()

        alice_public = alice.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)
        bob_public = bob.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)
        charlie_public = charlie.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)

        alice.make_transaction(bob_public, 5)
        new_block = alice.make_block()

        bob.add_proposed_block(new_block)
        charlie.add_proposed_block(new_block)

        alice.add_a_block_to_chain()
        bob.add_a_block_to_chain()
        charlie.add_a_block_to_chain()

        new_transaction = bob.make_transaction(charlie_public, 3)
        alice.add_transaction_to_pool(new_transaction)
        new_block = alice.make_block()

        bob.add_proposed_block(new_block)
        charlie.add_proposed_block(new_block)

        alice.add_a_block_to_chain()
        bob.add_a_block_to_chain()
        charlie.add_a_block_to_chain()

        self.assertEqual(alice.get_balance(), NUMBER_OF_COINS - 5)  # NUMBER_OF_COINS - 1 - 5 + 1 (+1 because of fee from bob)
        self.assertEqual(alice.blockchain.get_balance(bob_public), 1)
        self.assertEqual(alice.blockchain.get_balance(charlie_public), 3)

        self.assertEqual(bob.blockchain.get_balance(alice_public), NUMBER_OF_COINS - 5)  # NUMBER_OF_COINS - 1 - 5 + 1 (+1 because of fee from bob)
        self.assertEqual(bob.get_balance(), 1)
        self.assertEqual(alice.blockchain.get_balance(charlie_public), 3)

        self.assertEqual(charlie.blockchain.get_balance(alice_public), NUMBER_OF_COINS - 5)  # NUMBER_OF_COINS - 1 - 5 + 1 (+1 because of fee from bob)
        self.assertEqual(charlie.blockchain.get_balance(bob_public), 1)
        self.assertEqual(charlie.get_balance(), 3)

        #     title networking test
        #
        # note over alice:makes transaction1: amount=5, receiver=bob
        # note over alice:makes block1: transaction1
        # alice->bob:block: transaction1
        # alice->charlie:block1: transaction
        #
        # note over alice:adds block1 to chain
        # note over bob:adds block1 to chain
        # note over charlie:adds block1 to chain
        #
        # note over bob:transaction2: amount=3, receiver=charlie
        # alice->bob:transaction2
        # bob->charlie:transaction2
        #
        # note over alice:makes block2: transaction2
        # alice->bob:block2
        # alice->charlie:block2
        #
        # note over alice:adds block2 to chain
        # note over bob:adds block2 to chain
        # note over charlie:adds block2 to chain

    def test_non_ich_leader_and_multi_transaction_block(self):  # ich = initial coin holder
        alice = Wallet(ECC.import_key(INITIAL_COIN_HOLDER_SECRET))
        bob = Wallet()

        alice_public = alice.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)
        bob_public = bob.public_key.export_key(format=EXPORT_IMPORT_KEY_FORMAT)

        alice.make_transaction(bob_public, 5)
        new_block = alice.make_block()  # alice balance = 4 | bob balance = 5

        bob.add_proposed_block(new_block)

        alice.add_a_block_to_chain()
        bob.add_a_block_to_chain()

        new_transaction_bob_stake = bob.make_transaction(STAKE_ADDRESS, 2)
        alice.make_transaction(bob_public, 2)
        alice.add_transaction_to_pool(new_transaction_bob_stake)
        new_block = alice.make_block()  # alice balance = 3 | bob balance = 4
        bob.add_proposed_block(new_block)
        alice.add_a_block_to_chain()
        bob.add_a_block_to_chain()

        bob.make_transaction(alice_public, 3)
        new_block = bob.make_block()  # alice balance = 6 | bob balance = 1
        alice.add_proposed_block(new_block)

        bob.add_a_block_to_chain()
        alice.add_a_block_to_chain()

        self.assertEqual(alice.get_balance(), NUMBER_OF_COINS - 4)
        self.assertEqual(alice.blockchain.get_balance(bob_public), 1)

        self.assertEqual(bob.blockchain.get_balance(alice_public), NUMBER_OF_COINS - 4)
        self.assertEqual(bob.get_balance(), 1)

if __name__ == "__main__":
    unittest.main()
