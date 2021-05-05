from meetcoin import Transaction, Block
from meetcoin_utils import *
from socket import *


# TODO: request chain update by broadcasting a request and then tcp connect to first x peers to get blocks from them, find incentive for people to actually send the blocks.


class Peer:
    def __init__(self):
        self.udp_sender = socket(AF_INET, SOCK_DGRAM)
        self.udp_sender.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.udp_receiver = socket(AF_INET, SOCK_DGRAM)
        self.udp_receiver.bind(('', UDP_PORT))

        self.tcp_sock = socket(AF_INET, SOCK_STREAM)
        self.tcp_sock.bind(("0.0.0.0", TCP_PORT))
        self.tcp_sock.listen(5)

    # sending:
    def udp_send_raw(self, message):
        self.udp_sender.sendto(message.encode('utf-8'), ('255.255.255.255', UDP_PORT))

    def udp_send(self, to_send):
        message = ""
        if type(to_send) == Transaction:
            message = "transaction:" + to_send.serialize()
        elif type(to_send) == Block:
            message = "block:" + to_send.serialize()
        else:
            message = to_send

        self.udp_send_raw(message)

    def request_update_connection(self):
        self.udp_send("request_update_connection")

    # receiving
    def udp_receive_raw(self):
        return self.udp_receiver.recvfrom(RECV_SIZE)

    def udp_receive(self):
        (received_message, sender_address) = self.udp_receive_raw()
        received_message = received_message.decode('utf-8')
        if received_message[:len("transaction:")] == "transaction:":
            return Transaction.deserialize(received_message[len("transaction:"):])

        if received_message[:len("block:")] == "block:":
            return Block.deserialize(received_message[len("block:"):])

        if received_message == "request_update_connection":
            self.tcp_sock.connect(sender_address)


if __name__ == "__main__":
    Peer()
