from Crypto.Hash import SHA256  # Secure Hash Algorithm (of size) 256 (bits)


CURVE_FOR_KEYS = 'NIST P-256'
STANDARD_FOR_SIGNATURES = 'fips-186-3'
STAKE_ADDRESS = "STAKE_ADDRESS"
TRANSACTION_FEE = 1
EXPORT_IMPORT_KEY_FORMAT = 'PEM'

# for ICO:
INITIAL_TRANSACTION_ID = "3d8f027a-8c78-454b-93df-75523384feaf"
NUMBER_OF_COINS = 10
INITIAL_COIN_HOLDER = '''-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE9zp6h9JFTqBbagWASuXhTVX/3mUQ
dlRFkB112qFWgA2IimLJ5v9cIF+NwW086j+NDBYk1l5aoVnGtAnT4UjkTw==
-----END PUBLIC KEY-----'''
# initial coin holder secret key:
# -----BEGIN PRIVATE KEY-----
# MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgkchMEe4X6NC8pWgS
# K1F4yX0KsgZFAYwr9vZmc8aKrauhRANCAAT3OnqH0kVOoFtqBYBK5eFNVf/eZRB2
# VEWQHXXaoVaADYiKYsnm/1wgX43BbTzqP40MFiTWXlqhWca0CdPhSORP
# -----END PRIVATE KEY-----

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
