from meetcoin import *
from socket import *
from select import select
try:  # determine if using windows or not, if not assume linux
    from msvcrt import getch
    def getch_decode():
        return getch().decode()
    from msvcrt import kbhit
    operating_system = "windows"
    enter_key = '\r'
except (ImportError, ModuleNotFoundError) as e:
    from getch import getch
    def getch_decode():
        return getch()
    from KBHit import KBHit
    kbhit = KBHit().kbhit
    operating_system = "linux"
    enter_key = '\n'

# TODO: request chain update by broadcasting a request and then tcp connect to first x peers to get blocks from them, find incentive for people to actually send the blocks.


class Peer:
    def __init__(self, secret_key=None, blockchain=None):
        self.wallet = Wallet(secret_key, blockchain)

        self.udp_sender = socket(AF_INET, SOCK_DGRAM)
        self.udp_sender.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.udp_receiver = socket(AF_INET, SOCK_DGRAM)
        self.udp_receiver.bind(('', 55555))

        self.tcp_sock = socket(AF_INET, SOCK_STREAM)

        self.contacts = {}

    def send(self, msg):
        # TODO: implement sending big files
        self.udp_sender.sendto(msg.encode('utf-8'), ('255.255.255.255', 55555))

    def receive_raw(self):
        # TODO: implement receiving big files
        return self.udp_receiver.recvfrom(RECV_SIZE)[0].decode('utf-8')

    def receive(self):
        received_message = self.receive_raw()
        if received_message[:len("transaction:")] == "transaction:":
            self.wallet.add_transaction_to_pool(Transaction.deserialize(received_message[len("transaction:"):]))
            print("added transaction")
        if received_message[:len("block:")] == "block:":
            self.wallet.add_proposed_block(Transaction.deserialize(received_message[len("block:"):]))
            print("added block")

    def send_transaction(self, key, amount):
        self.send("transaction:" + self.wallet.make_transaction(key, amount).serialize())

    def send_block(self):
        self.send("block:" + self.wallet.make_block().serialize())

    def run(self):
        """runs only if main() runs"""
        command = ""
        print(f"your public key is: {self.wallet.public_key.export_key(format=PUBLIC_KEY_FORMAT)}")
        while True:
            rlist, wlist, xlist = select([self.udp_receiver], [], [], 0.01)
            if rlist:
                self.receive()
            if kbhit():
                try:
                    key_pressed = getch_decode()
                except (UnicodeDecodeError, AttributeError):
                    key_pressed = ""
                if key_pressed == enter_key:
                    print()
                    if command == "t":
                        address = input("address to send coins to: ")
                        amount = input(f"amount of coins to send (including {TRANSACTION_FEE} for the validator fee: ")
                        self.send_transaction(address, amount)
                    if command == "b":
                        self.send_block()

                    if command == "pt":
                        print(self.wallet.transaction_pool)
                    if command == "pb":
                        print(self.wallet.proposed_blocks)

                    command = ""
                else:
                    print(key_pressed, end="", flush=True)
                    command += key_pressed


def main():
    peer = Peer()
    peer.run()


if __name__ == "__main__":
    main()
