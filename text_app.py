from networking import *
from meetcoin import *
from select import select
try:  # determine if using windows or not, if not assume linux
    from msvcrt import getch  # only works in windows
    def getch_decode():
        return getch().decode()
    from msvcrt import kbhit
    operating_system = "windows"
    enter_key = '\r'
except (ImportError, ModuleNotFoundError) as e:
    from getch import getch  # does not work in linux
    def getch_decode():
        return getch()
    from KBHit import KBHit
    kbhit = KBHit().kbhit
    operating_system = "linux"
    enter_key = '\n'

class App:
    def __init__(self, secret_key=None, blockchain=None):
        self.wallet = Wallet(secret_key, blockchain)
        self.peer = Peer()

        self.tcp_connected_peers = []

    def receive_from_udp_socket(self, received_message):
        if type(received_message) == Transaction:
            self.wallet.add_transaction_to_pool(received_message)

        if type(received_message) == Block:
            self.wallet.add_proposed_block(received_message)

        if received_message == "request_update_connection":
            pass

        print("received:")
        print(received_message)

    def send_transaction(self):
        address = input("address to send coins to: ")
        amount = input(f"amount of coins to send (including {TRANSACTION_FEE} for the validator fee: ")
        transaction = self.wallet.make_transaction(address, amount)
        self.peer.udp_send(transaction)

    def send_block(self):
        self.peer.udp_send(self.wallet.make_block())

    def request_update_connection(self):
        self.peer.request_update_connection()

    def run(self):
        command = ""
        print(f"your public key is: {self.wallet.public_key.export_key(format=PUBLIC_KEY_FORMAT)}")
        while True:
            rlist, wlist, xlist = select([self.peer.udp_receiver, self.peer.tcp_sock], [], [], 0.01)
            for sock in rlist:
                received_message = self.peer.udp_receive()
                if sock == self.peer.udp_receiver:
                    self.receive_from_udp_socket(received_message)

                if sock == self.peer.tcp_sock:
                    (new_sock, address) = self.peer.tcp_sock.accept()
                    print(f"tcp connected to {address}")
                    self.tcp_connected_peers.append(new_sock)

            if kbhit():
                try:
                    key_pressed = getch_decode()
                except (UnicodeDecodeError, AttributeError):
                    key_pressed = ""
                if key_pressed == enter_key:
                    print()
                    if command == "t":
                        self.send_transaction()
                        print("sent transaction")
                    if command == "b":
                        self.send_block()
                    if command == "r":
                        self.request_update_connection()

                    if command == "pt":
                        print(self.wallet.transaction_pool)
                    if command == "pb":
                        print(self.wallet.proposed_blocks)

                    command = ""
                else:
                    print(key_pressed, end="", flush=True)
                    command += key_pressed


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
