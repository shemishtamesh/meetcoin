# for meetcoin:
from Crypto.Hash import SHA256  # Secure Hash Algorithm (of size) 256 (bits)

# for xml for tree widget on gui:
from json2xml.utils import readfromstring
from json2xml import json2xml
import xml.etree.ElementTree as et

# for determining os
import platform


CURVE_FOR_KEYS = 'P-256'  # 'NIST P-256'
STANDARD_FOR_SIGNATURES = 'fips-186-3'
STAKE_ADDRESS = "STAKE_ADDRESS"
TRANSACTION_FEE = 1.0
PUBLIC_KEY_FORMAT = 'PEM'#'OpenSSH'
SECRET_KEY_FORMAT = 'PEM'
SECRET_KEY_PROTECTION = 'PBKDF2WithHMAC-SHA1AndAES128-CBC'
NUM_OF_TRANSACTIONS_IN_BLOCK = 1

# for ICO:
NUMBER_OF_COINS = 10.0  # must be over 2
INITIAL_COIN_HOLDER = '''-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE9zp6h9JFTqBbagWASuXhTVX/3mUQ\ndlRFkB112qFWgA2IimLJ5v9cIF+NwW086j+NDBYk1l5aoVnGtAnT4UjkTw==\n-----END PUBLIC KEY-----'''
INITIAL_COIN_HOLDER_SECRET = r'''-----BEGIN PRIVATE KEY-----
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


# for networking:
RECV_SIZE = 1024 * 10
UDP_PORT = 50000
TCP_PORT = 50001
NUMBER_OF_CONNECTED_CLIENTS = 2


def json_file_to_xml_string(json_file):
    json_string = json_file.read()

    data = readfromstring(json_string)
    xml_string = json2xml.Json2xml(data).to_xml()

    return et.fromstring(xml_string)[0]  # [0] because json2xml adds an unneeded wrapper


OS_NAME = platform.system()

if OS_NAME == 'Linux':
    import socket

    # def get_ip_address():
    #     temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     temp_server.listen(1)
    #
    #     temp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     port = 49152
    #     while True:
    #         try:
    #             temp_client.connect(("127.0.0.1", port))
    #             return temp_server.accept()[0]
    #         except OSError:
    #             port += 1
