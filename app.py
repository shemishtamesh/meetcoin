# for networking:
from networking import *
from select import select

# for meetcoin system
from meetcoin import *

# for files
from random import randint
import os

# for gui:
from ui_meetcoin import Ui_MainWindow
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

# for exception handling:
import sys

if OS_NAME == 'Linux':
    SLASH_SIGN = '/'
elif OS_NAME == 'Windows':
    SLASH_SIGN = '\\'


class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        # creating the window:
        super(MainWindow, self).__init__(*args, **kwargs)

        # set up the ui:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # setting up title bar and grips to resize the window:
        self.ui.exit_button.clicked.connect(lambda: self.close())
        self.is_maximized = False  # for maximizing and resizing the window using the maximize button
        self.last_click_on_empty_space = None
        self.ui.maximize_button.clicked.connect(self.maximize_resize_window)
        self.ui.minimize_button.clicked.connect(lambda: self.showMinimized())
        self.ui.title_bar.mouseMoveEvent = self.drag_window
        self.setWindowFlag(qtc.Qt.FramelessWindowHint)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.gripSize = 8
        self.grips = []
        for i in range(4):
            grip = qtw.QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            grip.setStyleSheet("background-color: rgba(0,0,0,0)")
            self.grips.append(grip)

        # setting up wallet:
        self.ui.create_wallet_btn.clicked.connect(self.create_wallet)
        self.ui.recreate_wallet_btn.clicked.connect(self.recreate_wallet)
        self.ui.enter_wallet_btn.clicked.connect(self.enter_wallet)
        self.wallet = None

        # setting up networking:
        self.peer = Peer()

        # setting up navigation buttons:
        self.ui.my_wallet_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.my_wallet_pg))  # navigation to my wallet page
        self.ui.blockchain_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.blockchain_pg))  # navigation to blockchain page
        self.ui.go_to_changing_wallet_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.change_wallet_pg))  # navigation to change wallet page
        self.ui.help_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.help_pg))  # navigation to help page
        self.ui.menu_frame.hide()  # hide until a wallet is created/recreated

        # setting up contacts list file:
        try:
            with open(f"data{SLASH_SIGN}contacts list.json", "r+") as contact_list_file:
                if type(json.load(contact_list_file)) != dict:
                    contact_list_file.seek(0)
                    json.dump({}, contact_list_file)
        except (IOError, json.decoder.JSONDecodeError):
            with open(f"data{SLASH_SIGN}contacts list.json", "w") as contact_list_file:
                contact_list_file.write("{}")
        with open(f"data{SLASH_SIGN}contacts list.json", "r") as contact_list_file:
            contact_list_dict = json.load(contact_list_file)
            for contact_name in contact_list_dict:
                self.add_contact(contact_name, contact_list_dict[contact_name])

        # setting up adding removing and editing contacts:
        self.ui.add_contact_btn.clicked.connect(self.add_contact)
        self.ui.update_contact_btn.clicked.connect(self.update_contact)
        self.ui.delete_contact_btn.clicked.connect(self.remove_selected_contact)

        # networking related:
        self.ui.send_transaction_btn.clicked.connect(self.send_transaction)

        # set up password change:
        self.ui.change_password_btn.clicked.connect(self.update_password)

        # set up is_validator boolean:
        self.is_validator = False

        # set up initial load screen:
        self.ui.stop_waiting_button.clicked.connect(self.stop_waiting_for_blocks)
        self.finished_collecting_missing_blocks = False

    # window functionality:
    def maximize_resize_window(self):
        if not self.is_maximized:
            self.showMaximized()
            self.is_maximized = True
        else:
            self.showNormal()
            self.is_maximized = False

    def drag_window(self, event):
        # if maximized, resize
        if self.is_maximized:
            x_window_center = self.normalGeometry().width() // 2
            self.showNormal()
            self.is_maximized = False
            self.move(qtc.QPoint(event.globalPos().x() - x_window_center, 0))

        # if left mouse click is clicked, move the window
        if event.buttons() == qtc.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.last_click_on_empty_space)
            self.last_click_on_empty_space = event.globalPos()
            event.accept()

    # wallet creation and entering:
    def create_wallet(self):
        self.wallet = Wallet()
        password = self.ui.choosing_password_in.text()
        with open(f"data{SLASH_SIGN}private key.txt", 'w') as secret_key_file:
            if password:
                secret_key_file.write(self.wallet.secret_key.export_key(format=SECRET_KEY_FORMAT,
                                                                        passphrase=password,
                                                                        protection=SECRET_KEY_PROTECTION))
            else:
                secret_key_file.write(self.wallet.secret_key.export_key(format=SECRET_KEY_FORMAT,
                                                                        protection=SECRET_KEY_PROTECTION))

        self.request_missing_blocks()

    def enter_wallet(self):
        password = self.ui.already_have_wallet_password_in.text()
        try:
            with open(f"data{SLASH_SIGN}private key.txt", 'r') as secret_key_file:
                protected_secret_key = secret_key_file.read()
                self.wallet = Wallet(ECC.import_key(protected_secret_key, passphrase=password))
            self.request_missing_blocks()
        except ValueError:
            qtw.QMessageBox.critical(None, 'Fail', "password doesn't match the protected private key that was provided.")
        except IndexError:
            qtw.QMessageBox.critical(None, 'Fail', "there is no wallet on this device.")

    def recreate_wallet(self):
        password = self.ui.recreate_wallet_password.text()
        protected_secret_key = self.ui.recreate_wallet_private_key.text()
        try:
            self.wallet = Wallet(ECC.import_key(protected_secret_key, passphrase=password))
            with open(f"data{SLASH_SIGN}private key.txt", 'w') as secret_key_file:
                secret_key_file.write(protected_secret_key)
            self.request_missing_blocks()
        except ValueError:
            qtw.QMessageBox.critical(None, 'Fail', "password doesn't match the protected private key that was provided.")

    def finish_entering_wallet(self):
        self.ui.menu_frame.show()  # show the navigation menu after a wallet is created
        self.ui.stackedWidget.setCurrentWidget(self.ui.my_wallet_pg)  # go to "my wallet" page
        self.ui.public_key_lbl.setText(self.wallet.public_key.export_key(format=PUBLIC_KEY_FORMAT))
        self.create_blockchain_file()
        self.ui.current_balance_lbl.setText(str(self.wallet.get_balance()))
        with open(f"data{SLASH_SIGN}blockchain.json", "r") as blockchain_file:
            self.put_json_chain_on_tree(blockchain_file)

        if self.wallet.public_key.export_key(format=PUBLIC_KEY_FORMAT) in self.wallet.blockchain.get_validators():
            self.is_validator = True

        self.handle_blocks()  # TODO: maybe use multithreading/processing for this, but probably because multithreading would probably not reduce time and multiprocessing wouldn't work because of memmory
        self.constant_receive()

    # blockchain file:
    def create_blockchain_file(self):
        try:
            with open(f"data{SLASH_SIGN}blockchain.json", "r+") as blockchain_file:
                if type(json.load(blockchain_file)) != dict:
                    blockchain_file.seek(0)
                    json.dump(self.wallet.blockchain.serialize(), blockchain_file, indent=4)
        except (IOError, json.decoder.JSONDecodeError):
            with open(f"data{SLASH_SIGN}blockchain.json", "w") as blockchain_file:
                blockchain_file.write(self.wallet.blockchain.serialize())
        with open(f"data{SLASH_SIGN}blockchain.json", "r") as blockchain_file:
            self.wallet.blockchain = Blockchain.deserialize(blockchain_file.read())

    def update_blockchain_file(self):
        with open(f"data{SLASH_SIGN}blockchain.json", "w") as blockchain_file:
            blockchain_file.write(self.wallet.blockchain.serialize())
        self.ui.current_balance_lbl.setText(str(self.wallet.get_balance()))

    # trees:
    def add_transaction_to_pool_tree(self, json_transaction):
        rand_int = randint(0, 999999)
        with open(f"data{SLASH_SIGN}transaction{rand_int}.json", "w") as json_file:
            json_file.write("{\"transaction\":")  # adding a "transaction wrapper for display
            json_file.write(json_transaction.serialize())
            json_file.write("}")  # adding a "transaction wrapper for display
        with open(f"data{SLASH_SIGN}transaction{rand_int}.json", "r") as json_file:
            tree = json_file_to_xml_string(json_file)
        self.put_xml_tree_on_tree(tree, self.ui.transaction_pool_tree)
        os.remove(f"data{SLASH_SIGN}transaction{rand_int}.json")

    def add_block_to_proposed_tree(self, json_block):
        rand_int = randint(0, 999999)
        with open(f"data{SLASH_SIGN}block{rand_int}.json", "w") as json_file:
            json_file.write("{\"block\":")  # adding a "block wrapper for display
            json_file.write(json_block.serialize())
            json_file.write("}")  # adding a "block wrapper for display
        with open(f"data{SLASH_SIGN}block{rand_int}.json", "r") as json_file:
            tree = json_file_to_xml_string(json_file)
        self.put_xml_tree_on_tree(tree, self.ui.proposed_blocks_tree)
        os.remove(f"data{SLASH_SIGN}block{rand_int}.json")

    def put_xml_tree_on_tree(self, xml_tree, tree_widget):
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

    def put_json_chain_on_tree(self, json_file):
        tree = json_file_to_xml_string(json_file)

        # rename generic "item" names to more informative names in xml
        for tree_child in tree:
            tree_child.tag = "block"
            for block_child in tree_child:
                if block_child.tag == "data":
                    for data_child in block_child:
                        data_child.tag = "transaction"

        self.ui.blockchain_tree.clear()
        self.put_xml_tree_on_tree(tree, self.ui.blockchain_tree)

    # contact list editing:
    def add_contact(self, name=None, public_key=None):
        if not name:
            name = self.ui.new_contacts_name_in.text()
        if not public_key:
            public_key = self.ui.new_contacts_public_key_in.text()
            if public_key != STAKE_ADDRESS:
                try:
                    ECC.import_key(public_key)
                except ValueError:
                    qtw.QMessageBox.critical(None, 'Fail', "public key is incorrect")
                    return False

        # add the new contact to the contacts list file:
        new_contact = {name: public_key}
        with open(f"data{SLASH_SIGN}contacts list.json", "r+") as contact_list_file:
            data = json.load(contact_list_file)
            if name not in data:
                data.update(new_contact, )
                contact_list_file.seek(0)
                json.dump(data, contact_list_file)

        self.update_contacts_list_on_gui()
        return True

    def update_contact(self):
        selected_contacts = self.ui.contacts_list.selectedItems()
        if selected_contacts:
            self.remove_selected_contact(selected_contacts)
            self.add_contact(self.ui.updated_contacts_name_in.text(), self.ui.updated_contacts_public_key_in.text())

    def remove_selected_contact(self, selected_contacts=None):
        if not selected_contacts:
            selected_contacts = self.ui.contacts_list.selectedItems()
        for contact in selected_contacts:
            with open(f"data{SLASH_SIGN}contacts list.json", "r+") as contact_list_file:
                data = json.load(contact_list_file)
                contacts_name = contact.text().split(": ")[0]
                data.pop(contacts_name)
                contact_list_file.truncate(0)
                contact_list_file.seek(0)
                json.dump(data, contact_list_file)

        self.update_contacts_list_on_gui()

    def update_contacts_list_on_gui(self):
        with open(f"data{SLASH_SIGN}contacts list.json", "r") as contact_list_file:
            data = json.load(contact_list_file)
            self.ui.contacts_list.clear()
            for contact_name in data:
                self.ui.contacts_list.addItem(f"{contact_name}: {data[contact_name]}")

    # updating password:
    def update_password(self):
        old_password = self.ui.old_password_in.text()
        try:
            with open(f"data{SLASH_SIGN}private key.txt", 'r') as secret_key_file:
                protected_secret_key = secret_key_file.read()
                ECC.import_key(protected_secret_key, passphrase=old_password)
        except ValueError:
            qtw.QMessageBox.critical(None, 'Fail', "old password doesn't match the protected private key that was provided.")
            return

        new_password = self.ui.new_password_in.text()
        with open(f"data{SLASH_SIGN}private key.txt", 'w') as secret_key_file:
            secret_key_file.write(self.wallet.secret_key.export_key(format=SECRET_KEY_FORMAT,
                                                                    passphrase=new_password,
                                                                    protection=SECRET_KEY_PROTECTION))

        qtw.QMessageBox.information(None, 'Success', "successfully changed the password.")

    # block handling:
    def handle_blocks(self):
        new_block = self.wallet.make_block()
        if self.is_validator and new_block:
            self.peer.udp_send(new_block)
            self.ui.transaction_pool_tree.clear()

        if self.wallet.add_a_block_to_chain():
            # checking if validator now:
            if self.wallet.public_key.export_key(format=PUBLIC_KEY_FORMAT) in self.wallet.blockchain.get_validators():
                self.is_validator = True

            # clearing trees:
            self.ui.transaction_pool_tree.clear()
            self.ui.proposed_blocks_tree.clear()

            # update_particle blockchain file and blockchain tree:
            self.update_blockchain_file()
            with open(f"data{SLASH_SIGN}blockchain.json", "r") as blockchain_file:
                self.put_json_chain_on_tree(blockchain_file)

        qtc.QTimer.singleShot(10000, self.handle_blocks)

    # networking:
    def send_transaction(self):
        password = self.ui.transaction_password_in.text()
        with open(f"data{SLASH_SIGN}private key.txt", 'r') as secret_key_file:
            protected_secret_key = secret_key_file.read()
            try:
                Wallet(ECC.import_key(protected_secret_key, passphrase=password))
            except ValueError:
                qtw.QMessageBox.critical(None, 'Fail', "password doesn't match the protected private key that was provided.")
                return

            receiver = self.ui.contacts_list.currentItem()
            try:
                receiver = receiver.text().split(": ")[-1]
            except AttributeError:
                qtw.QMessageBox.critical(None, 'Fail', "no contact selected.")
                return

            try:
                amount = float(self.ui.amount_text_incer.text())
            except ValueError:
                qtw.QMessageBox.critical(None, 'Fail', "amount must be a number.")
                return
            if amount > 0:
                transaction = self.wallet.make_transaction(receiver, amount)
                if transaction:
                    self.peer.udp_send(transaction)
                    qtw.QMessageBox.information(None, 'Success', "successfully sent the transaction.")
                else:
                    qtw.QMessageBox.critical(None, 'Fail', "you don't have enough meetcoins to complete this transaction.")
            else:
                qtw.QMessageBox.critical(None, 'Fail', "amount must be more than zero.")

    def constant_receive(self):
        if self.peer.tcp_client:
            rlist, wlist, xlist = select([self.peer.udp_receiver, self.peer.tcp_client], [], [], 0.01)
        else:
            rlist, wlist, xlist = select([self.peer.udp_receiver], [], [], 0.01)
        for sock in rlist:
            if sock == self.peer.udp_receiver:
                received_message = self.peer.udp_receive()
                self.received_from_udp_socket(received_message)

            if sock == self.peer.tcp_client:
                received_message = sock.recv(RECV_SIZE).decode()
                print(f"tcp_client_received: {received_message}")
                if received_message[len("position "):] == "position ":
                    block_position_from_end_of_chain_to_send = int(received_message[:len("position ")])
                    self.send_a_missing_block(block_position_from_end_of_chain_to_send)
                elif received_message[len("finished"):] == "finished":
                    self.close_clinet()

        qtc.QTimer.singleShot(100, self.constant_receive)

    def received_from_udp_socket(self, message):
        if type(message) == Transaction:
            self.wallet.add_transaction_to_pool(message)
            self.add_transaction_to_pool_tree(message)
        elif type(message) == Block:
            self.wallet.add_proposed_block(message)
            self.add_block_to_proposed_tree(message)
        elif type(message) == str and message[:len("connected")] == "connected":
            self.send_a_missing_block(self.wallet.blockchain.chain[-1].block_number)
        else:
            print(message)

    def send_a_missing_block(self, position):
        block_to_send = [block for block in self.wallet.blockchain.chain if block.block_number == position][0]
        self.peer.tcp_client_send(block_to_send)

    def request_missing_blocks(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.updating_blockchain_pg)
        self.collect_blocks()

    def collect_blocks(self):
        missing_blocks_by_peer = {}
        self.peer.request_update_connection()
        finished_so_far = 0
        tcp_connected_peers = []

        def collect_blocks_networking():
            nonlocal finished_so_far
            nonlocal tcp_connected_peers

            rlist, wlist, xlist = [], [], []
            if len(tcp_connected_peers) <= NUMBER_OF_CONNECTED_CLIENTS:
                rlist, wlist, xlist = select([self.peer.tcp_server] + tcp_connected_peers, [], [], 0.01)
            for sock in rlist:
                if sock == self.peer.tcp_server:
                    (new_sock, address) = self.peer.tcp_server.accept()
                    print(f"tcp connected to {address}")
                    tcp_connected_peers.append(new_sock)

                elif sock in tcp_connected_peers:
                    received_message = sock.recv(RECV_SIZE).decode()
                    if received_message[:len("Block: ")] == "Block: ":
                        received_message = received_message[len("Block: "):]
                        print(f"tcp_client_received: Block")
                        received_block = Block.deserialize(received_message)
                        if received_block.block_number not in [block.block_number for block in self.wallet.blockchain.chain]:  # if block number isn't alewady in chain
                            if sock not in missing_blocks_by_peer:
                                missing_blocks_by_peer[sock] = []
                            missing_blocks_by_peer[sock].append(received_block)
                            sock.send(f"position {received_block.block_number - 1}".encode('utf-8'))
                        else:
                            sock.send("finished".encode('utf-8'))
                            if finished_so_far >= NUMBER_OF_CONNECTED_CLIENTS:
                                self.finished_collecting_missing_blocks = True
                            else:
                                finished_so_far += 1

                    elif received_message == '':
                        tcp_connected_peers.remove(sock)

                    else:
                        print(received_message)

            if not self.finished_collecting_missing_blocks:
                qtc.QTimer.singleShot(1000, collect_blocks_networking)
            else:
                tcp_connected_peers = []
                self.peer.close_server()
                self.handle_collected_blocks(list(missing_blocks_by_peer.values()))
                self.finish_entering_wallet()

        collect_blocks_networking()

    def stop_waiting_for_blocks(self):
        self.finished_collecting_missing_blocks = True

    def handle_collected_blocks(self, collected_blocks_lists_list):
        valid_collected_blocks_lists_list = []
        for collected_blocks_lists in collected_blocks_lists_list:
            for collected_block in collected_blocks_lists:
                if collected_block.is_valid():
                    valid_collected_blocks_lists_list.append(collected_blocks_lists)

        valid_collected_blocks_lists_list_tuples = []
        for valid_collected_blocks_lists in valid_collected_blocks_lists_list:
            valid_collected_blocks_list_tuples = []
            for valid_collected_block in valid_collected_blocks_lists:
                valid_collected_blocks_list_tuples.append((valid_collected_block.block_number, valid_collected_block.hash_block))
            valid_collected_blocks_lists_list_tuples.append(valid_collected_blocks_list_tuples)

        correct_valid_collected_blocks_list_tuples = most_frequent(valid_collected_blocks_lists_list_tuples)
        index_of_correct_valid_collected_blocks_list = valid_collected_blocks_lists_list_tuples.index(correct_valid_collected_blocks_list_tuples)
        correct_valid_collected_blocks_list = valid_collected_blocks_lists_list[index_of_correct_valid_collected_blocks_list]

        for correct_valid_collected_block in correct_valid_collected_blocks_list:
            self.wallet.add_proposed_block(correct_valid_collected_block)
            if not self.wallet.add_a_block_to_chain(correct_valid_collected_block):
                self.request_missing_blocks()


    # on events:
    def mousePressEvent(self, event):
        self.last_click_on_empty_space = event.globalPos()

    def resizeEvent(self, event):
        qtw.QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        # top left grip doesn't need to be moved
        # top right
        self.grips[1].move(rect.right() - self.gripSize, 0)
        # bottom right
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grips[3].move(0, rect.bottom() - self.gripSize)


if __name__ == "__main__":
    # for handling exceptions:
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook

    # for running the app:
    app = qtw.QApplication([])
    widget = MainWindow()
    widget.show()
    app.exec_()
