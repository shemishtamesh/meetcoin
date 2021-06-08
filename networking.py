from meetcoin_logic import Transaction, Block
from meetcoin_utils import *
from socket import *


if OS_NAME == "Linux":
    import netifaces as ni
    host_ip = ni.ifaddresses('enp0s3')[ni.AF_INET][0]['addr']

elif OS_NAME == "Windows":
    host_ip = gethostbyname(gethostname())


class Peer:
    """used to handle networking, both udp and tcp"""
    def __init__(self):
        # udp sockets:
        self.udp_sender = socket(AF_INET, SOCK_DGRAM)
        self.udp_sender.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.udp_receiver = socket(AF_INET, SOCK_DGRAM)
        self.udp_receiver.bind(('', UDP_PORT))

        # tcp sockets:
        self.tcp_server = None

        self.tcp_client = None

    # sending:
    def udp_send_raw(self, message):
        """broadcasts a udp message"""
        self.udp_sender.sendto(message.encode('utf-8'), ('255.255.255.255', UDP_PORT))

    def udp_send(self, to_send):
        """formats and broadcasts a udp message"""
        if type(to_send) == Transaction:
            self.udp_send_raw("transaction:" + to_send.serialize())
        elif type(to_send) == Block:
            self.udp_send_raw("block:" + to_send.serialize())
        else:
            self.udp_send_raw(to_send)

    def tcp_client_send(self, to_send):
        """sends a tcp message to a server (a new peer that's asking for missing blocks)"""
        if type(to_send) == Block:
            self.tcp_client.send(("Block: " + to_send.serialize()).encode('utf-8'))
        else:
            self.tcp_client.send(to_send.encode('utf-8'))

    def request_update_connection(self):
        """opens the tcp_server socket, broadcasts a request for connection"""
        self.tcp_server = socket(AF_INET, SOCK_STREAM)
        if OS_NAME == 'Linux':
            self.tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcp_server.bind(("0.0.0.0", TCP_PORT))
        self.tcp_server.listen(NUMBER_OF_CONNECTED_CLIENTS)
        self.udp_send("request_update_connection")

    def close_server(self):
        """closes and deletes the tcp_server socket"""
        if self.tcp_server:
            self.tcp_server.close()
            self.tcp_server = None

    def close_client(self):
        """closes and deletes the tcp_client socket"""
        if self.tcp_client:
            self.tcp_client.close()
            self.tcp_client = None

    # receiving
    def udp_receive_raw(self):
        """receives a message from the udp_receiver port and returns it"""
        return self.udp_receiver.recvfrom(RECV_SIZE)

    def udp_receive(self):
        """receives a udp message, interprets it, and returns the relevant information, also tcp connects if necessary"""
        (received_message, sender_address) = self.udp_receive_raw()
        received_message = received_message.decode('utf-8')
        if received_message[:len("transaction:")] == "transaction:":
            return Transaction.deserialize(received_message[len("transaction:"):])

        if received_message[:len("block:")] == "block:":
            return Block.deserialize(received_message[len("block:"):])

        if received_message == "request_update_connection" and sender_address[0] != host_ip:
            try:
                self.close_client()
                self.tcp_client = socket(AF_INET, SOCK_STREAM)
                self.tcp_client.connect((sender_address[0], TCP_PORT))
                return f"connected to {(sender_address[0], TCP_PORT)}"
            except OSError:
                self.tcp_client = None
                return "can't connect"


if __name__ == "__main__":
    pass
