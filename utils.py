from Crypto.Hash import SHA256  # Secure Hash Algorithm (of size) 256 (bits)


CURVE_FOR_KEYS = 'NIST P-256'
STANDARD_FOR_SIGNATURES = 'fips-186-3'
STAKE_ADDRESS = "STAKE_ADDRESS"
TRANSACTION_FEE = 1.0
EXPORT_IMPORT_KEY_FORMAT = 'PEM'

# for ICO:
NUMBER_OF_COINS = 10.0
INITIAL_COIN_HOLDER = '''-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE9zp6h9JFTqBbagWASuXhTVX/3mUQ
dlRFkB112qFWgA2IimLJ5v9cIF+NwW086j+NDBYk1l5aoVnGtAnT4UjkTw==
-----END PUBLIC KEY-----'''
INITIAL_COIN_HOLDER_SECRET = '''-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgkchMEe4X6NC8pWgS
K1F4yX0KsgZFAYwr9vZmc8aKrauhRANCAAT3OnqH0kVOoFtqBYBK5eFNVf/eZRB2
VEWQHXXaoVaADYiKYsnm/1wgX43BbTzqP40MFiTWXlqhWca0CdPhSORP
-----END PRIVATE KEY-----'''
INITIAL_STAKE_TRANSACTION = r'''{"signature": "b\"\\x18\\xcaAr0\\xa9/\\xb8\\x95\\x81[\\xea\\xcc\\xb5\\xed\\x91\\x8c\\xd1<\\xe8]v\\xe2o\\xc7'\\x9d\\x88\\r\\x10\\xbc|\\x05\\xc0^\\x81o\\xe7\\xe6\\x8f\\x9b\\xd6%\\x96)$-L\\x93\\x90\\xcd\\xd8d6\\xe6\\xa2\\xad\\xc9\\xdc\\xcf&3F\\xc7\"", "sender": "-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE9zp6h9JFTqBbagWASuXhTVX/3mUQ\ndlRFkB112qFWgA2IimLJ5v9cIF+NwW086j+NDBYk1l5aoVnGtAnT4UjkTw==\n-----END PUBLIC KEY-----", "receiver": "STAKE_ADDRESS", "amount": 1, "fee": 1}'''
# initial_coin_holder = Wallet(ECC.import_key(INITIAL_COIN_HOLDER_SECRET), Blockchain([]))  #            /\
# second_transaction = initial_coin_holder.make_transaction(STAKE_ADDRESS, 1).serialize()  # makes this /  \

# vars of NIST P-256 elliptic curve:
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
a = -3

def sha256_hash(*args):
    """return a sha256 hash of a concatenation of the input input"""
    str_rep = ""
    for arg in args:
        str_rep += str(arg)

    return SHA256.new(str_rep.encode())