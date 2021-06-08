# for meetcoin:
from Crypto.Hash import SHA256  # Secure Hash Algorithm (of size) 256 (bits)

# for xml for tree widget on gui:
from json2xml.utils import readfromstring
from json2xml import json2xml
import xml.etree.ElementTree as et

# for determining os
import platform

# for .ini file
import configparser

# for trees
from PyQt5 import QtWidgets as qtw

# for password check:
import re

config = configparser.ConfigParser()
try:
    config.read('configure.ini')

    # for cryptography:
    CURVE_FOR_KEYS = config['cryptography']['CURVE_FOR_KEYS']
    STANDARD_FOR_SIGNATURES = config['cryptography']['STANDARD_FOR_SIGNATURES']
    STAKE_ADDRESS = config['cryptography']['STAKE_ADDRESS']
    TRANSACTION_FEE = float(config['cryptography']['TRANSACTION_FEE'])
    PUBLIC_KEY_FORMAT = config['cryptography']['PUBLIC_KEY_FORMAT']
    SECRET_KEY_FORMAT = config['cryptography']['SECRET_KEY_FORMAT']
    SECRET_KEY_PROTECTION = config['cryptography']['SECRET_KEY_PROTECTION']
    NUM_OF_TRANSACTIONS_IN_BLOCK = int(config['cryptography']['NUM_OF_TRANSACTIONS_IN_BLOCK'])

    # for ICH:
    NUMBER_OF_COINS = float(config['ICH']['NUMBER_OF_COINS'])
    INITIAL_COIN_HOLDER = config['ICH']['INITIAL_COIN_HOLDER']
    INITIAL_STAKE_TRANSACTION = config['ICH']['INITIAL_STAKE_TRANSACTION']

    # vars of NIST P-256 elliptic curve:
    p = int(config['fips-186-3_constants']['p'])
    b = int(config['fips-186-3_constants']['b'])
    a = int(config['fips-186-3_constants']['a'])

    # for networking:
    RECV_SIZE = eval(config['networking']['RECV_SIZE'])
    UDP_PORT = int(config['networking']['UDP_PORT'])
    TCP_PORT = int(config['networking']['TCP_PORT'])
    NUMBER_OF_CONNECTED_CLIENTS = int(config['networking']['NUMBER_OF_CONNECTED_CLIENTS'])

except configparser.ParsingError:
    print("could not read from ini")
    # for cryptography:
    CURVE_FOR_KEYS = 'P-256'
    STANDARD_FOR_SIGNATURES = 'fips-186-3'
    STAKE_ADDRESS = "STAKE_ADDRESS"
    TRANSACTION_FEE = 1.0
    PUBLIC_KEY_FORMAT = 'PEM'
    SECRET_KEY_FORMAT = 'PEM'
    SECRET_KEY_PROTECTION = 'PBKDF2WithHMAC-SHA1AndAES128-CBC'
    NUM_OF_TRANSACTIONS_IN_BLOCK = 1

    # for ICH:
    NUMBER_OF_COINS = 10.0  # must be over 2
    INITIAL_COIN_HOLDER = '''-----BEGIN PUBLIC KEY-----
    MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE9zp6h9JFTqBbagWASuXhTVX/3mUQ
    dlRFkB112qFWgA2IimLJ5v9cIF+NwW086j+NDBYk1l5aoVnGtAnT4UjkTw==
    -----END PUBLIC KEY-----'''
    INITIAL_STAKE_TRANSACTION = r'''{"signature": "b\"\\x18\\xcaAr0\\xa9/\\xb8\\x95\\x81[\\xea\\xcc\\xb5\\xed\\x91\\x8c\\xd1<\\xe8]v\\xe2o\\xc7'\\x9d\\x88\\r\\x10\\xbc|\\x05\\xc0^\\x81o\\xe7\\xe6\\x8f\\x9b\\xd6%\\x96)$-L\\x93\\x90\\xcd\\xd8d6\\xe6\\xa2\\xad\\xc9\\xdc\\xcf&3F\\xc7\"", "sender": "-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE9zp6h9JFTqBbagWASuXhTVX/3mUQ\ndlRFkB112qFWgA2IimLJ5v9cIF+NwW086j+NDBYk1l5aoVnGtAnT4UjkTw==\n-----END PUBLIC KEY-----", "receiver": "STAKE_ADDRESS", "amount": 1, "fee": 1}'''
    # initial_coin_holder = Wallet(ECC.import_key(INITIAL_COIN_HOLDER_SECRET), Blockchain([]))  #            /\
    # second_transaction = initial_coin_holder.make_transaction(STAKE_ADDRESS, 1).serialize()  # makes this /  \

    # vars of NIST P-256 elliptic curve:
    p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
    b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
    a = -3

    # for networking:
    RECV_SIZE = 1024 * 10
    UDP_PORT = 50000
    TCP_PORT = 50001
    NUMBER_OF_CONNECTED_CLIENTS = 2

# check what os is this:
OS_NAME = platform.system()


def sha256_hash(*args):
    """return a sha256 hash of a concatenation of the input input"""
    str_rep = ""
    for arg in args:
        str_rep += str(arg)

    return SHA256.new(str_rep.encode())


def json_file_to_xml_string(json_file):
    """takes a json file and returns an xml string"""
    json_string = json_file.read()

    data = readfromstring(json_string)
    xml_string = json2xml.Json2xml(data).to_xml()

    return et.fromstring(xml_string)[0]  # [0] because json2xml adds an unneeded wrapper


def most_frequent(lst):
    """takes a list and returns the most frequent element in it"""
    counter = 0
    num = lst[0]

    for i in lst:
        curr_frequency = lst.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i

    return num


def put_xml_tree_on_tree(xml_tree, tree_widget):
    """puts an xml tree on a Qtree"""
    top_level_item = qtw.QTreeWidgetItem([xml_tree.tag])
    tree_widget.addTopLevelItem(top_level_item)

    def display_tree(parent, tree_to_display):
        for child in tree_to_display:
            branch = qtw.QTreeWidgetItem([child.tag])
            parent.addChild(branch)

            display_tree(branch, child)

        if parent.text is not None:
            if not tree_to_display.text:
                parent.addChild(qtw.QTreeWidgetItem(["None"]))
            else:
                parent.addChild(qtw.QTreeWidgetItem([tree_to_display.text]))

    display_tree(top_level_item, xml_tree)


def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"\W", password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }
