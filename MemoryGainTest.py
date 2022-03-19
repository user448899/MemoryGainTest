"""
Joshua Chick. Memory Gain is a flashcards app.
Copyright (C) 2022 Joshua Chick

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import time
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QDesktopWidget
import datetime
import re
import tempfile
import urllib.request
import os


class Ui_main_win(object):

    def __init__(self):
        self.temp_path = tempfile.gettempdir()

    def setupUi(self):
        # File and directory checker.
        memorygaindir_on_device = os.path.exists(f"{self.temp_path}\\..\\MemoryGain")
        cards_on_device = os.path.exists(f"{self.temp_path}\\..\\MemoryGain\\cards.txt")
        decks_on_device = os.path.exists(f"{self.temp_path}\\..\\MemoryGain\\decks.txt")

        if not memorygaindir_on_device:
            os.system(f"md {self.temp_path}\\..\\MemoryGain")

        if not cards_on_device:
            os.system(f"null > {self.temp_path}\\..\\MemoryGain\\cards.txt")

        if not decks_on_device:
            os.system(f"null > {self.temp_path}\\..\\MemoryGain\\decks.txt")

        # Update checker.
        going_to_update = False
        try:
            html = urllib.request.urlopen("https://memorygain.app")
            if "Test version 0.0.0" not in str(html.read()):
                self.update_msg = QtWidgets.QMessageBox()
                self.update_msg.setWindowTitle("Update")
                self.update_msg.setText(
                    "There is an updated version available at https://memorygain.app. Would you like to download the updated version?")
                self.update_msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                self.update_msg.setIcon(QtWidgets.QMessageBox.Information)
                self.update_msg.exec_()
                if self.update_msg.clickedButton().text() == "&Yes":
                    going_to_update = True
                    os.system("START https://memorygain.app")

        except:
            pass

        if going_to_update:
            sys.exit()

        # Main window.
        self.main_win = QtWidgets.QMainWindow()
        # Finds how many are due today.
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        cards_parts = re.split("DUE\^\^\$=|INTERVAL\^\^\$=", cards_text.read())
        cards_text.close()
        cards_parts.pop(0)
        num_to_study = 0
        # Removes those not due today.
        end_of_today = str(datetime.datetime.now())
        end_of_today = datetime.datetime(int(end_of_today[:4]), int(end_of_today[5:7]), int(end_of_today[8:10]), 23, 59, 59, 999999)
        for idx, part in enumerate(cards_parts):
            if idx % 2 == 0 and datetime.datetime.strptime(part, "%Y-%m-%d %H:%M:%S.%f") <= end_of_today:
                num_to_study += 1

        self.main_win.setObjectName("main_win")
        self.main_win.resize(750, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_win.sizePolicy().hasHeightForWidth())
        self.main_win.setSizePolicy(sizePolicy)
        self.main_win.setMinimumSize(QtCore.QSize(700, 400))
        self.main_win.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.main_win.setStyleSheet("""
                                QMainWindow#main_win{
                                    background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(30, 10, 30, 255), stop:1 rgba(60, 10, 60, 255));
                                }
                                QScrollBar{
                                    background: transparent;
                                    width: 10px;
                                }
                                """)

        self.main_win_centralwidget = QtWidgets.QWidget(self.main_win)
        self.main_win_centralwidget.setObjectName("main_win_centralwidget")
        self.main_win_gridLayout = QtWidgets.QGridLayout(self.main_win_centralwidget)
        self.main_win_gridLayout.setObjectName("main_win_gridLayout")

        self.create_deck_btn = QtWidgets.QPushButton(self.main_win_centralwidget)
        self.create_deck_btn.setObjectName("create_deck_btn")
        self.create_deck_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.create_deck_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.create_deck_btn.setFont(font)
        self.create_deck_btn.setStyleSheet("""
                                            QPushButton#create_deck_btn{
                                                background-color:transparent;
                                                border-radius: 15px;
                                                border: 1px solid white;
                                                color: white;
                                            }
                                            QPushButton#create_deck_btn:hover{
                                                background-color: rgba(255, 255, 255, 0.1);
                                            }
                                            QPushButton#create_deck_btn:pressed{
                                                background-color: rgba(255, 255, 255, 0.2);
                                            }
                                            """)
        self.create_deck_btn.clicked.connect(lambda: self.create_deck_btn_clicked())
        self.create_deck_btn.setText("Create deck")
        self.main_win_gridLayout.addWidget(self.create_deck_btn, 0, 1, 1, 1)

        self.study_btn = QtWidgets.QPushButton(self.main_win_centralwidget)
        self.study_btn.setObjectName("study_btn")
        self.study_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.study_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.study_btn.setFont(font)
        self.study_btn.setStyleSheet("""
                                    QPushButton#study_btn{
                                        background-color:transparent;
                                        border-radius: 15px;
                                        border: 1px solid white;
                                        color: white;
                                    }
                                    QPushButton#study_btn:hover{
                                        background-color: rgba(255, 255, 255, 0.1);
                                    }
                                    QPushButton#study_btn:pressed{
                                        background-color: rgba(255, 255, 255, 0.2);
                                    }
                                    """)
        if num_to_study < 1000:
            self.study_btn.setText(f"Study {num_to_study}")
        else:
            self.study_btn.setText(f"Study 999+")
        self.study_btn.clicked.connect(lambda: self.study_btn_clicked())
        self.main_win_gridLayout.addWidget(self.study_btn, 1, 1, 1, 1)

        main_win_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_win_gridLayout.addItem(main_win_spacer, 0, 2, 1, 1)

        main_win_spacer1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_win_gridLayout.addItem(main_win_spacer1, 0, 0, 1, 1)

        self.main_win_scrollArea = QtWidgets.QScrollArea(self.main_win_centralwidget)
        self.main_win_scrollArea.setMinimumSize(QtCore.QSize(310, 16777215))
        self.main_win_scrollArea.setMaximumSize(QtCore.QSize(310, 16777215))
        self.main_win_scrollArea.setWidgetResizable(True)
        self.main_win_scrollArea.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.main_win_scrollArea.setObjectName("main_win_scrollArea")
        self.main_win_scrollArea.setStyleSheet("""
                                                background-color: transparent;
                                                border: none;
                                                """)
        self.main_win_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.main_win_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 300, 435))
        self.main_win_scrollAreaWidgetContents.setObjectName("main_win_scrollAreaWidgetContents")
        self.main_win_verticalLayout = QtWidgets.QVBoxLayout(self.main_win_scrollAreaWidgetContents)
        self.main_win_verticalLayout.setObjectName("main_win_verticalLayout")

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "r")
        decks_lines = decks_text.readlines()
        for idx, i in enumerate(decks_lines):
            self.deck_btn = QtWidgets.QPushButton(self.main_win_scrollAreaWidgetContents)
            self.deck_btn.setMinimumSize(QtCore.QSize(282, 40))
            self.deck_btn.setMaximumSize(QtCore.QSize(282, 40))
            self.deck_btn.setFont(font)
            self.deck_btn.setStyleSheet("""
                                        QPushButton#deck_btn{
                                            background-color: transparent;
                                            text-align: left;
                                            color: white;
                                            border-radius: 15px;
                                        }
                                        QPushButton#deck_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#deck_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
            self.deck_btn.setObjectName("deck_btn")
            self.deck_btn.setText("  " + i.replace("\n", ""))
            self.main_win_verticalLayout.addWidget(self.deck_btn)
            if idx == 0:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(0))
            if idx == 1:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(1))
            if idx == 2:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(2))
            if idx == 3:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(3))
            if idx == 4:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(4))
            if idx == 5:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(5))
            if idx == 6:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(6))
            if idx == 7:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(7))
            if idx == 8:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(8))
            if idx == 9:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(9))

        decks_text.close()

        main_win_spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_win_verticalLayout.addItem(main_win_spacer2)
        self.main_win_scrollArea.setWidget(self.main_win_scrollAreaWidgetContents)
        self.main_win_gridLayout.addWidget(self.main_win_scrollArea, 2, 1, 1, 1)
        self.create_deck_btn.raise_()
        self.main_win_scrollArea.raise_()
        self.main_win.setCentralWidget(self.main_win_centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self.main_win)

        _translate = QtCore.QCoreApplication.translate
        self.main_win.setWindowTitle(_translate("main_win", "Memory Gain"))
        self.main_win.setIconSize(QtCore.QSize(0, 0))
        self.main_win.setWindowIcon(QtGui.QIcon("feather\\layers.svg"))

        self.main_win.show()

    def study_btn_clicked(self):
        # Clears main_win
        self.main_win_centralwidget = QtWidgets.QWidget()
        self.main_win_centralwidget.deleteLater()

        # Closes Create deck window.
        self.create_deck_win = QtWidgets.QWidget()
        self.create_deck_win.close()

        # Creates new main_win_centralwidget and main_win_gridLayout.
        self.study_centralwidget = QtWidgets.QWidget()
        self.study_gridLayout = QtWidgets.QGridLayout(self.study_centralwidget)

        self.get_card()

        self.study_gridLayout.setObjectName("study_gridLayout")
        self.study_upper_horizontalLayout = QtWidgets.QHBoxLayout()
        self.study_upper_horizontalLayout.setObjectName("study_upper_horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_upper_horizontalLayout.addItem(spacerItem)

        self.study_home_btn = QtWidgets.QPushButton(self.main_win)
        self.study_home_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.study_home_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.study_home_btn.setFont(font)
        self.study_home_btn.setStyleSheet("""
                                        QPushButton#study_home_btn{
                                            background-color:transparent;
                                            border-radius: 15px;
                                            border: 1px solid white;
                                            color: white;
                                        }
                                        QPushButton#study_home_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#study_home_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.study_home_btn.setObjectName("study_home_btn")
        self.study_upper_horizontalLayout.addWidget(self.study_home_btn)
        self.study_home_btn.clicked.connect(lambda: self.study_home_btn_clicked())

        self.study_edit_btn = QtWidgets.QPushButton(self.main_win)
        self.study_edit_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.study_edit_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.study_edit_btn.setFont(font)
        self.study_edit_btn.setStyleSheet("""
                                        QPushButton#study_edit_btn{
                                            background-color:transparent;
                                            border-radius: 15px;
                                            border: 1px solid white;
                                            color: white;
                                        }
                                        QPushButton#study_edit_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#study_edit_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.study_edit_btn.setObjectName("study_edit_btn")
        self.study_edit_btn.clicked.connect(lambda: self.study_edit_btn_clicked())
        if not self.got_card:
            self.study_edit_btn.hide()

        self.study_upper_horizontalLayout.addWidget(self.study_edit_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_upper_horizontalLayout.addItem(spacerItem1)
        self.study_gridLayout.addLayout(self.study_upper_horizontalLayout, 0, 0, 1, 1)
        self.study_labels_verticalLayout = QtWidgets.QVBoxLayout()
        self.study_labels_verticalLayout.setObjectName("study_labels_verticalLayout")
        self.study_qst_label = QtWidgets.QLabel(self.main_win)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.study_qst_label.sizePolicy().hasHeightForWidth())
        self.study_qst_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.study_qst_label.setFont(font)
        self.study_qst_label.setStyleSheet("""
                                            QLabel#study_qst_label{
                                                color: white;
                                           }
                                           """)
        self.study_qst_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.study_qst_label.setObjectName("study_qst_label")
        self.study_labels_verticalLayout.addWidget(self.study_qst_label)
        if not self.got_card:
            self.study_qst_label.setText("Completed.")
        else:
            self.study_qst_label.setText(self.got_card[1])

        self.study_line = QtWidgets.QFrame(self.main_win)
        self.study_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.study_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.study_line.setObjectName("study_line")
        if not self.got_card:
            self.study_line.hide()

        self.study_labels_verticalLayout.addWidget(self.study_line)

        self.study_ans_label = QtWidgets.QLabel(self.main_win)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.study_ans_label.sizePolicy().hasHeightForWidth())
        self.study_ans_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.study_ans_label.setFont(font)
        self.study_ans_label.setStyleSheet("""
                                            QLabel#study_ans_label{
                                                color:white;
                                           }
                                           """)
        self.study_ans_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.study_ans_label.setObjectName("study_ans_label")
        self.study_labels_verticalLayout.addWidget(self.study_ans_label)

        self.study_gridLayout.addLayout(self.study_labels_verticalLayout, 1, 0, 1, 1)
        self.study_lower_horizontalLayout = QtWidgets.QHBoxLayout()
        self.study_lower_horizontalLayout.setObjectName("study_lower_horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_lower_horizontalLayout.addItem(spacerItem2)

        self.again_btn = QtWidgets.QPushButton(self.main_win)
        self.again_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.again_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.again_btn.setFont(font)
        self.again_btn.setStyleSheet("""
                                    QPushButton#again_btn{
                                        background-color:transparent;
                                        border-radius: 15px;
                                        border: 1px solid white;
                                        color: white;
                                    }
                                    QPushButton#again_btn:hover{
                                        background-color: rgba(255, 255, 255, 0.1);
                                    }
                                    QPushButton#again_btn:pressed{
                                        background-color: rgba(255, 255, 255, 0.2);
                                    }
                                    """)
        self.again_btn.setObjectName("again_btn")
        self.study_lower_horizontalLayout.addWidget(self.again_btn)
        self.again_btn.clicked.connect(lambda: self.again_btn_clicked())
        self.again_btn.hide()

        self.show_ans_btn = QtWidgets.QPushButton(self.main_win)
        self.show_ans_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.show_ans_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.show_ans_btn.setFont(font)
        self.show_ans_btn.setStyleSheet("""
                                        QPushButton#show_ans_btn{
                                            background-color:transparent;
                                            border-radius: 15px;
                                            border: 1px solid white;
                                            color: white;
                                        }
                                        QPushButton#show_ans_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#show_ans_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.show_ans_btn.setObjectName("show_ans_btn")
        self.study_lower_horizontalLayout.addWidget(self.show_ans_btn)
        self.show_ans_btn.clicked.connect(lambda: self.show_ans_btn_clicked())
        if not self.got_card:
            self.show_ans_btn.hide()

        self.correct_btn = QtWidgets.QPushButton(self.main_win)
        self.correct_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.correct_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.correct_btn.setFont(font)
        self.correct_btn.setStyleSheet("""
                                        QPushButton#correct_btn{
                                            background-color:transparent;
                                            border-radius: 15px;
                                            border: 1px solid white;
                                            color: white;
                                        }
                                        QPushButton#correct_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#correct_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.correct_btn.setObjectName("correct_btn")
        self.study_lower_horizontalLayout.addWidget(self.correct_btn)
        self.correct_btn.clicked.connect(lambda: self.correct_btn_clicked())
        self.correct_btn.hide()

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_lower_horizontalLayout.addItem(spacerItem3)
        self.study_gridLayout.addLayout(self.study_lower_horizontalLayout, 2, 0, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(self.main_win)

        _translate = QtCore.QCoreApplication.translate

        self.main_win.setWindowTitle(_translate("study_win", "Memory Gain - Study"))
        self.study_home_btn.setText(_translate("study_win", "Home"))
        self.study_edit_btn.setText(_translate("study_win", "Edit"))
        self.again_btn.setText(_translate("study_win", "Again"))
        self.show_ans_btn.setText(_translate("study_win", "Answer"))
        self.correct_btn.setText(_translate("study_win", "Correct"))

        self.main_win.setCentralWidget(self.study_centralwidget)

    def study_edit_btn_clicked(self):
        self.study_centralwidget.deleteLater()

        self.edit_centralwidget = QtWidgets.QWidget()
        self.edit_win_gridLayout = QtWidgets.QGridLayout(self.edit_centralwidget)
        self.edit_win_gridLayout.setObjectName("edit_win_gridLayout")
        self.edit_win_verticalLayout = QtWidgets.QVBoxLayout()
        self.edit_win_verticalLayout.setObjectName("edit_win_verticalLayout")

        self.edit_qst_label = QtWidgets.QLabel()
        self.edit_qst_label.setMinimumSize(QtCore.QSize(150, 35))
        self.edit_qst_label.setMaximumSize(QtCore.QSize(150, 35))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.edit_qst_label.setFont(font)
        self.edit_qst_label.setStyleSheet("""
                                            QLabel#edit_qst_label{
                                                color: white;
                                            }
                                          """)
        self.edit_qst_label.setObjectName("edit_qst_label")
        self.edit_win_verticalLayout.addWidget(self.edit_qst_label)

        self.edit_qst_text = QtWidgets.QTextEdit()
        self.edit_qst_text.setMinimumSize(QtCore.QSize(500, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.edit_qst_text.setFont(font)
        self.edit_qst_text.setStyleSheet("""
                                        QTextEdit#edit_qst_text{
                                            background-color: rgba(255, 255, 255, 0.1);
                                            color: white;
                                            border: none;
                                            border-radius: 15px;
                                            padding: 5px;
                                         }
                                         """)
        self.edit_qst_text.setObjectName("edit_qst_text")
        self.edit_qst_text.setText(self.got_card[1])
        self.edit_win_verticalLayout.addWidget(self.edit_qst_text)

        self.edit_ans_label = QtWidgets.QLabel()
        self.edit_ans_label.setMinimumSize(QtCore.QSize(150, 35))
        self.edit_ans_label.setMaximumSize(QtCore.QSize(150, 35))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.edit_ans_label.setFont(font)
        self.edit_ans_label.setStyleSheet("""
                                            QLabel#edit_ans_label{
                                                color: white;
                                          }
                                          """)
        self.edit_ans_label.setObjectName("edit_ans_label")
        self.edit_win_verticalLayout.addWidget(self.edit_ans_label)

        self.edit_ans_text = QtWidgets.QTextEdit()
        self.edit_ans_text.setMinimumSize(QtCore.QSize(500, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.edit_ans_text.setFont(font)
        self.edit_ans_text.setStyleSheet("""
                                        QTextEdit#edit_ans_text{                                         
                                            background-color: rgba(255, 255, 255, 0.1);
                                            color: white;
                                            border: none;
                                            border-radius: 15px;
                                            padding: 5px;
                                        }
                                        """)
        self.edit_ans_text.setObjectName("edit_ans_text")
        self.edit_ans_text.setText(self.got_card[2])
        self.edit_win_verticalLayout.addWidget(self.edit_ans_text)

        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.edit_win_verticalLayout.addItem(spacerItem)
        self.edit_win_gridLayout.addLayout(self.edit_win_verticalLayout, 0, 0, 1, 1)
        self.edit_win_horizontalLayout = QtWidgets.QHBoxLayout()
        self.edit_win_horizontalLayout.setObjectName("edit_win_horizontalLayout")

        self.edit_save_btn = QtWidgets.QPushButton()
        self.edit_save_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.edit_save_btn.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.edit_save_btn.setFont(font)
        self.edit_save_btn.setStyleSheet("""
                                        QPushButton#edit_save_btn{
                                            background-color: transparent;
                                            border: 1px solid white;
                                            border-radius: 15px;
                                            color: white;
                                         }
                                         QPushButton#edit_save_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                         }
                                         QPushButton#edit_save_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                         }
                                         """)
        self.edit_save_btn.setObjectName("edit_save_btn")
        self.edit_win_horizontalLayout.addWidget(self.edit_save_btn)
        self.edit_save_btn.clicked.connect(lambda: self.edit_save_btn_clicked())

        self.edit_del_btn = QtWidgets.QPushButton()
        self.edit_del_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.edit_del_btn.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.edit_del_btn.setFont(font)
        self.edit_del_btn.setStyleSheet("""
                                        QPushButton#edit_del_btn{
                                            background-color: transparent;
                                            border: 1px solid white;
                                            border-radius: 15px;
                                            color: white;
                                        }
                                        QPushButton#edit_del_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#edit_del_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.edit_del_btn.setObjectName("edit_del_btn")
        self.edit_win_horizontalLayout.addWidget(self.edit_del_btn)
        self.edit_del_btn.clicked.connect(lambda: self.edit_del_btn_clicked())

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.edit_win_horizontalLayout.addItem(spacerItem1)

        self.edit_back_btn = QtWidgets.QPushButton()
        self.edit_back_btn.setObjectName("edit_back_btn")
        self.edit_back_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.edit_back_btn.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.edit_back_btn.setFont(font)
        self.edit_back_btn.setStyleSheet("""
                                        QPushButton#edit_back_btn{
                                            background-color: transparent;
                                            border-radius: 15px;
                                            border: 1px solid white;
                                            color: white;
                                        }
                                        QPushButton#edit_back_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#edit_back_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.edit_win_horizontalLayout.addWidget(self.edit_back_btn)
        self.edit_back_btn.clicked.connect(lambda: self.edit_back_btn_clicked())

        self.edit_win_gridLayout.addLayout(self.edit_win_horizontalLayout, 1, 0, 1, 1)

        _translate = QtCore.QCoreApplication.translate
        self.main_win.setWindowTitle(_translate("edit_win", "Memory Gain - Study - Edit"))
        self.edit_qst_label.setText(_translate("edit_win", "Question:"))
        self.edit_ans_label.setText(_translate("edit_win", "Answer:"))
        self.edit_save_btn.setText(_translate("edit_win", "Save"))
        self.edit_del_btn.setText(_translate("edit_win", "Delete"))
        self.edit_back_btn.setText(_translate("edit_win", "Cancel"))

        self.main_win.setCentralWidget(self.edit_centralwidget)

    def edit_del_btn_clicked(self):
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        cards_parts = re.split("DECK\^\^\$=|QUESTION\^\^\$=|ANSWER\^\^\$=|EASE\^\^\$=|DUE\^\^\$=|INTERVAL\^\^\$=|PHASE\^\^\$=", cards_text.read())
        cards_parts.pop(0)
        cards_text.close()

        # Removes \n.
        for i in range(len(cards_parts)):
            if i % 7 == 6:
                cards_parts[i] = cards_parts[i][:-1]

        cards = []
        for i in range(len(cards_parts)):
            if i % 7 == 6:
                store_list = [cards_parts[i - 6], cards_parts[i - 5], cards_parts[i - 4], cards_parts[i - 3], cards_parts[i - 2], cards_parts[i - 1], cards_parts[i]]
                cards.append(store_list)

        for idx, card in enumerate(cards):
            if card[0] == self.got_card[0] and card[1] == self.got_card[1]:
                cards.pop(idx)

        cards_to_write = []
        for card in cards:
            cards_to_write.append(f"DECK^^$={card[0]}QUESTION^^$={card[1]}ANSWER^^$={card[2]}EASE^^$={card[3]}DUE^^$={card[4]}INTERVAL^^$={card[5]}PHASE^^$={card[6]}\n")

        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "w")
        cards_text.writelines(cards_to_write)
        cards_text.close()

        self.edit_centralwidget.deleteLater()
        self.study_btn_clicked()

    def edit_save_btn_clicked(self):
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        cards_parts = re.split("DECK\^\^\$=|QUESTION\^\^\$=|ANSWER\^\^\$=|EASE\^\^\$=|DUE\^\^\$=|INTERVAL\^\^\$=|PHASE\^\^\$=", cards_text.read())
        cards_parts.pop(0)
        cards_text.close()

        # Removes \n.
        for i in range(len(cards_parts)):
            if i % 7 == 6:
                cards_parts[i] = cards_parts[i][:-1]

        cards = []
        for i in range(len(cards_parts)):
            if i % 7 == 6:
                store_list = [cards_parts[i - 6], cards_parts[i - 5], cards_parts[i - 4], cards_parts[i - 3], cards_parts[i - 2], cards_parts[i - 1], cards_parts[i]]
                cards.append(store_list)

        for card in cards:
            if card[0] == self.got_card[0] and card[1] == self.got_card[1]:
                card[1] = self.edit_qst_text.toPlainText()
                card[2] = self.edit_ans_text.toPlainText()
                break

        cards_to_write = []
        for card in cards:
            cards_to_write.append(
                f"DECK^^$={card[0]}QUESTION^^$={card[1]}ANSWER^^$={card[2]}EASE^^$={card[3]}DUE^^$={card[4]}INTERVAL^^$={card[5]}PHASE^^$={card[6]}\n")

        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "w")
        cards_text.writelines(cards_to_write)
        cards_text.close()

        self.got_card[1] = self.edit_qst_text.toPlainText()
        self.got_card[2] = self.edit_ans_text.toPlainText()

        # As self.study_btn_clicked() will re-get self.got_card, to preserve the card they hit edit on:
        card = self.got_card
        self.edit_centralwidget.deleteLater()
        self.study_btn_clicked()
        self.got_card = card
        self.study_qst_label.setText(self.edit_qst_text.toPlainText())
        self.study_ans_label.setText("")
        self.correct_btn.hide()
        self.again_btn.hide()
        self.show_ans_btn.show()

    def edit_back_btn_clicked(self):
        card = self.got_card
        self.edit_centralwidget.deleteLater()
        self.study_btn_clicked()
        self.got_card = card
        self.study_qst_label.setText(card[1])

    def study_home_btn_clicked(self):

        # Finds how many are due today.
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        cards_parts = re.split("DUE\^\^\$=|INTERVAL\^\^\$=", cards_text.read())
        cards_text.close()
        cards_parts.pop(0)
        num_to_study = 0
        # Removes those not due today.
        end_of_today = str(datetime.datetime.now())
        end_of_today = datetime.datetime(int(end_of_today[:4]), int(end_of_today[5:7]), int(end_of_today[8:10]), 23, 59,
                                         59, 999999)
        for idx, part in enumerate(cards_parts):
            if idx % 2 == 0 and datetime.datetime.strptime(part, "%Y-%m-%d %H:%M:%S.%f") <= end_of_today:
                num_to_study += 1

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_win.sizePolicy().hasHeightForWidth())
        self.main_win.setSizePolicy(sizePolicy)
        self.main_win.setMinimumSize(QtCore.QSize(350, 400))
        self.main_win.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.main_win.setStyleSheet("""
                                        QMainWindow#main_win{
                                            background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(30, 10, 30, 255), stop:1 rgba(60, 10, 60, 255));
                                        }
                                        QScrollBar{
                                            background: transparent;
                                            width: 10px;
                                        }
                                        """)

        self.main_win_centralwidget = QtWidgets.QWidget(self.main_win)
        # Shown at end (stop screen updating).
        self.main_win_centralwidget.hide()
        self.main_win_centralwidget.setObjectName("main_win_centralwidget")
        self.main_win_gridLayout = QtWidgets.QGridLayout(self.main_win_centralwidget)
        self.main_win_gridLayout.setObjectName("main_win_gridLayout")

        self.create_deck_btn = QtWidgets.QPushButton(self.main_win_centralwidget)
        self.create_deck_btn.setObjectName("create_deck_btn")
        self.create_deck_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.create_deck_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.create_deck_btn.setFont(font)
        self.create_deck_btn.setStyleSheet("""
                                                    QPushButton#create_deck_btn{
                                                        background-color:transparent;
                                                        border-radius: 15px;
                                                        border: 1px solid white;
                                                        color: white;
                                                    }
                                                    QPushButton#create_deck_btn:hover{
                                                        background-color: rgba(255, 255, 255, 0.1);
                                                    }
                                                    QPushButton#create_deck_btn:pressed{
                                                        background-color: rgba(255, 255, 255, 0.2);
                                                    }
                                                    """)
        self.create_deck_btn.clicked.connect(lambda: self.create_deck_btn_clicked())
        self.create_deck_btn.setText("Create deck")
        self.main_win_gridLayout.addWidget(self.create_deck_btn, 0, 1, 1, 1)

        self.study_btn = QtWidgets.QPushButton(self.main_win_centralwidget)
        self.study_btn.setObjectName("study_btn")
        self.study_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.study_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.study_btn.setFont(font)
        self.study_btn.setStyleSheet("""
                                            QPushButton#study_btn{
                                                background-color:transparent;
                                                border-radius: 15px;
                                                border: 1px solid white;
                                                color: white;
                                            }
                                            QPushButton#study_btn:hover{
                                                background-color: rgba(255, 255, 255, 0.1);
                                            }
                                            QPushButton#study_btn:pressed{
                                                background-color: rgba(255, 255, 255, 0.2);
                                            }
                                            """)
        if num_to_study < 1000:
            self.study_btn.setText(f"Study {num_to_study}")
        else:
            self.study_btn.setText(f"Study 999+")
        self.study_btn.clicked.connect(lambda: self.study_btn_clicked())
        self.main_win_gridLayout.addWidget(self.study_btn, 1, 1, 1, 1)

        main_win_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_win_gridLayout.addItem(main_win_spacer, 0, 2, 1, 1)

        main_win_spacer1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_win_gridLayout.addItem(main_win_spacer1, 0, 0, 1, 1)

        self.main_win_scrollArea = QtWidgets.QScrollArea(self.main_win_centralwidget)
        self.main_win_scrollArea.setMinimumSize(QtCore.QSize(310, 16777215))
        self.main_win_scrollArea.setMaximumSize(QtCore.QSize(310, 16777215))
        self.main_win_scrollArea.setWidgetResizable(True)
        self.main_win_scrollArea.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.main_win_scrollArea.setObjectName("main_win_scrollArea")
        self.main_win_scrollArea.setStyleSheet("""
                                                        background-color: transparent;
                                                        border: none;
                                                        """)
        self.main_win_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.main_win_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 300, 435))
        self.main_win_scrollAreaWidgetContents.setObjectName("main_win_scrollAreaWidgetContents")
        self.main_win_verticalLayout = QtWidgets.QVBoxLayout(self.main_win_scrollAreaWidgetContents)
        self.main_win_verticalLayout.setObjectName("main_win_verticalLayout")

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "r")
        decks_lines = decks_text.readlines()
        for idx, i in enumerate(decks_lines):
            self.deck_btn = QtWidgets.QPushButton(self.main_win_scrollAreaWidgetContents)
            self.deck_btn.setMinimumSize(QtCore.QSize(282, 40))
            self.deck_btn.setMaximumSize(QtCore.QSize(282, 40))
            self.deck_btn.setFont(font)
            self.deck_btn.setStyleSheet("""
                                                QPushButton#deck_btn{
                                                    background-color: transparent;
                                                    text-align: left;
                                                    color: white;
                                                    border-radius: 15px;
                                                }
                                                QPushButton#deck_btn:hover{
                                                    background-color: rgba(255, 255, 255, 0.1);
                                                }
                                                QPushButton#deck_btn:pressed{
                                                    background-color: rgba(255, 255, 255, 0.2);
                                                }
                                                """)
            self.deck_btn.setObjectName("deck_btn")
            self.deck_btn.setText("  " + i.replace("\n", ""))
            self.main_win_verticalLayout.addWidget(self.deck_btn)
            if idx == 0:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(0))
            if idx == 1:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(1))
            if idx == 2:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(2))
            if idx == 3:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(3))
            if idx == 4:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(4))
            if idx == 5:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(5))
            if idx == 6:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(6))
            if idx == 7:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(7))
            if idx == 8:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(8))
            if idx == 9:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(9))

        decks_text.close()

        main_win_spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_win_verticalLayout.addItem(main_win_spacer2)
        self.main_win_scrollArea.setWidget(self.main_win_scrollAreaWidgetContents)
        self.main_win_gridLayout.addWidget(self.main_win_scrollArea, 2, 1, 1, 1)
        self.create_deck_btn.raise_()
        self.main_win_scrollArea.raise_()
        self.main_win.setCentralWidget(self.main_win_centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self.main_win)

        _translate = QtCore.QCoreApplication.translate
        self.main_win.setWindowTitle(_translate("main_win", "Memory Gain"))
        self.main_win_centralwidget.show()

    def show_ans_btn_clicked(self):
        self.study_ans_label.setText(self.got_card[2])
        self.show_ans_btn.hide()
        self.again_btn.show()
        self.correct_btn.show()

    def correct_btn_clicked(self):
        if self.got_card[6] == "L":
            self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
            self.got_card[6] = "B"
            self.write_card_ac()
        elif self.got_card[6] == "B":
            self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=1440))
            self.got_card[5] = "1440"
            self.got_card[6] = "G"
            self.write_card_ac()
        elif self.got_card[6] == "G":
            self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=int(float(self.got_card[3]) * int(self.got_card[5]))))
            self.got_card[5] = str(int(float(self.got_card[3]) * int(self.got_card[5])))
            self.got_card[6] = "G"
            self.write_card_ac()
        elif self.got_card[6] == "l":
            self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
            self.got_card[6] = "B"
            self.write_card_ac()
        elif self.got_card[6] == "b":
            self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
            self.got_card[6] = "B"
            self.write_card_ac()
        elif self.got_card[6] == "g":
            self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
            self.got_card[6] = "B"
            self.write_card_ac()

        self.get_card()
        if self.got_card:
            self.study_qst_label.setText(self.got_card[1])
            self.study_ans_label.setText("")
            self.correct_btn.hide()
            self.again_btn.hide()
            self.show_ans_btn.show()
        else:
            self.correct_btn.hide()
            self.again_btn.hide()
            self.study_qst_label.setText("Completed.")
            self.study_line.hide()
            self.study_ans_label.hide()
            self.study_edit_btn.hide()

    def again_btn_clicked(self):
        if self.got_card:
            if self.got_card[6] == "l":
                self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=1))
                self.write_card_ac()
            elif self.got_card[6] == "b":
                self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=1))
                self.write_card_ac()
            elif self.got_card[6] == "g":
                self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
                self.write_card_ac()
            elif self.got_card[6] == "L":
                self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=1))
                self.got_card[6] = "l"
                self.write_card_ac()
            elif self.got_card[6] == "B":
                self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=1))
                self.got_card[6] = "b"
                self.write_card_ac()
            elif self.got_card[6] == "G":
                self.got_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
                self.got_card[5] = 0
                if float(self.got_card[3]) > 1.3:
                    self.got_card[3] = str(float(self.got_card[3]) * 0.80)
                    if float(self.got_card[3]) < 1.3:
                        self.got_card[3] = "1.3"
                self.got_card[6] = "g"
                self.write_card_ac()

            self.correct_btn.hide()
            self.again_btn.hide()
            self.show_ans_btn.show()
            self.get_card()
            self.study_qst_label.setText(self.got_card[1])
            self.study_ans_label.setText("")

    def write_card_ac(self):
        # Writes self.got_card to cards.txt if again or correct is pressed.
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        cards_parts = re.split("DECK\^\^\$=|QUESTION\^\^\$=|ANSWER\^\^\$=|EASE\^\^\$=|DUE\^\^\$=|INTERVAL\^\^\$=|PHASE\^\^\$=", cards_text.read())
        cards_parts.pop(0)
        cards_text.close()

        # Removes \n.
        for i in range(len(cards_parts)):
            if i % 7 == 6:
                cards_parts[i] = cards_parts[i][:-1]

        cards = []
        for i in range(len(cards_parts)):
            if i % 7 == 6:
                store_list = [cards_parts[i - 6], cards_parts[i - 5], cards_parts[i - 4], cards_parts[i - 3],
                              cards_parts[i - 2], cards_parts[i - 1], cards_parts[i]]
                cards.append(store_list)

        for card in cards:
            # EASE, DUE, INTERVAL, PHASE.
            if card[0] == self.got_card[0] and card[1] == self.got_card[1]:
                card[3] = self.got_card[3]
                card[4] = self.got_card[4]
                card[5] = self.got_card[5]
                card[6] = self.got_card[6]
                break

        # Writes
        cards_to_write = []
        for card in cards:
            cards_to_write.append(f"DECK^^$={card[0]}QUESTION^^$={card[1]}ANSWER^^$={card[2]}EASE^^$={card[3]}DUE^^$={card[4]}INTERVAL^^$={card[5]}PHASE^^$={card[6]}\n")

        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "w")
        cards_text.writelines(cards_to_write)
        cards_text.close()

    def get_card(self):
        # Everything due today.
        # Over-dues in date order.
        # "l" and "b" due in 30 sec + "g" and "B" due in 3 min, in date order.
        # "L" in date order.
        # "G" in date order.
        # Rest of "l", "b", "g", and "B" in reverse date order.
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        if len(cards_text.read()) == 0:
            self.got_card = False
        else:
            cards_text.seek(0)
            cards_parts = re.split("DECK\^\^\$=|QUESTION\^\^\$=|ANSWER\^\^\$=|EASE\^\^\$=|DUE\^\^\$=|INTERVAL\^\^\$=|PHASE\^\^\$=", cards_text.read())
            cards_parts.pop(0)
            cards_text.close()
            # Removes those not due today.
            end_of_today = str(datetime.datetime.now())
            end_of_today = datetime.datetime(int(end_of_today[:4]), int(end_of_today[5:7]), int(end_of_today[8:10]), 23, 59, 59, 999999)
            i = 0
            while i < len(cards_parts):
                if i % 7 == 4 and datetime.datetime.strptime(cards_parts[i], "%Y-%m-%d %H:%M:%S.%f") > end_of_today:
                    for j in range(7):
                        cards_parts.pop(i - 4)
                    i = i - 4
                else:
                    i += 1

            if len(cards_parts) == 0:
                self.got_card = False
            else:
                # Removes \n.
                for i in range(len(cards_parts)):
                    if i % 7 == 6:
                        cards_parts[i] = cards_parts[i][:-1]

                cards = []
                for i in range(len(cards_parts)):
                    if i % 7 == 6:
                        store_list = [cards_parts[i - 6], cards_parts[i - 5], cards_parts[i - 4], cards_parts[i - 3], cards_parts[i - 2], cards_parts[i - 1], cards_parts[i]]
                        cards.append(store_list)

                # Over-dues in order (earliest to latest) using bubble sort.
                over_dues = []
                for card in cards:
                    if datetime.datetime.strptime(card[4], "%Y-%m-%d %H:%M:%S.%f") < datetime.datetime.now():
                        over_dues.append(card)

                length = len(over_dues)
                while length > 1:
                    for i in range(length - 1):
                        if datetime.datetime.strptime(over_dues[i][4], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.strptime(over_dues[i + 1][4], "%Y-%m-%d %H:%M:%S.%f"):
                            smaller = over_dues[i + 1]
                            over_dues[i + 1] = over_dues[i]
                            over_dues[i] = smaller
                    length -= 1

                if len(over_dues) != 0:
                    self.got_card = over_dues[0]
                else:
                    # "l" and "b" due in 30 sec + "g" and "B" due in 3 min, in order, using bubble sort. THIS IS IF NO OVER-DUES.
                    l_b_list = []
                    g_B_list = []
                    for card in cards:
                        if (card[6] == "l" or card[6] == "b") and (datetime.datetime.strptime(card[4], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.now() < datetime.timedelta(seconds=30)):
                            l_b_list.append(card)

                    for card in cards:
                        if (card[6] == "g" or card[6] == "B") and (datetime.datetime.strptime(card[4], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.now() < datetime.timedelta(seconds=180)):
                            g_B_list.append(card)

                    l_b_g_B_list = l_b_list + g_B_list

                    length = len(l_b_g_B_list)
                    while length > 1:
                        for i in range(length - 1):
                            if datetime.datetime.strptime(l_b_g_B_list[i][4], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.strptime(l_b_g_B_list[i + 1][4], "%Y-%m-%d %H:%M:%S.%f"):
                                smaller = l_b_g_B_list[i + 1]
                                l_b_g_B_list[i + 1] = l_b_g_B_list[i]
                                l_b_g_B_list[i] = smaller
                        length -= 1

                    if len(l_b_g_B_list) != 0:
                        self.got_card = l_b_g_B_list[0]
                    else:
                        # "L" in order. This is  OR "l", or "b"s due in 30 sec and no "g", or "B"s due in 3 min.
                        L_list = []
                        for card in cards:
                            if card[6] == "L":
                                L_list.append(card)

                        length = len(L_list)
                        while length > 1:
                            for i in range(length - 1):
                                if datetime.datetime.strptime(L_list[i][4], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.strptime(L_list[i + 1][4], "%Y-%m-%d %H:%M:%S.%f"):
                                    smaller = L_list[i + 1]
                                    L_list[i + 1] = L_list[i]
                                    L_list[i] = smaller
                            length -= 1

                        if len(L_list) != 0:
                            self.got_card = L_list[0]
                        else:
                            # "G" in order. This is if there are no over-dues; "l" or "b"s due in 30 sec and no "g", or "B"s due in 3 min; and no "L"s.
                            G_list = []
                            for card in cards:
                                if card[6] == "G":
                                    G_list.append(card)

                            length = len(G_list)
                            while length > 1:
                                for i in range(length - 1):
                                    if datetime.datetime.strptime(G_list[i][4], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.strptime(G_list[i + 1][4], "%Y-%m-%d %H:%M:%S.%f"):
                                        smaller = G_list[i + 1]
                                        G_list[i + 1] = G_list[i]
                                        G_list[i] = smaller
                                length -= 1

                            if len(G_list) != 0:
                                self.got_card = G_list[0]
                            else:
                                # "l", "b", "g", and "B" in reverse order. This is if there are no over-dues; "l" or "b"s due in 30 sec and no "g" or "B"s due in 3 min; "L"s; or "G"s.
                                l_b_g_B_rev_list = []
                                for card in cards:
                                    if card[6] == "l" or card[6] == "b" or card[6] == "g" or card[6] == "B":
                                        l_b_g_B_rev_list.append(card)

                                # This sorts from earliest to latest but takes the last one.
                                length = len(l_b_g_B_rev_list)
                                while length > 1:
                                    for i in range(length - 1):
                                        if datetime.datetime.strptime(l_b_g_B_rev_list[i][4], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.strptime(l_b_g_B_rev_list[i + 1][4], "%Y-%m-%d %H:%M:%S.%f"):
                                            smaller = l_b_g_B_rev_list[i + 1]
                                            l_b_g_B_rev_list[i + 1] = l_b_g_B_rev_list[i]
                                            l_b_g_B_rev_list[i] = smaller
                                    length -= 1
                                if len(l_b_g_B_rev_list) != 0:
                                    self.got_card = l_b_g_B_rev_list[-1]

    def deck_btn_clicked(self, idx):
        # Clears main_win.
        self.main_win_scrollArea.deleteLater()
        self.study_btn.deleteLater()
        self.create_deck_btn.deleteLater()

        # Closes Create deck window.
        self.create_deck_win = QtWidgets.QWidget()
        self.create_deck_win.close()

        decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "r")
        deck = decks_text.readlines()[idx].replace("\n", "")
        decks_text.close()

        self.deck_win_verticalLayout = QtWidgets.QVBoxLayout()
        self.deck_win_verticalLayout.setObjectName("deck_win_verticalLayout")

        self.deck_label = QtWidgets.QLabel()
        self.deck_label.setMinimumSize(QtCore.QSize(300, 40))
        self.deck_label.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.deck_label.setFont(font)
        self.deck_label.setStyleSheet("""
                                    QLabel#deck_label{
                                        color:white;
                                    }
                                    """)
        self.deck_label.setAlignment(QtCore.Qt.AlignCenter)
        self.deck_label.setObjectName("deck_label")
        self.deck_win_verticalLayout.addWidget(self.deck_label)

        self.add_cards_btn = QtWidgets.QPushButton()
        self.add_cards_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.add_cards_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_cards_btn.setFont(font)
        self.add_cards_btn.setStyleSheet("""
                                        QPushButton#add_cards_btn{
                                            background-color: transparent;
                                            border-radius: 15px;
                                            border: 1px solid white;
                                            color: white;
                                        }
                                        QPushButton#add_cards_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#add_cards_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.add_cards_btn.setObjectName("add_cards_btn")
        self.deck_win_verticalLayout.addWidget(self.add_cards_btn)
        self.add_cards_btn.clicked.connect(lambda: self.add_cards_btn_clicked(deck))

        self.search_deck_btn = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_deck_btn.sizePolicy().hasHeightForWidth())
        self.search_deck_btn.setSizePolicy(sizePolicy)
        self.search_deck_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.search_deck_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.search_deck_btn.setFont(font)
        self.search_deck_btn.setStyleSheet("""
                                        QPushButton#search_deck_btn{
                                            background-color: transparent;
                                            border-radius: 15px;
                                            border: 1px solid white;
                                            color: white;
                                        }
                                        QPushButton#search_deck_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#search_deck_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.search_deck_btn.setObjectName("search_deck_btn")
        self.deck_win_verticalLayout.addWidget(self.search_deck_btn)
        self.search_deck_btn.clicked.connect(lambda: self.search_deck_btn_clicked(deck))

        self.del_deck_btn = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.del_deck_btn.sizePolicy().hasHeightForWidth())
        self.del_deck_btn.setSizePolicy(sizePolicy)
        self.del_deck_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.del_deck_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.del_deck_btn.setFont(font)
        self.del_deck_btn.setStyleSheet("""
                                        QPushButton#del_deck_btn{
                                            background-color: transparent;
                                            border-radius: 15px;
                                            border: 1px solid white;
                                            color: white;
                                        }
                                        QPushButton#del_deck_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#del_deck_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.del_deck_btn.setObjectName("del_deck_btn")
        self.deck_win_verticalLayout.addWidget(self.del_deck_btn)
        self.del_deck_btn.clicked.connect(lambda: self.del_deck_btn_clicked(deck))

        self.back_decks_btn = QtWidgets.QPushButton()
        self.back_decks_btn.setMinimumSize(QtCore.QSize(300, 35))
        self.back_decks_btn.setMaximumSize(QtCore.QSize(300, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.back_decks_btn.setFont(font)
        self.back_decks_btn.setStyleSheet("""
                                        QPushButton#back_decks_btn{
                                            background-color: transparent;
                                            border-radius: 15px;
                                            border: 1px solid white;
                                            color: white;
                                        }
                                        QPushButton#back_decks_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#back_decks_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.back_decks_btn.setObjectName("back_decks_btn")
        self.deck_win_verticalLayout.addWidget(self.back_decks_btn)
        self.back_decks_btn.clicked.connect(lambda: self.back_decks_btn_clicked())

        self.main_win_gridLayout.addLayout(self.deck_win_verticalLayout, 1, 1, 1, 1)

        _translate = QtCore.QCoreApplication.translate
        self.main_win.setWindowTitle(f"{deck} deck")
        self.deck_label.setText(f"{deck}")
        self.add_cards_btn.setText(_translate("deck_win", "Add cards"))
        self.search_deck_btn.setText(_translate("deck_win", "Search"))
        self.del_deck_btn.setText(_translate("deck_win", "Delete"))
        self.back_decks_btn.setText(_translate("deck_win", "Home"))

        self.main_win.setWindowIcon(QtGui.QIcon("feather\\layers.svg"))

    def del_deck_btn_clicked(self, deck):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle("Confirmation")
        self.msg.setText(f"Are you sure you want to delete the {deck} deck, and all cards associated with the {deck} deck? ")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        self.msg.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        self.msg.buttonClicked.connect(lambda: self.del_deck_msg_clicked(self.msg.clickedButton(), deck))
        self.msg.exec_()

    def del_deck_msg_clicked(self, btn, deck):
        if btn.text() == "OK":

            decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "r")
            decks_lines = decks_text.readlines()
            index = decks_lines.index(deck + "\n")
            decks_lines.pop(index)
            decks_text.close()

            decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "w")
            decks_text.writelines(decks_lines)
            decks_text.close()

            cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
            cards_parts = re.split("DECK\^\^\$=|QUESTION\^\^\$=|ANSWER\^\^\$=|EASE\^\^\$=|DUE\^\^\$=|INTERVAL\^\^\$=|PHASE\^\^\$=", cards_text.read())
            cards_parts.pop(0)
            cards_text.close()

            # Removes \n.
            for i in range(len(cards_parts)):
                if i % 7 == 6:
                    cards_parts[i] = cards_parts[i][:-1]

            cards = []
            for i in range(len(cards_parts)):
                if i % 7 == 6:
                    store_list = [cards_parts[i - 6], cards_parts[i - 5], cards_parts[i - 4], cards_parts[i - 3], cards_parts[i - 2], cards_parts[i - 1], cards_parts[i]]
                    cards.append(store_list)

            # Writes.
            cards_to_write = []
            for card in cards:
                if card[0] != deck:
                    cards_to_write.append(f"DECK^^$={card[0]}QUESTION^^$={card[1]}ANSWER^^$={card[2]}EASE^^$={card[3]}DUE^^$={card[4]}INTERVAL^^$={card[5]}PHASE^^$={card[6]}\n")

            cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "w")
            cards_text.writelines(cards_to_write)
            cards_text.close()

            #Clears the deck layout.
            self.deck_label.deleteLater()
            self.search_deck_btn.deleteLater()
            self.search_deck_btn.deleteLater()
            self.back_decks_btn.deleteLater()
            self.del_deck_btn.deleteLater()
            self.add_cards_btn.deleteLater()

            ######################################### Re-draws main_win ###################################################
            # Finds how many are due today.
            cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
            cards_parts = re.split("DUE\^\^\$=|INTERVAL\^\^\$=", cards_text.read())
            cards_text.close()
            cards_parts.pop(0)
            num_to_study = 0
            # Removes those not due today.
            end_of_today = str(datetime.datetime.now())
            end_of_today = datetime.datetime(int(end_of_today[:4]), int(end_of_today[5:7]), int(end_of_today[8:10]), 23,
                                             59,
                                             59, 999999)
            for idx, part in enumerate(cards_parts):
                if idx % 2 == 0 and datetime.datetime.strptime(part, "%Y-%m-%d %H:%M:%S.%f") <= end_of_today:
                    num_to_study += 1

            self.main_win_centralwidget = QtWidgets.QWidget(self.main_win)
            self.main_win_centralwidget.setObjectName("main_win_centralwidget")
            self.main_win_gridLayout = QtWidgets.QGridLayout(self.main_win_centralwidget)
            self.main_win_gridLayout.setObjectName("main_win_gridLayout")

            self.create_deck_btn = QtWidgets.QPushButton(self.main_win_centralwidget)
            self.create_deck_btn.setObjectName("create_deck_btn")
            self.create_deck_btn.setMinimumSize(QtCore.QSize(300, 40))
            self.create_deck_btn.setMaximumSize(QtCore.QSize(300, 40))
            font = QtGui.QFont()
            font.setFamily("Verdana")
            font.setPointSize(12)
            self.create_deck_btn.setFont(font)
            self.create_deck_btn.setStyleSheet("""
                                                                        QPushButton#create_deck_btn{
                                                                            background-color:transparent;
                                                                            border-radius: 15px;
                                                                            border: 1px solid white;
                                                                            color: white;
                                                                        }
                                                                        QPushButton#create_deck_btn:hover{
                                                                            background-color: rgba(255, 255, 255, 0.1);
                                                                        }
                                                                        QPushButton#create_deck_btn:pressed{
                                                                            background-color: rgba(255, 255, 255, 0.2);
                                                                        }
                                                                        """)
            self.create_deck_btn.clicked.connect(lambda: self.create_deck_btn_clicked())
            self.create_deck_btn.setText("Create deck")
            self.main_win_gridLayout.addWidget(self.create_deck_btn, 0, 1, 1, 1)

            self.study_btn = QtWidgets.QPushButton(self.main_win_centralwidget)
            self.study_btn.setObjectName("study_btn")
            self.study_btn.setMinimumSize(QtCore.QSize(300, 40))
            self.study_btn.setMaximumSize(QtCore.QSize(300, 40))
            font = QtGui.QFont()
            font.setFamily("Verdana")
            font.setPointSize(12)
            self.study_btn.setFont(font)
            self.study_btn.setStyleSheet("""
                                                                QPushButton#study_btn{
                                                                    background-color:transparent;
                                                                    border-radius: 15px;
                                                                    border: 1px solid white;
                                                                    color: white;
                                                                }
                                                                QPushButton#study_btn:hover{
                                                                    background-color: rgba(255, 255, 255, 0.1);
                                                                }
                                                                QPushButton#study_btn:pressed{
                                                                    background-color: rgba(255, 255, 255, 0.2);
                                                                }
                                                                """)
            if num_to_study < 1000:
                self.study_btn.setText(f"Study {num_to_study}")
            else:
                self.study_btn.setText(f"Study 999+")
            self.study_btn.clicked.connect(lambda: self.study_btn_clicked())
            self.main_win_gridLayout.addWidget(self.study_btn, 1, 1, 1, 1)

            main_win_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Minimum)
            self.main_win_gridLayout.addItem(main_win_spacer, 0, 2, 1, 1)

            main_win_spacer1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                     QtWidgets.QSizePolicy.Minimum)
            self.main_win_gridLayout.addItem(main_win_spacer1, 0, 0, 1, 1)

            self.main_win_scrollArea = QtWidgets.QScrollArea(self.main_win_centralwidget)
            self.main_win_scrollArea.setMinimumSize(QtCore.QSize(310, 16777215))
            self.main_win_scrollArea.setMaximumSize(QtCore.QSize(310, 16777215))
            self.main_win_scrollArea.setWidgetResizable(True)
            self.main_win_scrollArea.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
            self.main_win_scrollArea.setObjectName("main_win_scrollArea")
            self.main_win_scrollArea.setStyleSheet("""
                                                                            background-color: transparent;
                                                                            border: none;
                                                                            """)
            self.main_win_scrollAreaWidgetContents = QtWidgets.QWidget()
            self.main_win_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 300, 435))
            self.main_win_scrollAreaWidgetContents.setObjectName("main_win_scrollAreaWidgetContents")
            self.main_win_verticalLayout = QtWidgets.QVBoxLayout(self.main_win_scrollAreaWidgetContents)
            self.main_win_verticalLayout.setObjectName("main_win_verticalLayout")

            font = QtGui.QFont()
            font.setFamily("Verdana")
            font.setPointSize(12)
            decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "r")
            decks_lines = decks_text.readlines()
            for idx, i in enumerate(decks_lines):
                self.deck_btn = QtWidgets.QPushButton(self.main_win_scrollAreaWidgetContents)
                self.deck_btn.setMinimumSize(QtCore.QSize(282, 40))
                self.deck_btn.setMaximumSize(QtCore.QSize(282, 40))
                self.deck_btn.setFont(font)
                self.deck_btn.setStyleSheet("""
                                                                    QPushButton#deck_btn{
                                                                        background-color: transparent;
                                                                        text-align: left;
                                                                        color: white;
                                                                        border-radius: 15px;
                                                                    }
                                                                    QPushButton#deck_btn:hover{
                                                                        background-color: rgba(255, 255, 255, 0.1);
                                                                    }
                                                                    QPushButton#deck_btn:pressed{
                                                                        background-color: rgba(255, 255, 255, 0.2);
                                                                    }
                                                                    """)
                self.deck_btn.setObjectName("deck_btn")
                self.deck_btn.setText("  " + i.replace("\n", ""))
                self.main_win_verticalLayout.addWidget(self.deck_btn)
                if idx == 0:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(0))
                if idx == 1:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(1))
                if idx == 2:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(2))
                if idx == 3:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(3))
                if idx == 4:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(4))
                if idx == 5:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(5))
                if idx == 6:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(6))
                if idx == 7:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(7))
                if idx == 8:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(8))
                if idx == 9:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(9))
            decks_text.close()

            main_win_spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                     QtWidgets.QSizePolicy.Expanding)
            self.main_win_verticalLayout.addItem(main_win_spacer2)
            self.main_win_scrollArea.setWidget(self.main_win_scrollAreaWidgetContents)
            self.main_win_gridLayout.addWidget(self.main_win_scrollArea, 2, 1, 1, 1)
            self.create_deck_btn.raise_()
            self.main_win_scrollArea.raise_()
            self.main_win.setCentralWidget(self.main_win_centralwidget)

            QtCore.QMetaObject.connectSlotsByName(self.main_win)

            _translate = QtCore.QCoreApplication.translate
            self.main_win.setWindowTitle(_translate("main_win", "Memory Gain"))
            self.main_win.setWindowIcon(QtGui.QIcon("feather\\layers.svg"))

    def search_deck_btn_clicked(self, deck):
        self.search_win = QtWidgets.QWidget()
        self.search_win.setWindowTitle(f"Search {deck}")
        self.search_win.setObjectName("search_win")
        self.search_win.resize(700, 500)
        self.search_win.setStyleSheet("""
                                        QWidget#search_win{
                                            background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(40, 10, 40, 255), stop:1 rgba(20, 0, 20, 255));
                                        }
                                        QScrollBar{
                                            background: transparent;
                                            width: 10px;
                                        }
                                        """)
        self.search_win_gridLayout = QtWidgets.QGridLayout(self.search_win)
        self.search_win_gridLayout.setObjectName("search_win_gridLayout")
        self.search_win_verticalLayout = QtWidgets.QVBoxLayout()
        self.search_win_verticalLayout.setObjectName("search_win_verticalLayout")
        self.search_win_horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.search_win_horizontalLayout_2.setObjectName("search_win_horizontalLayout_2")

        self.input_search = QtWidgets.QLineEdit(self.search_win)
        self.input_search.setMinimumSize(QtCore.QSize(400, 40))
        self.input_search.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.input_search.setFont(font)
        self.input_search.setObjectName("input_search")
        self.input_search.setStyleSheet("""
                                        QLineEdit#input_search{
                                            background-color: rgba(255, 255, 255, 0.1);
                                            border-radius: 15px;
                                            padding-left: 5px;
                                            padding-right: 5px;
                                            color: white;
                                        }
                                        """)
        self.search_win_horizontalLayout_2.addWidget(self.input_search)

        self.search_btn = QtWidgets.QPushButton(self.search_win)
        self.search_btn.setMinimumSize(QtCore.QSize(150, 40))
        self.search_btn.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.search_btn.setFont(font)
        self.search_btn.setStyleSheet("""
                                    QPushButton#search_btn{
                                        background-color: transparent;
                                        text-align: left;
                                        color: white;
                                        border-radius: 15px;
                                        border: 1px solid white;
                                        text-align: center;
                                    }
                                    QPushButton#search_btn:hover{
                                        background-color: rgba(255, 255, 255, 0.1);
                                    }
                                    QPushButton#search_btn:pressed{
                                        background-color: rgba(255, 255, 255, 0.2);
                                    }
                                    """)
        self.search_btn.setObjectName("search_btn")
        self.search_win_horizontalLayout_2.addWidget(self.search_btn)
        self.search_btn.clicked.connect(lambda: self.search_btn_clicked(deck))
        self.search_win_verticalLayout.addLayout(self.search_win_horizontalLayout_2)
        self.search_btn.setText("Search")

        self.search_win_horizontalLayout = QtWidgets.QHBoxLayout()
        self.search_win_horizontalLayout.setObjectName("search_win_horizontalLayout")

        self.search_win_verticalLayout.addLayout(self.search_win_horizontalLayout_2)
        self.search_win_gridLayout.addLayout(self.search_win_verticalLayout, 1, 1, 1, 1)

        self.search_win.setWindowIcon(QtGui.QIcon("feather\\search.svg"))

        QtCore.QMetaObject.connectSlotsByName(self.search_win)
        self.search_win.show()
        self.showing = False

    def search_btn_clicked(self, deck):
        self.search_query = self.input_search.text()
        self.search_page = 1
        self.search_upto = 0

        # Check query exists.
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        cards = re.split("QUESTION\^\^\$=|ANSWER\^\^\$=|EASE\^\^\$=", cards_text.read())
        cards.pop(0)
        is_in = False
        for i in range(len(cards)):
            if i % 3 == 0 or i % 3 == 1:
                if self.search_query in cards[i]:
                    is_in = True
        cards_text.close()

        if is_in:
            cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
            self.search_card_idxs = []
            cards = cards_text.read().split("DECK^^$=")
            cards.pop(0)
            cards_deck_and_rest = []
            for i in range(len(cards)):
                cards_deck_and_rest.append(cards[i][:cards[i].index("QUESTION^^$=")])
                cards_deck_and_rest.append(cards[i][cards[i].index("QUESTION^^$="):])
            for i in range(len(cards)):
                if deck == cards_deck_and_rest[i*2]:
                    qst_onwards = cards_deck_and_rest[i*2 + 1].split("QUESTION^^$=")
                    qst = qst_onwards[1].split("ANSWER^^$=")[0]
                    ans = qst_onwards[1].split("ANSWER^^$=")[1].split("EASE^^$=")[0]
                    if self.search_query in qst or self.search_query in ans:
                        self.search_card_idxs.append(i)

            if len(self.search_card_idxs) != 0:
                qst_onwards = cards[self.search_card_idxs[self.search_upto]].split("QUESTION^^$=")
                qst = qst_onwards[1].split("ANSWER^^$=")[0]
                ans = qst_onwards[1].split("ANSWER^^$=")[1].split("EASE^^$=")[0]

            cards_text.close()

            if (not self.showing) and (len(self.search_card_idxs) != 0):
                self.search_qst_label = QtWidgets.QLabel(self.search_win)
                self.search_qst_label.setMinimumSize(QtCore.QSize(140, 25))
                self.search_qst_label.setMaximumSize(QtCore.QSize(140, 25))
                font = QtGui.QFont("Verdana")
                font.setPointSize(12)
                self.search_qst_label.setFont(font)
                self.search_qst_label.setStyleSheet("color:white;\n"
                                                    "border:none;")
                self.search_qst_label.setObjectName("search_qst_label")
                self.search_win_verticalLayout.addWidget(self.search_qst_label)
                self.search_qst_label.setText("Question:")

                self.search_qst_text = QtWidgets.QTextEdit(self.search_win)
                font = QtGui.QFont("Verdana")
                font.setPointSize(12)
                self.search_qst_text.setFont(font)
                self.search_qst_text.setStyleSheet("""
                                                    background-color: rgba(255, 255, 255, 0.1);
                                                    border-radius:15px;
                                                    padding:5px;
                                                    color: white;
                                                    """)
                self.search_qst_text.setObjectName("search_qst_text")
                self.search_win_verticalLayout.addWidget(self.search_qst_text)

                self.search_ans_label = QtWidgets.QLabel(self.search_win)
                self.search_ans_label.setMinimumSize(QtCore.QSize(140, 25))
                self.search_ans_label.setMaximumSize(QtCore.QSize(140, 25))
                font = QtGui.QFont("Verdana")
                font.setPointSize(12)
                self.search_ans_label.setFont(font)
                self.search_ans_label.setStyleSheet("color:white;\n"
                                                    "border:none;")
                self.search_ans_label.setObjectName("search_ans_label")
                self.search_win_verticalLayout.addWidget(self.search_ans_label)
                self.search_ans_label.setText("Answer:")

                self.search_ans_text = QtWidgets.QTextEdit(self.search_win)
                font = QtGui.QFont("Verdana")
                font.setPointSize(12)
                self.search_ans_text.setFont(font)
                self.search_ans_text.setStyleSheet("""
                                                   background-color: rgba(255, 255, 255, 0.1);
                                                   border-radius:15px;
                                                   padding:5px;
                                                   color: white;
                                                   """)
                self.search_ans_text.setObjectName("search_ans_text")
                self.search_win_verticalLayout.addWidget(self.search_ans_text)

                self.search_save_btn = QtWidgets.QPushButton(self.search_win)
                self.search_save_btn.setMinimumSize(QtCore.QSize(200, 40))
                self.search_save_btn.setMaximumSize(QtCore.QSize(200, 40))
                font = QtGui.QFont("Verdana")
                font.setPointSize(12)
                self.search_save_btn.setFont(font)
                self.search_save_btn.setStyleSheet("""
                                                    QPushButton#search_save_btn{
                                                        background-color: transparent;
                                                        text-align: left;
                                                        color: white;
                                                        border-radius: 15px;
                                                        border: 1px solid white;
                                                        text-align: center;
                                                    }
                                                    QPushButton#search_save_btn:hover{
                                                        background-color: rgba(255, 255, 255, 0.1);
                                                    }
                                                    QPushButton#search_save_btn:pressed{
                                                        background-color: rgba(255, 255, 255, 0.2);
                                                    }
                                                    """)
                self.search_save_btn.setObjectName("search_save_btn")
                self.search_win_horizontalLayout.addWidget(self.search_save_btn)
                self.search_save_btn.setText("Save")
                self.search_save_btn.clicked.connect(lambda: self.search_save_btn_clicked())

                self.search_del_btn = QtWidgets.QPushButton(self.search_win)
                self.search_del_btn.setMinimumSize(QtCore.QSize(200, 40))
                self.search_del_btn.setMaximumSize(QtCore.QSize(200, 40))
                font = QtGui.QFont("Verdana")
                font.setPointSize(12)
                self.search_del_btn.setFont(font)
                self.search_del_btn.setStyleSheet("""
                                                QPushButton#search_del_btn{
                                                    background-color: transparent;
                                                    text-align: left;
                                                    color: white;
                                                    border-radius: 15px;
                                                    border: 1px solid white;
                                                    text-align: center;
                                                }
                                                QPushButton#search_del_btn:hover{
                                                    background-color: rgba(255, 255, 255, 0.1);
                                                }
                                                QPushButton#search_del_btn:pressed{
                                                    background-color: rgba(255, 255, 255, 0.2);
                                                }
                                                """)
                self.search_del_btn.setObjectName("search_del_btn")
                self.search_win_horizontalLayout.addWidget(self.search_del_btn)
                self.search_del_btn.setText("Delete")
                self.search_del_btn.clicked.connect(lambda: self.search_del_btn_clicked(deck))

                spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.search_win_horizontalLayout.addItem(spacerItem1)

                self.search_left_btn = QtWidgets.QPushButton(self.search_win)
                self.search_left_btn.setMinimumSize(QtCore.QSize(70, 40))
                self.search_left_btn.setMaximumSize(QtCore.QSize(70, 40))
                font = QtGui.QFont("Verdana")
                font.setPointSize(12)
                self.search_left_btn.setFont(font)
                self.search_left_btn.setStyleSheet("""
                                                QPushButton#search_left_btn{
                                                    background-color: transparent;
                                                    text-align: left;
                                                    color: white;
                                                    border-radius: 15px;
                                                    border: 1px solid white;
                                                    text-align: center;
                                                }
                                                QPushButton#search_left_btn:hover{
                                                    background-color: rgba(255, 255, 255, 0.1);
                                                }
                                                QPushButton#search_left_btn:pressed{
                                                    background-color: rgba(255, 255, 255, 0.2);
                                                }
                                                """)
                self.search_left_btn.setText("")
                icon3 = QtGui.QIcon()
                icon3.addPixmap(QtGui.QPixmap("feather_white\\chevron-left.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.search_left_btn.setIcon(icon3)
                self.search_left_btn.setIconSize(QtCore.QSize(22, 22))
                self.search_left_btn.setObjectName("search_left_btn")
                self.search_win_horizontalLayout.addWidget(self.search_left_btn)
                self.search_left_btn.clicked.connect(lambda: self.search_left_btn_clicked())

                self.card_of_card_label = QtWidgets.QLabel(self.search_win)
                self.card_of_card_label.setMinimumSize(QtCore.QSize(100, 40))
                self.card_of_card_label.setMaximumSize(QtCore.QSize(100, 40))
                font = QtGui.QFont("Verdana")
                font.setPointSize(12)
                self.card_of_card_label.setFont(font)
                self.card_of_card_label.setStyleSheet("color:white;\n"
                                                      "border:none;")
                self.card_of_card_label.setAlignment(QtCore.Qt.AlignCenter)
                self.card_of_card_label.setObjectName("card_of_card_label")
                self.search_win_horizontalLayout.addWidget(self.card_of_card_label)

                self.search_right_btn = QtWidgets.QPushButton(self.search_win)
                self.search_right_btn.setMinimumSize(QtCore.QSize(70, 40))
                self.search_right_btn.setMaximumSize(QtCore.QSize(70, 40))
                font = QtGui.QFont("Verdana")
                font.setPointSize(12)
                self.search_right_btn.setFont(font)
                self.search_right_btn.setStyleSheet("""
                                                    QPushButton#search_right_btn{
                                                        background-color: transparent;
                                                        text-align: left;
                                                        color: white;
                                                        border-radius: 15px;
                                                        border: 1px solid white;
                                                        text-align: center;
                                                    }
                                                    QPushButton#search_right_btn:hover{
                                                        background-color: rgba(255, 255, 255, 0.1);
                                                    }
                                                    QPushButton#search_right_btn:pressed{
                                                        background-color: rgba(255, 255, 255, 0.2);
                                                    }
                                                    """)
                self.search_right_btn.setText("")
                icon4 = QtGui.QIcon()
                icon4.addPixmap(QtGui.QPixmap("feather_white\\chevron-right.svg"),
                                QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.search_right_btn.setIcon(icon4)
                self.search_right_btn.setIconSize(QtCore.QSize(22, 22))
                self.search_right_btn.setObjectName("search_right_btn")
                self.search_win_horizontalLayout.addWidget(self.search_right_btn)
                self.search_right_btn.clicked.connect(lambda: self.search_right_btn_clicked())

                self.search_win_verticalLayout.addLayout(self.search_win_horizontalLayout)
                self.search_win_gridLayout.addLayout(self.search_win_verticalLayout, 1, 1, 1, 1)
                self.showing = True

                self.search_qst_text.setText(qst)
                self.search_ans_text.setText(ans)
                self.card_of_card_label.setText(f"{self.search_page} of {len(self.search_card_idxs)}")

            elif len(self.search_card_idxs) != 0:
                self.search_qst_text.setText(qst)
                self.search_ans_text.setText(ans)
                self.card_of_card_label.setText(f"{self.search_page} of {len(self.search_card_idxs)}")

            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Not found")
                center = QDesktopWidget().availableGeometry().center()
                msg.move(center)
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("No card with that text was found.")
                msg.exec_()

        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Not found")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("No card with that text was found.")
            msg.exec_()

    def search_save_btn_clicked(self):
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        num_of_cards = len(cards_text.read().split("DECK^^$=")) - 1
        cards_text.seek(0)
        cards_parts = re.split("DECK\^\^\$=|QUESTION\^\^\$=|ANSWER\^\^\$=|EASE\^\^\$=", cards_text.read())
        cards_parts.pop(0)
        # Math is relevant to the splitting.
        qst_idx = self.search_card_idxs[self.search_upto] * 4 + 1
        cards_parts[qst_idx] = self.search_qst_text.toPlainText().strip()
        cards_parts[qst_idx + 1] = self.search_ans_text.toPlainText().strip()
        cards_text.close()

        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "w")
        cards_parts_f = []
        for i in range(num_of_cards):
            n = i * 4
            cards_parts_f.append(f"DECK^^$={cards_parts[n]}QUESTION^^$={cards_parts[n + 1]}ANSWER^^$={cards_parts[n + 2]}EASE^^$={cards_parts[n + 3]}")
        cards_text.writelines(cards_parts_f)
        cards_text.close()

    def search_del_btn_clicked(self, deck):
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        cards = cards_text.read().split("DECK^^$=")
        cards.pop(0)
        cards.pop(self.search_card_idxs[self.search_upto])
        cards_text.close()
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "w")
        for idx, i in enumerate(cards):
            cards[idx] = "DECK^^$=" + i
        cards_text.writelines(cards)
        cards_text.close()
        if len(self.search_card_idxs) == 1:
            self.search_win.close()
        else:
            self.search_btn_clicked(deck)

    def search_right_btn_clicked(self):
        if self.search_page != len(self.search_card_idxs):
            self.search_page += 1
            self.search_upto += 1

            cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
            cards = cards_text.read().split("DECK^^$=")
            cards.pop(0)

            qst_onwards = cards[self.search_card_idxs[self.search_upto]].split("QUESTION^^$=")
            qst = qst_onwards[1].split("ANSWER^^$=")[0]
            ans = qst_onwards[1].split("ANSWER^^$=")[1].split("EASE^^$=")[0]

            self.search_qst_text.setText(qst)
            self.search_ans_text.setText(ans)
            self.card_of_card_label.setText(f"{self.search_page} of {len(self.search_card_idxs)}")

            cards_text.close()

    def search_left_btn_clicked(self):
        if self.search_page != 1:
            self.search_page -= 1
            self.search_upto -= 1

            cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
            cards = cards_text.read().split("DECK^^$=")
            cards.pop(0)

            qst_onwards = cards[self.search_card_idxs[self.search_upto]].split("QUESTION^^$=")
            qst = qst_onwards[1].split("ANSWER^^$=")[0]
            ans = qst_onwards[1].split("ANSWER^^$=")[1].split("EASE^^$=")[0]

            self.search_qst_text.setText(qst)
            self.search_ans_text.setText(ans)
            self.card_of_card_label.setText(f"{self.search_page} of {len(self.search_card_idxs)}")

            cards_text.close()

    def add_cards_btn_clicked(self, deck):
        self.add_cards_win = QtWidgets.QWidget()
        self.add_cards_win.setObjectName("add_cards_win")
        self.add_cards_win.resize(700, 500)
        self.add_cards_win.setStyleSheet("""
                                        QWidget#add_cards_win{
                                            background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(40, 10, 40, 255), stop:1 rgba(20, 0, 20, 255));;
                                        }
                                        QScrollBar{
                                           background: transparent;
                                           width: 10px;
                                        }
                                        """)
        self.add_cards_gridLayout = QtWidgets.QGridLayout(self.add_cards_win)
        self.add_cards_gridLayout.setObjectName("add_cards_gridLayout")
        self.add_cards_verticalLayout = QtWidgets.QVBoxLayout()
        self.add_cards_verticalLayout.setObjectName("add_cards_verticalLayout")
        self.qst_label = QtWidgets.QLabel(self.add_cards_win)
        font = QtGui.QFont("Verdana")
        font.setPointSize(12)
        self.qst_label.setFont(font)
        self.qst_label.setStyleSheet("""
                                    color: white;
                                    """)
        self.qst_label.setObjectName("qst_label")
        self.add_cards_verticalLayout.addWidget(self.qst_label)

        self.input_qst = QtWidgets.QTextEdit(self.add_cards_win)
        font = QtGui.QFont("Verdana")
        font.setPointSize(12)
        self.input_qst.setFont(font)
        self.input_qst.setStyleSheet("""
                                    background-color: rgba(255, 255, 255, 0.1);
                                    border-radius:10px;
                                    padding: 5px;
                                    color: white;
                                    """)
        self.input_qst.setObjectName("input_qst")
        self.add_cards_verticalLayout.addWidget(self.input_qst)

        self.ans_label = QtWidgets.QLabel(self.add_cards_win)
        font = QtGui.QFont("Verdana")
        font.setPointSize(12)
        self.ans_label.setFont(font)
        self.ans_label.setStyleSheet("color:white;")
        self.ans_label.setObjectName("ans_label")
        self.add_cards_verticalLayout.addWidget(self.ans_label)

        self.input_ans = QtWidgets.QTextEdit(self.add_cards_win)
        font = QtGui.QFont("Verdana")
        font.setPointSize(12)
        self.input_ans.setFont(font)
        self.input_ans.setStyleSheet("""
                                    background-color: rgba(255, 255, 255, 0.1);
                                    border-radius:10px;
                                    padding: 5px;
                                    color: white;
                                    """)
        self.input_ans.setObjectName("input_ans")
        self.add_cards_verticalLayout.addWidget(self.input_ans)

        self.add_cards_horizontalLayout = QtWidgets.QHBoxLayout()
        self.add_cards_horizontalLayout.setObjectName("add_cards_horizontalLayout")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.add_cards_horizontalLayout.addItem(spacerItem)

        self.add_card_btn = QtWidgets.QPushButton(self.add_cards_win)
        self.add_card_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.add_card_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont("Verdana")
        font.setPointSize(12)
        self.add_card_btn.setFont(font)
        self.add_card_btn.setStyleSheet("""
                                        QPushButton#add_card_btn{
                                            background-color: transparent;
                                            text-align: left;
                                            color: white;
                                            border-radius: 15px;
                                            border: 1px solid white;
                                            text-align: center;
                                        }
                                        QPushButton#add_card_btn:hover{
                                            background-color: rgba(255, 255, 255, 0.1);
                                        }
                                        QPushButton#add_card_btn:pressed{
                                            background-color: rgba(255, 255, 255, 0.2);
                                        }
                                        """)
        self.add_card_btn.setObjectName("add_card_btn")
        self.add_cards_horizontalLayout.addWidget(self.add_card_btn)
        self.add_card_btn.clicked.connect(lambda: self.add_card_btn_clicked(deck))

        self.add_cards_verticalLayout.addLayout(self.add_cards_horizontalLayout)
        self.add_cards_gridLayout.addLayout(self.add_cards_verticalLayout, 1, 1, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.add_cards_horizontalLayout.addItem(spacerItem1)

        QtCore.QMetaObject.connectSlotsByName(self.add_cards_win)

        _translate = QtCore.QCoreApplication.translate
        self.add_cards_win.setWindowTitle(_translate("add_cards_win", "Add cards"))
        self.qst_label.setText(_translate("add_cards_win", "Question:"))
        self.ans_label.setText(_translate("add_cards_win", "Answer:"))
        self.add_card_btn.setText(_translate("add_cards_win", "Add"))
        self.add_cards_win.show()

        self.add_cards_win.setWindowIcon(QtGui.QIcon("feather\\plus-square.svg"))

    def add_card_btn_clicked(self, deck):
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        cards = cards_text.read().split("QUESTION^^$=")
        cards.pop(0)
        qsts = []
        for card in cards:
            qsts.append(card.split("ANSWER^^$=")[0])
        cards_text.close()
        if self.input_qst.toPlainText().strip() == "":
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Invalid")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Please enter a question")
            msg.exec_()
        elif self.input_qst.toPlainText().strip() in qsts:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Duplicate")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("That question already exists. Card not added.")
            msg.exec_()
        elif "DECK^^$=" in self.input_qst.toPlainText() or "QUESTION^^$=" in self.input_qst.toPlainText() or "ANSWER^^$" in self.input_qst.toPlainText() or "EASE^^$" in self.input_qst.toPlainText() or "DUE^^$=" in self.input_qst.toPlainText() or "INTERVAL^^$=" in self.input_qst.toPlainText() or "PHASE^^$=" in self.input_qst.toPlainText() or "DECK^^$=" in self.input_ans.toPlainText() or "QUESTION^^$=" in self.input_ans.toPlainText() or "ANSWER^^$" in self.input_ans.toPlainText() or "EASE^^$" in self.input_ans.toPlainText() or "DUE^^$=" in self.input_ans.toPlainText() or "INTERVAL^^$=" in self.input_ans.toPlainText() or "PHASE^^$=" in self.input_ans.toPlainText():
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Invalid")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Due to the way items are stored, strings cannot contain\n\"DECK^^$=\", \"QUESTION^^$=\", \"ANSWER^^$=\", \"EASE^^$=\"\n\"DUE^^$=\", \"INTERVAL^^$=\", or \"PHASE^^$=\".")
            msg.exec_()
        else:
            cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "a")
            cards_text.write(f"DECK^^$={deck}QUESTION^^$={self.input_qst.toPlainText()}ANSWER^^$={self.input_ans.toPlainText()}EASE^^$=2.5DUE^^$={datetime.datetime.now()}INTERVAL^^$=0PHASE^^$=L\n")
            self.input_qst.clear()
            self.input_ans.clear()
            cards_text.close()

            cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
            total_cards = cards_text.read().count("DECK^^$=")
            cards_text.close()

    def cancel_card_btn_clicked(self):
        self.add_cards_win.close()

    def back_decks_btn_clicked(self):
        # Closes the Add cards window and Search window.
        self.add_cards_win = QtWidgets.QWidget()
        self.add_cards_win.close()
        self.search_win = QtWidgets.QWidget()
        self.search_win.close()

        # Clears the deck layout.
        self.deck_label.deleteLater()
        self.search_deck_btn.deleteLater()
        self.search_deck_btn.deleteLater()
        self.back_decks_btn.deleteLater()
        self.del_deck_btn.deleteLater()
        self.add_cards_btn.deleteLater()

        ######################################### Re-draws main_win ###################################################
        # Finds how many are due today.
        cards_text = open(f"{self.temp_path}\\..\\MemoryGain\\cards.txt", "r")
        cards_parts = re.split("DUE\^\^\$=|INTERVAL\^\^\$=", cards_text.read())
        cards_text.close()
        cards_parts.pop(0)
        num_to_study = 0
        # Removes those not due today.
        end_of_today = str(datetime.datetime.now())
        end_of_today = datetime.datetime(int(end_of_today[:4]), int(end_of_today[5:7]), int(end_of_today[8:10]), 23, 59,
                                         59, 999999)
        for idx, part in enumerate(cards_parts):
            if idx % 2 == 0 and datetime.datetime.strptime(part, "%Y-%m-%d %H:%M:%S.%f") <= end_of_today:
                num_to_study += 1

        self.main_win_centralwidget = QtWidgets.QWidget(self.main_win)
        self.main_win_centralwidget.setObjectName("main_win_centralwidget")
        self.main_win_gridLayout = QtWidgets.QGridLayout(self.main_win_centralwidget)
        self.main_win_gridLayout.setObjectName("main_win_gridLayout")

        self.create_deck_btn = QtWidgets.QPushButton(self.main_win_centralwidget)
        self.create_deck_btn.setObjectName("create_deck_btn")
        self.create_deck_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.create_deck_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.create_deck_btn.setFont(font)
        self.create_deck_btn.setStyleSheet("""
                                                            QPushButton#create_deck_btn{
                                                                background-color:transparent;
                                                                border-radius: 15px;
                                                                border: 1px solid white;
                                                                color: white;
                                                            }
                                                            QPushButton#create_deck_btn:hover{
                                                                background-color: rgba(255, 255, 255, 0.1);
                                                            }
                                                            QPushButton#create_deck_btn:pressed{
                                                                background-color: rgba(255, 255, 255, 0.2);
                                                            }
                                                            """)
        self.create_deck_btn.clicked.connect(lambda: self.create_deck_btn_clicked())
        self.create_deck_btn.setText("Create deck")
        self.main_win_gridLayout.addWidget(self.create_deck_btn, 0, 1, 1, 1)

        self.study_btn = QtWidgets.QPushButton(self.main_win_centralwidget)
        self.study_btn.setObjectName("study_btn")
        self.study_btn.setMinimumSize(QtCore.QSize(300, 40))
        self.study_btn.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.study_btn.setFont(font)
        self.study_btn.setStyleSheet("""
                                                    QPushButton#study_btn{
                                                        background-color:transparent;
                                                        border-radius: 15px;
                                                        border: 1px solid white;
                                                        color: white;
                                                    }
                                                    QPushButton#study_btn:hover{
                                                        background-color: rgba(255, 255, 255, 0.1);
                                                    }
                                                    QPushButton#study_btn:pressed{
                                                        background-color: rgba(255, 255, 255, 0.2);
                                                    }
                                                    """)
        if num_to_study < 1000:
            self.study_btn.setText(f"Study {num_to_study}")
        else:
            self.study_btn.setText(f"Study 999+")
        self.study_btn.clicked.connect(lambda: self.study_btn_clicked())
        self.main_win_gridLayout.addWidget(self.study_btn, 1, 1, 1, 1)

        main_win_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_win_gridLayout.addItem(main_win_spacer, 0, 2, 1, 1)

        main_win_spacer1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_win_gridLayout.addItem(main_win_spacer1, 0, 0, 1, 1)

        self.main_win_scrollArea = QtWidgets.QScrollArea(self.main_win_centralwidget)
        self.main_win_scrollArea.setMinimumSize(QtCore.QSize(310, 16777215))
        self.main_win_scrollArea.setMaximumSize(QtCore.QSize(310, 16777215))
        self.main_win_scrollArea.setWidgetResizable(True)
        self.main_win_scrollArea.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.main_win_scrollArea.setObjectName("main_win_scrollArea")
        self.main_win_scrollArea.setStyleSheet("""
                                                                background-color: transparent;
                                                                border: none;
                                                                """)
        self.main_win_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.main_win_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 300, 435))
        self.main_win_scrollAreaWidgetContents.setObjectName("main_win_scrollAreaWidgetContents")
        self.main_win_verticalLayout = QtWidgets.QVBoxLayout(self.main_win_scrollAreaWidgetContents)
        self.main_win_verticalLayout.setObjectName("main_win_verticalLayout")

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "r")
        decks_lines = decks_text.readlines()
        for idx, i in enumerate(decks_lines):
            self.deck_btn = QtWidgets.QPushButton(self.main_win_scrollAreaWidgetContents)
            self.deck_btn.setMinimumSize(QtCore.QSize(282, 40))
            self.deck_btn.setMaximumSize(QtCore.QSize(282, 40))
            self.deck_btn.setFont(font)
            self.deck_btn.setStyleSheet("""
                                                        QPushButton#deck_btn{
                                                            background-color: transparent;
                                                            text-align: left;
                                                            color: white;
                                                            border-radius: 15px;
                                                        }
                                                        QPushButton#deck_btn:hover{
                                                            background-color: rgba(255, 255, 255, 0.1);
                                                        }
                                                        QPushButton#deck_btn:pressed{
                                                            background-color: rgba(255, 255, 255, 0.2);
                                                        }
                                                        """)
            self.deck_btn.setObjectName("deck_btn")
            self.deck_btn.setText("  " + i.replace("\n", ""))
            self.main_win_verticalLayout.addWidget(self.deck_btn)
            if idx == 0:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(0))
            if idx == 1:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(1))
            if idx == 2:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(2))
            if idx == 3:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(3))
            if idx == 4:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(4))
            if idx == 5:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(5))
            if idx == 6:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(6))
            if idx == 7:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(7))
            if idx == 8:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(8))
            if idx == 9:
                self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(9))
        decks_text.close()

        main_win_spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_win_verticalLayout.addItem(main_win_spacer2)
        self.main_win_scrollArea.setWidget(self.main_win_scrollAreaWidgetContents)
        self.main_win_gridLayout.addWidget(self.main_win_scrollArea, 2, 1, 1, 1)
        self.create_deck_btn.raise_()
        self.main_win_scrollArea.raise_()
        self.main_win.setCentralWidget(self.main_win_centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self.main_win)

        _translate = QtCore.QCoreApplication.translate
        self.main_win.setWindowTitle(_translate("main_win", "Memory Gain"))
        self.main_win.setWindowIcon(QtGui.QIcon("feather\\layers.svg"))

    def create_deck_btn_clicked(self):
        Thread(target=self.create_deck_btn_clicked_window()).start()
        Thread(target=self.create_deck_btn_clicked_checker).start()

    def create_deck_btn_clicked_checker(self):
        while True:
            time.sleep(0.1)
            if not self.main_win.isVisible():
                self.create_deck_win = QtWidgets.QWidget()
                self.create_deck_win.close()
                break

    def create_deck_btn_clicked_window(self):
        self.create_deck_win = QtWidgets.QWidget()
        self.create_deck_win.setObjectName("create_deck_win")
        self.create_deck_win.resize(600, 150)
        self.create_deck_win.setMinimumSize(QtCore.QSize(600, 150))
        self.create_deck_win.setMaximumSize(QtCore.QSize(600, 150))
        self.create_deck_win.setStyleSheet("""
                                        QWidget#create_deck_win{
                                            background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(40, 10, 40, 255), stop:1 rgba(20, 0, 20, 255));
                                      }
                                      """)
        self.create_deck_gridLayout = QtWidgets.QGridLayout(self.create_deck_win)
        self.create_deck_gridLayout.setObjectName("create_deck_gridLayout")
        self.create_deck_verticalLayout = QtWidgets.QVBoxLayout()
        self.create_deck_verticalLayout.setObjectName("create_deck_verticalLayout")
        self.create_deck_horizontalLayout = QtWidgets.QHBoxLayout()
        self.create_deck_horizontalLayout.setObjectName("create_deck_horizontalLayout")

        self.create_prompt_label = QtWidgets.QLabel(self.create_deck_win)
        self.create_prompt_label.setMinimumSize(QtCore.QSize(60, 40))
        self.create_prompt_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.create_prompt_label.setFont(font)
        self.create_prompt_label.setStyleSheet("""
                                                QLabel#create_prompt_label{
                                                    color: white;
                                               }
                                               """)
        self.create_prompt_label.setObjectName("create_prompt_label")
        self.create_deck_horizontalLayout.addWidget(self.create_prompt_label)

        self.create_input_text = QtWidgets.QLineEdit(self.create_deck_win)
        self.create_input_text.setMinimumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.create_input_text.setFont(font)
        self.create_input_text.setStyleSheet("""
                                            QLineEdit#create_input_text{
                                                background-color: rgba(255, 255, 255, 0.1);
                                                border-radius: 15px;
                                                padding-left: 5px;
                                                padding-right: 5px;
                                                color: white;
                                             }
                                             """)
        self.create_input_text.setObjectName("create_input_text")
        self.create_deck_horizontalLayout.addWidget(self.create_input_text)
        self.create_deck_verticalLayout.addLayout(self.create_deck_horizontalLayout)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.create_deck_verticalLayout.addItem(spacerItem)
        self.create_deck_horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.create_deck_horizontalLayout_2.setObjectName("create_deck_horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.create_deck_horizontalLayout_2.addItem(spacerItem1)

        self.create_ok_btn = QtWidgets.QPushButton(self.create_deck_win)
        self.create_ok_btn.setMinimumSize(QtCore.QSize(150, 40))
        self.create_ok_btn.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.create_ok_btn.setFont(font)
        self.create_ok_btn.setStyleSheet("QPushButton#create_ok_btn{\n"
                                         "    background-color: transparent;\n"
                                         "      border: 1px solid white;\n"
                                         "       border-radius: 15px;\n"
                                         "    color: white;\n"
                                         "}\n"
                                         "QPushButton#create_ok_btn:hover{\n"
                                         "    background-color: rgba(255, 255, 255, 0.1);\n"
                                         "}\n"
                                         "QPushButton#create_ok_btn:pressed{\n"
                                         "    background-color: rgba(255, 255, 255, 0.2);\n"
                                         "}")
        self.create_ok_btn.setObjectName("create_ok_btn")
        self.create_deck_horizontalLayout_2.addWidget(self.create_ok_btn)
        self.create_ok_btn.clicked.connect(lambda: self.create_ok_btn_clicked())

        self.create_cancel_btn = QtWidgets.QPushButton(self.create_deck_win)
        self.create_cancel_btn.setMinimumSize(QtCore.QSize(150, 40))
        self.create_cancel_btn.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setWeight(50)
        self.create_cancel_btn.setFont(font)
        self.create_cancel_btn.setStyleSheet("QPushButton#create_cancel_btn{\n"
                                             "    background-color: transparent;\n"
                                             "      border: 1px solid white;\n"
                                             "       border-radius: 15px;\n"
                                             "    color: white;\n"
                                             "}\n"
                                             "QPushButton#create_cancel_btn:hover{\n"
                                             "    background-color: rgba(255, 255, 255, 0.1);\n"
                                             "}\n"
                                             "QPushButton#create_cancel_btn:pressed{\n"
                                             "    background-color: rgba(255, 255, 255, 0.2);\n"
                                             "}")
        self.create_cancel_btn.setObjectName("create_cancel_btn")
        self.create_deck_horizontalLayout_2.addWidget(self.create_cancel_btn)
        self.create_cancel_btn.clicked.connect(lambda: self.create_cancel_btn_clicked())

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.create_deck_horizontalLayout_2.addItem(spacerItem2)
        self.create_deck_verticalLayout.addLayout(self.create_deck_horizontalLayout_2)
        self.create_deck_gridLayout.addLayout(self.create_deck_verticalLayout, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.create_deck_gridLayout.addItem(spacerItem3, 1, 0, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(self.create_deck_win)

        _translate = QtCore.QCoreApplication.translate
        self.create_deck_win.setWindowTitle(_translate("create_deck_win", "Create deck"))
        self.create_prompt_label.setText(_translate("create_deck_win", "Deck:"))
        self.create_ok_btn.setText(_translate("create_deck_win", "Ok"))
        self.create_cancel_btn.setText(_translate("create_deck_win", "Cancel"))

        self.create_deck_win.setWindowIcon(QtGui.QIcon("feather\\plus.svg"))

        self.create_deck_win.show()

    def create_ok_btn_clicked(self):
        decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "r")
        decks_lines = decks_text.readlines()
        decks_text.close()

        if "DECK^^$=" in self.create_input_text.text() or "QUESTION^^$=" in self.create_input_text.text() or "ANSWER^^$" in self.create_input_text.text() or "EASE^^$" in self.create_input_text.text() or "DUE^^$" in self.create_input_text.text() or "INTERVAL^^$" in self.create_input_text.text() or "PHASE^^$" in self.create_input_text.text():
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Invalid")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Due to the way items are stored, strings cannot contain\n\"DECK^^$=\", \"QUESTION^^$=\", \"ANSWER^^$=\", \"EASE^^$=\"\n\"DUE^^$=\", \"INTERVAL^^$=\", or \"PHASE^^$=\".")
            msg.exec_()
        elif self.create_input_text.text().strip() == "":
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Invalid")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Please enter a deck name.")
            msg.exec_()
        elif self.create_input_text.text().strip() + "\n" in decks_lines:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Invalid")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("That deck already exists.")
            msg.exec_()
        elif len(decks_lines) > 9:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Limit")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("This version of the Memory Gain application supports a maximum of 10 decks.")
            msg.exec_()
        else:
            decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "a")
            decks_text.write(self.create_input_text.text().strip() + "\n")
            decks_text.close()

            decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "r")
            decks_sorted = decks_text.readlines()
            decks_sorted.sort(key=str.lower)
            decks_text.close()

            decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "w")
            decks_text.writelines(decks_sorted)
            decks_text.close()

            while self.main_win_verticalLayout.count():
                child = self.main_win_verticalLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            font = QtGui.QFont()
            font.setFamily("Verdana")
            font.setPointSize(12)
            decks_text = open(f"{self.temp_path}\\..\\MemoryGain\\decks.txt", "r")
            decks_lines = decks_text.readlines()
            for idx, i in enumerate(decks_lines):
                self.deck_btn = QtWidgets.QPushButton(self.main_win_scrollAreaWidgetContents)
                self.deck_btn.setMinimumSize(QtCore.QSize(282, 40))
                self.deck_btn.setMaximumSize(QtCore.QSize(282, 40))
                self.deck_btn.setFont(font)
                self.deck_btn.setStyleSheet("""QPushButton#deck_btn{
                                                background-color: transparent;
                                                text-align: left;
                                                color: white;
                                                border-radius: 15px;
                                            }
                                            QPushButton#deck_btn:hover{
                                                background-color: rgba(255, 255, 255, 0.1);
                                            }
                                            QPushButton#deck_btn:pressed{
                                                background-color: rgba(255, 255, 255, 0.2);
                                            }""")
                self.deck_btn.setObjectName("deck_btn")

                self.deck_btn.setText("  " + i.replace("\n", ""))
                self.main_win_verticalLayout.addWidget(self.deck_btn)
                if idx == 0:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(0))
                if idx == 1:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(1))
                if idx == 2:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(2))
                if idx == 3:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(3))
                if idx == 4:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(4))
                if idx == 5:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(5))
                if idx == 6:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(6))
                if idx == 7:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(7))
                if idx == 8:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(8))
                if idx == 9:
                    self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(9))

            decks_text.close()

            main_win_spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                     QtWidgets.QSizePolicy.Expanding)
            self.main_win_verticalLayout.addItem(main_win_spacer2)
            self.main_win_scrollArea.setWidget(self.main_win_scrollAreaWidgetContents)
            self.main_win_gridLayout.addWidget(self.main_win_scrollArea, 3, 1, 1, 1)
            self.create_deck_btn.raise_()
            self.main_win_scrollArea.raise_()
            self.main_win.setCentralWidget(self.main_win_centralwidget)

            self.create_deck_win.close()

    def create_cancel_btn_clicked(self):
        self.create_deck_win.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_main_win()
    ui.setupUi()
    sys.exit(app.exec_())

