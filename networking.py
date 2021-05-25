from meetcoin import Transaction, Block
from meetcoin_utils import *
from socket import *
# TODO: request chain update_particle by broadcasting a request and then tcp connect to first x peers to get blocks from them, find incentive for people to actually send the blocks.


if OS_NAME == "Linux":
    import os
    ifconfig_output = os.popen('ifconfig')
    output = ifconfig_output.read()
    relevant_section = output[output.find('enp0s3: '):output.find('  netmask')]
    host_ip = relevant_section[relevant_section.find('inet ') + len('inet '):]

elif OS_NAME == "Windows":
    host_ip = gethostbyname(gethostname())


class Peer:
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
        self.udp_sender.sendto(message.encode('utf-8'), ('255.255.255.255', UDP_PORT))

    def udp_send(self, to_send):
        if type(to_send) == Transaction:
            print("udp sending: " + "transaction:" + str(type(to_send)))
            self.udp_send_raw("transaction:" + to_send.serialize())
        elif type(to_send) == Block:
            print("udp sending: " + "block:" + str(type(to_send)))
            self.udp_send_raw("udp sending: " + "block:" + to_send.serialize())
        else:
            print("udp sending: " + to_send)
            self.udp_send_raw(to_send)

    def tcp_client_send(self, to_send):
        if type(to_send) == Block:
            print("tcp_client sending: " + str(type(to_send)))
            self.tcp_client.send(("Block: " + to_send.serialize()).encode('utf-8'))
        else:
            print("tcp_client sending: " + str(type(to_send)))
            self.tcp_client.send(to_send.encode('utf-8'))

    def request_update_connection(self):
        self.tcp_server = socket(AF_INET, SOCK_STREAM)
        self.tcp_server.bind(("0.0.0.0", TCP_PORT))
        self.tcp_server.listen(NUMBER_OF_CONNECTED_CLIENTS)
        self.udp_send("request_update_connection")

    def close_server(self):
        self.tcp_server.close()
        self.tcp_server = None

    def close_client(self):
        self.tcp_client.close()
        self.tcp_client = None

    # receiving
    def udp_receive_raw(self):
        return self.udp_receiver.recvfrom(RECV_SIZE)

    def udp_receive(self):
        (received_message, sender_address) = self.udp_receive_raw()
        received_message = received_message.decode('utf-8')
        print(f"received_message: {received_message}, sender_address: {sender_address}")
        if received_message[:len("transaction:")] == "transaction:":
            return Transaction.deserialize(received_message[len("transaction:"):])

        if received_message[:len("block:")] == "block:":
            return Block.deserialize(received_message[len("block:"):])

        if received_message == "request_update_connection" and sender_address[0] != host_ip:
            try:
                self.tcp_client = socket(AF_INET, SOCK_STREAM)
                self.tcp_client.connect((sender_address[0], TCP_PORT))
                return f"connected to {(sender_address[0], TCP_PORT)}"
            except OSError:
                return "can't connect"

if __name__ == "__main__":
    Peer()
