# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'meetcoincGIHiz.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(947, 545)
        MainWindow.setStyleSheet(u"background-color: rgb(83, 83, 83);\n"
"background-color: rgb(53, 53, 53);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"color:white")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.title_bar = QFrame(self.centralwidget)
        self.title_bar.setObjectName(u"title_bar")
        self.title_bar.setMinimumSize(QSize(0, 25))
        self.title_bar.setMaximumSize(QSize(16777215, 25))
        self.title_bar.setStyleSheet(u"background-color: rgb(43, 43, 43);")
        self.title_bar.setFrameShape(QFrame.StyledPanel)
        self.title_bar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.title_bar)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.title_bar)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.minimize_button = QPushButton(self.title_bar)
        self.minimize_button.setObjectName(u"minimize_button")
        self.minimize_button.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.minimize_button)

        self.maximize_button = QPushButton(self.title_bar)
        self.maximize_button.setObjectName(u"maximize_button")
        self.maximize_button.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.maximize_button)

        self.exit_button = QPushButton(self.title_bar)
        self.exit_button.setObjectName(u"exit_button")
        self.exit_button.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.exit_button)


        self.verticalLayout_2.addWidget(self.title_bar)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.menu_frame = QFrame(self.frame)
        self.menu_frame.setObjectName(u"menu_frame")
        self.menu_frame.setMinimumSize(QSize(180, 0))
        self.menu_frame.setStyleSheet(u"background-color: rgb(53, 53, 53);")
        self.menu_frame.setFrameShape(QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.menu_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.my_wallet_btn = QPushButton(self.menu_frame)
        self.my_wallet_btn.setObjectName(u"my_wallet_btn")

        self.verticalLayout_3.addWidget(self.my_wallet_btn)

        self.blockchain_btn = QPushButton(self.menu_frame)
        self.blockchain_btn.setObjectName(u"blockchain_btn")

        self.verticalLayout_3.addWidget(self.blockchain_btn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.help_btn = QPushButton(self.menu_frame)
        self.help_btn.setObjectName(u"help_btn")

        self.verticalLayout_3.addWidget(self.help_btn)


        self.horizontalLayout.addWidget(self.menu_frame)

        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background-color: rgb(83, 83, 83);")
        self.blockchain_pg = QWidget()
        self.blockchain_pg.setObjectName(u"blockchain_pg")
        self.verticalLayout_4 = QVBoxLayout(self.blockchain_pg)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.blockchain_tree = QTreeWidget(self.blockchain_pg)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.blockchain_tree.setHeaderItem(__qtreewidgetitem)
        self.blockchain_tree.setObjectName(u"blockchain_tree")
        self.blockchain_tree.header().setVisible(False)

        self.verticalLayout_4.addWidget(self.blockchain_tree)

        self.stackedWidget.addWidget(self.blockchain_pg)
        self.help_pg = QWidget()
        self.help_pg.setObjectName(u"help_pg")
        self.verticalLayout_12 = QVBoxLayout(self.help_pg)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.help_grid = QFrame(self.help_pg)
        self.help_grid.setObjectName(u"help_grid")
        self.help_grid.setFrameShape(QFrame.StyledPanel)
        self.help_grid.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.help_grid)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(self.help_grid)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_2.addWidget(self.label_20, 0, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 1, 0, 1, 1)


        self.verticalLayout_12.addWidget(self.help_grid)

        self.stackedWidget.addWidget(self.help_pg)
        self.my_wallet_pg = QWidget()
        self.my_wallet_pg.setObjectName(u"my_wallet_pg")
        self.verticalLayout_6 = QVBoxLayout(self.my_wallet_pg)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.my_wallet_pg)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(u"QTabWidget::pane { border: 0; }")
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(True)
        self.my_wallet_tab = QWidget()
        self.my_wallet_tab.setObjectName(u"my_wallet_tab")
        self.verticalLayout = QVBoxLayout(self.my_wallet_tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.my_wallet_tab)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame_3)
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.public_key_lbl = QLabel(self.frame_3)
        self.public_key_lbl.setObjectName(u"public_key_lbl")
        self.public_key_lbl.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.public_key_lbl)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.current_balance_lbl = QLabel(self.frame_3)
        self.current_balance_lbl.setObjectName(u"current_balance_lbl")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.current_balance_lbl)

        self.label_25 = QLabel(self.frame_3)
        self.label_25.setObjectName(u"label_25")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_25)

        self.current_stake_lbl = QLabel(self.frame_3)
        self.current_stake_lbl.setObjectName(u"current_stake_lbl")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.current_stake_lbl)


        self.verticalLayout.addWidget(self.frame_3)

        self.tabWidget.addTab(self.my_wallet_tab, "")
        self.add_contact_tab = QWidget()
        self.add_contact_tab.setObjectName(u"add_contact_tab")
        self.verticalLayout_7 = QVBoxLayout(self.add_contact_tab)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.add_contact_tab)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.formLayout_3 = QFormLayout(self.frame_5)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.new_contacts_name_in = QLineEdit(self.frame_5)
        self.new_contacts_name_in.setObjectName(u"new_contacts_name_in")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.new_contacts_name_in)

        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_9)

        self.new_contacts_public_key_in = QLineEdit(self.frame_5)
        self.new_contacts_public_key_in.setObjectName(u"new_contacts_public_key_in")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.new_contacts_public_key_in)

        self.add_contact_btn = QPushButton(self.frame_5)
        self.add_contact_btn.setObjectName(u"add_contact_btn")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.add_contact_btn)


        self.verticalLayout_7.addWidget(self.frame_5)

        self.tabWidget.addTab(self.add_contact_tab, "")
        self.edit_delete_contact_tab = QWidget()
        self.edit_delete_contact_tab.setObjectName(u"edit_delete_contact_tab")
        self.verticalLayout_8 = QVBoxLayout(self.edit_delete_contact_tab)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.edit_delete_contact_tab)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.formLayout_4 = QFormLayout(self.frame_6)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_10 = QLabel(self.frame_6)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_10)

        self.label_11 = QLabel(self.frame_6)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_11)

        self.updated_contacts_name_in = QLineEdit(self.frame_6)
        self.updated_contacts_name_in.setObjectName(u"updated_contacts_name_in")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.updated_contacts_name_in)

        self.updated_contacts_public_key_in = QLineEdit(self.frame_6)
        self.updated_contacts_public_key_in.setObjectName(u"updated_contacts_public_key_in")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.updated_contacts_public_key_in)

        self.update_contact_btn = QPushButton(self.frame_6)
        self.update_contact_btn.setObjectName(u"update_contact_btn")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.update_contact_btn)

        self.delete_contact_btn = QPushButton(self.frame_6)
        self.delete_contact_btn.setObjectName(u"delete_contact_btn")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.delete_contact_btn)


        self.verticalLayout_8.addWidget(self.frame_6)

        self.tabWidget.addTab(self.edit_delete_contact_tab, "")
        self.make_transaction_tab = QWidget()
        self.make_transaction_tab.setObjectName(u"make_transaction_tab")
        self.verticalLayout_9 = QVBoxLayout(self.make_transaction_tab)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.make_transaction_tab)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.formLayout_2 = QFormLayout(self.frame_4)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.amount_text_incer = QLineEdit(self.frame_4)
        self.amount_text_incer.setObjectName(u"amount_text_incer")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.amount_text_incer)

        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.transaction_password_in = QLineEdit(self.frame_4)
        self.transaction_password_in.setObjectName(u"transaction_password_in")
        self.transaction_password_in.setEchoMode(QLineEdit.Password)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.transaction_password_in)

        self.send_transaction_btn = QPushButton(self.frame_4)
        self.send_transaction_btn.setObjectName(u"send_transaction_btn")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.send_transaction_btn)


        self.verticalLayout_9.addWidget(self.frame_4)

        self.tabWidget.addTab(self.make_transaction_tab, "")
        self.proposed_tab = QWidget()
        self.proposed_tab.setObjectName(u"proposed_tab")
        self.gridLayout = QGridLayout(self.proposed_tab)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.transaction_pool_tree = QTreeWidget(self.proposed_tab)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.transaction_pool_tree.setHeaderItem(__qtreewidgetitem1)
        self.transaction_pool_tree.setObjectName(u"transaction_pool_tree")
        self.transaction_pool_tree.header().setVisible(False)

        self.gridLayout.addWidget(self.transaction_pool_tree, 1, 1, 1, 1)

        self.proposed_blocks_tree = QTreeWidget(self.proposed_tab)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setText(0, u"1");
        self.proposed_blocks_tree.setHeaderItem(__qtreewidgetitem2)
        self.proposed_blocks_tree.setObjectName(u"proposed_blocks_tree")
        self.proposed_blocks_tree.header().setVisible(False)

        self.gridLayout.addWidget(self.proposed_blocks_tree, 1, 0, 1, 1)

        self.label_17 = QLabel(self.proposed_tab)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 0, 0, 1, 1)

        self.label_18 = QLabel(self.proposed_tab)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout.addWidget(self.label_18, 0, 1, 1, 1)

        self.tabWidget.addTab(self.proposed_tab, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_11 = QVBoxLayout(self.tab)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.tab)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.new_password_in = QLineEdit(self.frame_2)
        self.new_password_in.setObjectName(u"new_password_in")
        self.new_password_in.setEchoMode(QLineEdit.Password)

        self.gridLayout_6.addWidget(self.new_password_in, 1, 1, 1, 3)

        self.label_19 = QLabel(self.frame_2)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_6.addWidget(self.label_19, 1, 0, 1, 1)

        self.change_password_btn = QPushButton(self.frame_2)
        self.change_password_btn.setObjectName(u"change_password_btn")

        self.gridLayout_6.addWidget(self.change_password_btn, 3, 0, 1, 1)

        self.label_16 = QLabel(self.frame_2)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_6.addWidget(self.label_16, 2, 0, 1, 1)

        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)

        self.confirm_updated_password_in = QLineEdit(self.frame_2)
        self.confirm_updated_password_in.setObjectName(u"confirm_updated_password_in")
        self.confirm_updated_password_in.setEchoMode(QLineEdit.Password)

        self.gridLayout_6.addWidget(self.confirm_updated_password_in, 2, 1, 1, 3)

        self.label_32 = QLabel(self.frame_2)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_6.addWidget(self.label_32, 5, 2, 1, 1)

        self.old_password_in = QLineEdit(self.frame_2)
        self.old_password_in.setObjectName(u"old_password_in")
        self.old_password_in.setEchoMode(QLineEdit.Password)

        self.gridLayout_6.addWidget(self.old_password_in, 0, 1, 1, 3)

        self.label_13 = QLabel(self.frame_2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_6.addWidget(self.label_13, 5, 0, 4, 1)

        self.protected_private_key_lbl = QLabel(self.frame_2)
        self.protected_private_key_lbl.setObjectName(u"protected_private_key_lbl")
        self.protected_private_key_lbl.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout_6.addWidget(self.protected_private_key_lbl, 6, 2, 3, 2)


        self.verticalLayout_11.addWidget(self.frame_2)

        self.tabWidget.addTab(self.tab, "")

        self.verticalLayout_6.addWidget(self.tabWidget)

        self.label_28 = QLabel(self.my_wallet_pg)
        self.label_28.setObjectName(u"label_28")

        self.verticalLayout_6.addWidget(self.label_28)

        self.contacts_list = QListWidget(self.my_wallet_pg)
        QListWidgetItem(self.contacts_list)
        self.contacts_list.setObjectName(u"contacts_list")
        self.contacts_list.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_6.addWidget(self.contacts_list)

        self.stackedWidget.addWidget(self.my_wallet_pg)
        self.updating_blockchain_pg = QWidget()
        self.updating_blockchain_pg.setObjectName(u"updating_blockchain_pg")
        self.gridLayout_3 = QGridLayout(self.updating_blockchain_pg)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_13 = QFrame(self.updating_blockchain_pg)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_13)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.frame_13)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)

        self.stop_waiting_button = QPushButton(self.frame_13)
        self.stop_waiting_button.setObjectName(u"stop_waiting_button")

        self.gridLayout_4.addWidget(self.stop_waiting_button, 0, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_13, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.updating_blockchain_pg)
        self.change_wallet_pg = QWidget()
        self.change_wallet_pg.setObjectName(u"change_wallet_pg")
        self.verticalLayout_13 = QVBoxLayout(self.change_wallet_pg)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_3 = QTabWidget(self.change_wallet_pg)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tabWidget_3.setStyleSheet(u"QTabWidget::pane { border: 0; border-top: 0px; }")
        self.tabWidget_3.setTabShape(QTabWidget.Triangular)
        self.already_have_wallet_tab = QWidget()
        self.already_have_wallet_tab.setObjectName(u"already_have_wallet_tab")
        self.verticalLayout_17 = QVBoxLayout(self.already_have_wallet_tab)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_12 = QFrame(self.already_have_wallet_tab)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.formLayout_11 = QFormLayout(self.frame_12)
        self.formLayout_11.setObjectName(u"formLayout_11")
        self.formLayout_11.setHorizontalSpacing(0)
        self.formLayout_11.setVerticalSpacing(0)
        self.formLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_23 = QLabel(self.frame_12)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_11.setWidget(0, QFormLayout.LabelRole, self.label_23)

        self.already_have_wallet_password_in = QLineEdit(self.frame_12)
        self.already_have_wallet_password_in.setObjectName(u"already_have_wallet_password_in")
        self.already_have_wallet_password_in.setEchoMode(QLineEdit.Password)

        self.formLayout_11.setWidget(0, QFormLayout.FieldRole, self.already_have_wallet_password_in)

        self.enter_wallet_btn = QPushButton(self.frame_12)
        self.enter_wallet_btn.setObjectName(u"enter_wallet_btn")

        self.formLayout_11.setWidget(1, QFormLayout.LabelRole, self.enter_wallet_btn)


        self.verticalLayout_17.addWidget(self.frame_12)

        self.tabWidget_3.addTab(self.already_have_wallet_tab, "")
        self.new_wallet_tab = QWidget()
        self.new_wallet_tab.setObjectName(u"new_wallet_tab")
        self.verticalLayout_14 = QVBoxLayout(self.new_wallet_tab)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.frame_11 = QFrame(self.new_wallet_tab)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_11)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_14.addWidget(self.frame_11)

        self.frame_9 = QFrame(self.new_wallet_tab)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setStyleSheet(u"QTabWidget::pane { border: 0; }")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_9)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.create_wallet_btn = QPushButton(self.frame_9)
        self.create_wallet_btn.setObjectName(u"create_wallet_btn")

        self.gridLayout_5.addWidget(self.create_wallet_btn, 2, 0, 1, 1)

        self.label_24 = QLabel(self.frame_9)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_5.addWidget(self.label_24, 0, 0, 1, 1)

        self.label_12 = QLabel(self.frame_9)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_5.addWidget(self.label_12, 3, 0, 1, 2)

        self.verticalSpacer_2 = QSpacerItem(20, 16777215, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_2, 4, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 3, 2, 1, 1)

        self.choosing_password_in = QLineEdit(self.frame_9)
        self.choosing_password_in.setObjectName(u"choosing_password_in")
        self.choosing_password_in.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.choosing_password_in.setEchoMode(QLineEdit.Password)

        self.gridLayout_5.addWidget(self.choosing_password_in, 0, 1, 1, 2)

        self.label_15 = QLabel(self.frame_9)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_5.addWidget(self.label_15, 1, 0, 1, 1)

        self.confirm_new_password_in = QLineEdit(self.frame_9)
        self.confirm_new_password_in.setObjectName(u"confirm_new_password_in")
        self.confirm_new_password_in.setEchoMode(QLineEdit.Password)

        self.gridLayout_5.addWidget(self.confirm_new_password_in, 1, 1, 1, 2)


        self.verticalLayout_14.addWidget(self.frame_9)

        self.tabWidget_3.addTab(self.new_wallet_tab, "")
        self.already_have_a_wallet_on_device_tab = QWidget()
        self.already_have_a_wallet_on_device_tab.setObjectName(u"already_have_a_wallet_on_device_tab")
        self.verticalLayout_15 = QVBoxLayout(self.already_have_a_wallet_on_device_tab)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.already_have_a_wallet_on_device_tab)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.formLayout_10 = QFormLayout(self.frame_10)
        self.formLayout_10.setObjectName(u"formLayout_10")
        self.formLayout_10.setHorizontalSpacing(0)
        self.formLayout_10.setVerticalSpacing(0)
        self.formLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_21 = QLabel(self.frame_10)
        self.label_21.setObjectName(u"label_21")

        self.formLayout_10.setWidget(0, QFormLayout.LabelRole, self.label_21)

        self.recreate_wallet_password = QLineEdit(self.frame_10)
        self.recreate_wallet_password.setObjectName(u"recreate_wallet_password")
        self.recreate_wallet_password.setEchoMode(QLineEdit.Password)

        self.formLayout_10.setWidget(0, QFormLayout.FieldRole, self.recreate_wallet_password)

        self.label_22 = QLabel(self.frame_10)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_10.setWidget(1, QFormLayout.LabelRole, self.label_22)

        self.recreate_wallet_private_key = QLineEdit(self.frame_10)
        self.recreate_wallet_private_key.setObjectName(u"recreate_wallet_private_key")

        self.formLayout_10.setWidget(1, QFormLayout.FieldRole, self.recreate_wallet_private_key)

        self.recreate_wallet_btn = QPushButton(self.frame_10)
        self.recreate_wallet_btn.setObjectName(u"recreate_wallet_btn")

        self.formLayout_10.setWidget(2, QFormLayout.LabelRole, self.recreate_wallet_btn)


        self.verticalLayout_15.addWidget(self.frame_10)

        self.tabWidget_3.addTab(self.already_have_a_wallet_on_device_tab, "")

        self.verticalLayout_13.addWidget(self.tabWidget_3)

        self.stackedWidget.addWidget(self.change_wallet_pg)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.verticalLayout_2.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(4)
        self.tabWidget.setCurrentIndex(0)
        self.contacts_list.setCurrentRow(-1)
        self.tabWidget_3.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"meetcoin", None))
        self.minimize_button.setText(QCoreApplication.translate("MainWindow", u"min", None))
        self.maximize_button.setText(QCoreApplication.translate("MainWindow", u"max", None))
        self.exit_button.setText(QCoreApplication.translate("MainWindow", u"close", None))
        self.my_wallet_btn.setText(QCoreApplication.translate("MainWindow", u"my wallet", None))
        self.blockchain_btn.setText(QCoreApplication.translate("MainWindow", u"blockchain", None))
        self.help_btn.setText(QCoreApplication.translate("MainWindow", u"help", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"you can change your password from the \"settings\" page.\n"
"to open this wallet on another machine, go to the settings page, copy your encrypted private key,\n"
"and provide it at the \"already have a wallet, but not on this device\"\n"
"to give someone coins, you have to add that person as a contact. after that, you can select the contact,\n"
"and make transaction in the \"make transaction\" page.\n"
"to delete or edit a contact, you have to select the contact.\n"
"you can retrieve stake by sending a negative amount to the stake address.", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"your public key: ", None))
        self.public_key_lbl.setText(QCoreApplication.translate("MainWindow", u"public_key", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"your current balance: ", None))
        self.current_balance_lbl.setText(QCoreApplication.translate("MainWindow", u"current_balance", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"your current stake: ", None))
        self.current_stake_lbl.setText(QCoreApplication.translate("MainWindow", u"current_stake", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.my_wallet_tab), QCoreApplication.translate("MainWindow", u"my wallet", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"new contacts name: ", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"new contacts public key: ", None))
        self.add_contact_btn.setText(QCoreApplication.translate("MainWindow", u"add contact", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.add_contact_tab), QCoreApplication.translate("MainWindow", u"add contact", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"updated contacts name: ", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"updated contacts public key: ", None))
        self.update_contact_btn.setText(QCoreApplication.translate("MainWindow", u"update selected contact", None))
        self.delete_contact_btn.setText(QCoreApplication.translate("MainWindow", u"delete selected contact", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.edit_delete_contact_tab), QCoreApplication.translate("MainWindow", u"edit\\delete contact", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"amount (not including validator fee): ", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"password: ", None))
        self.send_transaction_btn.setText(QCoreApplication.translate("MainWindow", u"sign the transaction and send it", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.make_transaction_tab), QCoreApplication.translate("MainWindow", u"make transaction", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"proposed blocks:", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"transaction pool: ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.proposed_tab), QCoreApplication.translate("MainWindow", u"proposed blocks\\transaction pool", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"updated password: ", None))
        self.change_password_btn.setText(QCoreApplication.translate("MainWindow", u"update password", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"confirm password: ", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"old password: ", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"your protected private key:", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"passwords must contain:\n"
"        8 characters length or more\n"
"        1 digit or more\n"
"        1 symbol or more\n"
"        1 uppercase letter or more\n"
"        1 lowercase letter or more", None))
        self.protected_private_key_lbl.setText(QCoreApplication.translate("MainWindow", u"protected_private_key", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"settings", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"contacts list:", None))

        __sortingEnabled = self.contacts_list.isSortingEnabled()
        self.contacts_list.setSortingEnabled(False)
        ___qlistwidgetitem = self.contacts_list.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"stake: STAKE_ADDRESS", None));
        self.contacts_list.setSortingEnabled(__sortingEnabled)

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"trying to collect blocks and to update the local blockchain...", None))
        self.stop_waiting_button.setText(QCoreApplication.translate("MainWindow", u"stop watiting", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"password: ", None))
        self.enter_wallet_btn.setText(QCoreApplication.translate("MainWindow", u"enter wallet", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.already_have_wallet_tab), QCoreApplication.translate("MainWindow", u"already have a wallet on this device", None))
        self.create_wallet_btn.setText(QCoreApplication.translate("MainWindow", u"create wallet", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"new password: ", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"passwords must contain:\n"
"        8 characters length or more\n"
"        1 digit or more\n"
"        1 symbol or more\n"
"        1 uppercase letter or more\n"
"        1 lowercase letter or more", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"confirm password: ", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.new_wallet_tab), QCoreApplication.translate("MainWindow", u"new wallet", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"password: ", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"secret key (protected by the provided password): ", None))
        self.recreate_wallet_btn.setText(QCoreApplication.translate("MainWindow", u"recreate wallet", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.already_have_a_wallet_on_device_tab), QCoreApplication.translate("MainWindow", u"already have a wallet, but not on this device", None))
    # retranslateUi

