# for networking:
from networking import *
from select import select

# for meetcoin calculations and
from meetcoin import *

# for gui:
from ui_meetcoin import Ui_MainWindow
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


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
        grip_colors = ["rgb(43, 43, 43)", "rgb(43, 43, 43)", "rgb(83, 83, 83)", "rgb(53, 53, 53)"]
        for i in range(4):
            grip = qtw.QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            grip.setStyleSheet(f"background-color:{grip_colors[i]}")
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
            with open("data\\contacts list.json", "r+") as contact_list_file:
                if type(json.load(contact_list_file)) != dict:
                    contact_list_file.seek(0)
                    json.dump({}, contact_list_file)
        except (IOError, json.decoder.JSONDecodeError) as e:
            with open("data\\contacts list.json", "w") as contact_list_file:
                contact_list_file.write("{}")
        with open("data\\contacts list.json", "r") as contact_list_file:
            contact_list_dict = json.load(contact_list_file)
            for contact_name in contact_list_dict:
                self.add_contact(contact_name, contact_list_dict[contact_name])

        # setting up adding removing and editing contacts:
        self.ui.add_contact_btn.clicked.connect(self.add_contact)
        self.ui.update_contact_btn.clicked.connect(self.update_contact)
        self.ui.delete_contact_btn.clicked.connect(self.remove_selected_contact)

        self.ui.send_transaction_btn.clicked.connect(self.send_transaction)

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

    def create_wallet(self):
        self.wallet = Wallet()
        password = self.ui.choosing_password_in.text()
        with open("data\\private key.txt", 'w') as secret_key_file:
            if password:
                secret_key_file.write(self.wallet.secret_key.export_key(format=SECRET_KEY_FORMAT, passphrase=password, protection=SECRET_KEY_PROTECTION))
            else:
                secret_key_file.write(self.wallet.secret_key.export_key(format=SECRET_KEY_FORMAT, protection=SECRET_KEY_PROTECTION))

        self.ui.menu_frame.show()  # show the navigation menu after a wallet is created
        self.ui.stackedWidget.setCurrentWidget(self.ui.my_wallet_pg)
        self.ui.public_key_lbl.setText(self.wallet.public_key.export_key(format=PUBLIC_KEY_FORMAT))

    def enter_wallet(self):
        password = self.ui.already_have_wallet_password_in.text()
        try:
            with open("data\\private key.txt", 'r') as secret_key_file:
                protected_secret_key = secret_key_file.read()
                self.wallet = Wallet(ECC.import_key(protected_secret_key, passphrase=password))
            self.ui.menu_frame.show()  # show the navigation menu after a wallet is created
            self.ui.stackedWidget.setCurrentWidget(self.ui.my_wallet_pg)
            self.ui.public_key_lbl.setText(self.wallet.public_key.export_key(format=PUBLIC_KEY_FORMAT))
        except ValueError:
            qtw.QMessageBox.critical(None, 'Fail', "password doesn't match the protected private key that was provided.")
        except IndexError:
            qtw.QMessageBox.critical(None, 'Fail', "there is no wallet on this device.")

    def recreate_wallet(self):
        password = self.ui.recreate_wallet_password.text()
        protected_secret_key = self.ui.recreate_wallet_private_key.text()
        try:
            self.wallet = Wallet(ECC.import_key(protected_secret_key, passphrase=password))
            with open("data\\private key.txt", 'w') as secret_key_file:
                secret_key_file.write(protected_secret_key)
            self.ui.menu_frame.show()  # show the navigation menu after a wallet is created
            self.ui.stackedWidget.setCurrentWidget(self.ui.my_wallet_pg)
            self.ui.public_key_lbl.setText(self.wallet.public_key.export_key(format=PUBLIC_KEY_FORMAT))
        except ValueError:
            qtw.QMessageBox.critical(None, 'Fail', "password doesn't match the protected private key that was provided.")

    def add_contact(self, name=None, public_key=None):
        if not name:
            name = self.ui.new_contacts_name_in.text()
        if not public_key:
            public_key = self.ui.new_contacts_public_key_in.text()

        # add the new contact to the contacts list file:
        new_contact = {name: public_key}
        with open("data\\contacts list.json", "r+") as contact_list_file:
            data = json.load(contact_list_file)
            if name not in data:
                data.update(new_contact)
                contact_list_file.seek(0)
                json.dump(data, contact_list_file)

        self.update_contacts_list_on_gui()

    def update_contact(self):
        selected_contacts = self.ui.contacts_list.selectedItems()
        if selected_contacts:
            self.remove_selected_contact(selected_contacts)
            self.add_contact(self.ui.updated_contacts_name_in.text(), self.ui.updated_contacts_public_key_in.text())

    def remove_selected_contact(self, selected_contacts=None):
        if not selected_contacts:
            selected_contacts = self.ui.contacts_list.selectedItems()
        for contact in selected_contacts:
            with open("data\\contacts list.json", "r+") as contact_list_file:
                data = json.load(contact_list_file)
                contacts_name = contact.text().split(": ")[0]
                data.pop(contacts_name)
                contact_list_file.truncate(0)
                contact_list_file.seek(0)
                json.dump(data, contact_list_file)

        self.update_contacts_list_on_gui()

    def update_contacts_list_on_gui(self):
        with open("data\\contacts list.json", "r") as contact_list_file:
            data = json.load(contact_list_file)
            self.ui.contacts_list.clear()
            for contact_name in data:
                self.ui.contacts_list.addItem(f"{contact_name}: {data[contact_name]}")

    def send_transaction(self):
        password = self.ui.transaction_password_in.text()
        try:
            with open("data\\private key.txt", 'r') as secret_key_file:
                protected_secret_key = secret_key_file.read()
                self.wallet = Wallet(ECC.import_key(protected_secret_key, passphrase=password))

                receiver = self.ui.contacts_list.currentItem()
                receiver = receiver.text().split(": ")[-1]

                try:
                    amount = self.ui.amount_text_incer.text()
                except ValueError:
                    qtw.QMessageBox.critical(None, 'Fail', "amount must be a number")
                if amount > 0:
                    transaction = self.wallet.make_transaction(receiver, amount)
                    self.peer.udp_send(transaction)
                    print("sent transaction")
                else:
                    qtw.QMessageBox.critical(None, 'Fail', "amount must be more than zero")

        except ValueError:
            qtw.QMessageBox.critical(None, 'Fail', "password doesn't match the protected private key that was provided.")
        except AttributeError:
            qtw.QMessageBox.critical(None, 'Fail', "no contact selected.")


    # on events:
    def mousePressEvent(self, event):
        self.last_click_on_empty_space = event.globalPos()

    def resizeEvent(self, event):
        qtw.QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        # top left grip doesn't need to be moved...
        # top right
        self.grips[1].move(rect.right() - self.gripSize, 0)
        # bottom right
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grips[3].move(0, rect.bottom() - self.gripSize)


if __name__ == "__main__":
    app = qtw.QApplication([])
    widget = MainWindow()
    widget.show()
    app.exec_()