"""
Memory Gain (c) is a flashcards app.

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

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QDesktopWidget
import datetime
import tempfile
import urllib.request
import os
from functools import partial
import cards
import decks


class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.temp_path = tempfile.gettempdir()
        self.setup_ui()

    def setup_ui(self):
        # self.home_showing is used by self.deck_refresher() to decide whether or not to re-draw the main_win scroll area
        # to show newly created decks.
        self.home_showing = True

        # Update checker.
        try:
            html = urllib.request.urlopen("https://memorygain.app")
            if "Test version 0.0.4" not in str(html.read()):
                self.update_msg = QtWidgets.QMessageBox()
                self.update_msg.setWindowTitle("Update")
                self.update_msg.setText("There is an updated version available at https://memorygain.app. Would you like to download the updated version?")
                self.update_msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                self.update_msg.setIcon(QtWidgets.QMessageBox.Information)
                self.update_msg.exec_()
                if self.update_msg.clickedButton().text() == "&Yes":
                    os.system("START https://memorygain.app")
                    sys.exit()

        except urllib.error.URLError as e:
            print(e)

        except urllib.error.HTTPError as e:
            print(e)

        # Finds how many are due today.
        num_to_study = cards.get_num_to_study()

        self.setObjectName("main_win")
        self.resize(750, 600)
        self.setMinimumSize(QtCore.QSize(700, 400))
        self.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.setStyleSheet("""
                            QMainWindow#main_win{
                                background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(30, 10, 30, 255), stop:1 rgba(60, 10, 60, 255));
                            }
                            QScrollBar{
                                background: transparent;
                                width: 10px;
                            }
                            """)
        self.main_win_centralwidget = QtWidgets.QWidget(self)
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

        for idx, deck in enumerate(decks.get_deck_lines()):
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
            self.deck_btn.setText("  " + deck.replace("\n", ""))
            self.main_win_verticalLayout.addWidget(self.deck_btn)

            # This has to be done as the deck button cannot be assigned the 'idx' variable directly as this will make it
            # such that the argument of all buttons will be the last value of 'idx', i.e. if you write
            # 'self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(idx))' all buttons will have the final value of 'idx'.
            func = partial(self.deck_btn_clicked, idx)
            self.deck_btn.clicked.connect(func)

        main_win_spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_win_verticalLayout.addItem(main_win_spacer2)
        self.main_win_scrollArea.setWidget(self.main_win_scrollAreaWidgetContents)
        self.main_win_gridLayout.addWidget(self.main_win_scrollArea, 2, 1, 1, 1)
        self.setCentralWidget(self.main_win_centralwidget)

        self.setWindowTitle("Memory Gain")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

    def study_btn_clicked(self):
        self.home_showing = False
        # Clears main_win. "main_win_centralwidget" is reassigned as so this function can be called when cancelling
        # an edit from the study window.
        self.main_win_centralwidget = QtWidgets.QWidget()
        self.main_win_centralwidget.deleteLater()

        # Creates the study window contents.
        self.study_centralwidget = QtWidgets.QWidget()
        self.study_gridLayout = QtWidgets.QGridLayout(self.study_centralwidget)

        self.current_card = cards.get_card()

        self.study_gridLayout.setObjectName("study_gridLayout")
        self.study_upper_horizontalLayout = QtWidgets.QHBoxLayout()
        self.study_upper_horizontalLayout.setObjectName("study_upper_horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_upper_horizontalLayout.addItem(spacerItem)

        self.study_home_btn = QtWidgets.QPushButton(self)
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

        self.study_edit_btn = QtWidgets.QPushButton(self)
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
        if not self.current_card:
            self.study_edit_btn.hide()

        self.study_upper_horizontalLayout.addWidget(self.study_edit_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_upper_horizontalLayout.addItem(spacerItem1)
        self.study_gridLayout.addLayout(self.study_upper_horizontalLayout, 0, 0, 1, 1)
        self.study_labels_verticalLayout = QtWidgets.QVBoxLayout()
        self.study_labels_verticalLayout.setObjectName("study_labels_verticalLayout")
        self.study_qst_label = QtWidgets.QLabel(self)
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
        if not self.current_card:
            self.study_qst_label.setText("Completed.")
        else:
            self.study_qst_label.setText(self.current_card[1])

        self.study_line = QtWidgets.QFrame(self)
        self.study_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.study_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.study_line.setObjectName("study_line")
        if not self.current_card:
            self.study_line.hide()

        self.study_labels_verticalLayout.addWidget(self.study_line)

        self.study_ans_label = QtWidgets.QLabel(self)
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

        self.again_btn = QtWidgets.QPushButton(self)
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

        self.show_ans_btn = QtWidgets.QPushButton(self)
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
        if not self.current_card:
            self.show_ans_btn.hide()

        self.correct_btn = QtWidgets.QPushButton(self)
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

        self.setWindowTitle("Memory Gain - Study")
        self.study_home_btn.setText("Home")
        self.study_edit_btn.setText("Edit")
        self.again_btn.setText("Again")
        self.show_ans_btn.setText("Answer")
        self.correct_btn.setText("Correct")

        self.setCentralWidget(self.study_centralwidget)

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
        self.edit_qst_text.setText(self.current_card[1])
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
        self.edit_ans_text.setText(self.current_card[2])
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

        self.setWindowTitle("Memory Gain - Study - Edit")
        self.edit_qst_label.setText("Question:")
        self.edit_ans_label.setText("Answer:")
        self.edit_save_btn.setText("Save")
        self.edit_del_btn.setText("Delete")
        self.edit_back_btn.setText("Cancel")

        self.setCentralWidget(self.edit_centralwidget)

    def edit_del_btn_clicked(self):
        cards.del_card(self.current_card[0], self.current_card[1])

        # Reverts back to the study window.
        self.edit_centralwidget.deleteLater()
        self.study_btn_clicked()

    def edit_save_btn_clicked(self):
        cards.write_card_edit_save(self.current_card[0], self.current_card[1], self.edit_qst_text.toPlainText(), self.edit_ans_text.toPlainText())

        self.current_card[1] = self.edit_qst_text.toPlainText()
        self.current_card[2] = self.edit_ans_text.toPlainText()

        # As self.study_btn_clicked() will re-get self.current_card, to preserve the card they hit edit on:
        card = self.current_card
        self.edit_centralwidget.deleteLater()
        self.study_btn_clicked()
        self.current_card = card
        self.study_qst_label.setText(self.edit_qst_text.toPlainText())
        self.study_ans_label.setText("")
        self.correct_btn.hide()
        self.again_btn.hide()
        self.show_ans_btn.show()

    def edit_back_btn_clicked(self):
        card = self.current_card
        self.edit_centralwidget.deleteLater()
        self.study_btn_clicked()
        self.current_card = card
        self.study_qst_label.setText(card[1])

    def study_home_btn_clicked(self):
        self.home_showing = True
        # Finds how many are due today.
        num_to_study = cards.get_num_to_study()

        self.setMinimumSize(QtCore.QSize(700, 400))
        self.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.setStyleSheet("""
                            QMainWindow#main_win{
                                background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(30, 10, 30, 255), stop:1 rgba(60, 10, 60, 255));
                            }
                            QScrollBar{
                                background: transparent;
                                width: 10px;
                            }
                            """)
        self.main_win_centralwidget = QtWidgets.QWidget(self)
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

        for idx, deck in enumerate(decks.get_deck_lines()):
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
            self.deck_btn.setText("  " + deck.replace("\n", ""))
            self.main_win_verticalLayout.addWidget(self.deck_btn)

            # This has to be done as the deck button cannot be assigned the 'idx' variable directly as this will make it
            # such that the argument of all buttons will be the last value of 'idx', i.e. if you write
            # 'self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(idx))' all buttons will have the final value of 'idx'.
            func = partial(self.deck_btn_clicked, idx)
            self.deck_btn.clicked.connect(func)

        main_win_spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_win_verticalLayout.addItem(main_win_spacer2)
        self.main_win_scrollArea.setWidget(self.main_win_scrollAreaWidgetContents)
        self.main_win_gridLayout.addWidget(self.main_win_scrollArea, 2, 1, 1, 1)
        self.create_deck_btn.raise_()
        self.main_win_scrollArea.raise_()
        self.setCentralWidget(self.main_win_centralwidget)
        self.setWindowTitle("Memory Gain")
        self.main_win_centralwidget.show()

    def show_ans_btn_clicked(self):
        self.study_ans_label.setText(self.current_card[2])
        self.show_ans_btn.hide()
        self.again_btn.show()
        self.correct_btn.show()

    def correct_btn_clicked(self):
        if self.current_card[6] == "L":
            self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
            self.current_card[6] = "B"
        elif self.current_card[6] == "B":
            self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=1440))
            self.current_card[5] = "1440"
            self.current_card[6] = "G"
        elif self.current_card[6] == "G":
            self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=int(float(self.current_card[3]) * int(self.current_card[5]))))
            self.current_card[5] = str(int(float(self.current_card[3]) * int(self.current_card[5])))
        elif self.current_card[6] == "l":
            self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
            self.current_card[6] = "B"
        elif self.current_card[6] == "b":
            self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
            self.current_card[6] = "B"
        elif self.current_card[6] == "g":
            self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
            self.current_card[6] = "B"

        cards.write_card_ac(self.current_card)

        self.current_card = cards.get_card()
        if self.current_card:
            self.study_qst_label.setText(self.current_card[1])
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
        if self.current_card:
            if self.current_card[6] == "l":
                self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=1))
            elif self.current_card[6] == "b":
                self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=1))
            elif self.current_card[6] == "g":
                self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
            elif self.current_card[6] == "L":
                self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=1))
                self.current_card[6] = "l"
            elif self.current_card[6] == "B":
                self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=1))
                self.current_card[6] = "b"
            elif self.current_card[6] == "G":
                self.current_card[4] = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
                self.current_card[5] = 0
                if float(self.current_card[3]) > 1.3:
                    self.current_card[3] = str(float(self.current_card[3]) * 0.80)
                    if float(self.current_card[3]) < 1.3:
                        self.current_card[3] = "1.3"
                self.current_card[6] = "g"

            cards.write_card_ac(self.current_card)

            self.correct_btn.hide()
            self.again_btn.hide()
            self.show_ans_btn.show()
            self.current_card = cards.get_card()
            self.study_qst_label.setText(self.current_card[1])
            self.study_ans_label.setText("")

    def deck_btn_clicked(self, idx):
        self.home_showing = False
        # Clears main_win.
        self.main_win_scrollArea.deleteLater()
        self.study_btn.deleteLater()
        self.create_deck_btn.deleteLater()

        deck = decks.get_deck_name(idx)

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

        self.setWindowTitle(f"{deck} deck")
        self.deck_label.setText(f"{deck}")
        self.add_cards_btn.setText("Add cards")
        self.search_deck_btn.setText("Search")
        self.del_deck_btn.setText("Delete")
        self.back_decks_btn.setText("Home")

        self.setWindowIcon(QtGui.QIcon("icon.ico"))

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
            self.home_showing = True

            decks.del_deck(deck)

            #Clears the deck layout.
            self.deck_label.deleteLater()
            self.search_deck_btn.deleteLater()
            self.search_deck_btn.deleteLater()
            self.back_decks_btn.deleteLater()
            self.del_deck_btn.deleteLater()
            self.add_cards_btn.deleteLater()

            # Re-draws main_win.
            # Finds how many are due today.
            num_to_study = cards.get_num_to_study()

            self.main_win_centralwidget = QtWidgets.QWidget(self)
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

            for idx, deck in enumerate(decks.get_deck_lines()):
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
                self.deck_btn.setText("  " + deck.replace("\n", ""))
                self.main_win_verticalLayout.addWidget(self.deck_btn)

                # This has to be done as the deck button cannot be assigned the 'idx' variable directly as this will make it
                # such that the argument of all buttons will be the last value of 'idx', i.e. if you write
                # 'self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(idx))' all buttons will have the final value of 'idx'.
                func = partial(self.deck_btn_clicked, idx)
                self.deck_btn.clicked.connect(func)

            main_win_spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                     QtWidgets.QSizePolicy.Expanding)
            self.main_win_verticalLayout.addItem(main_win_spacer2)
            self.main_win_scrollArea.setWidget(self.main_win_scrollAreaWidgetContents)
            self.main_win_gridLayout.addWidget(self.main_win_scrollArea, 2, 1, 1, 1)
            self.create_deck_btn.raise_()
            self.main_win_scrollArea.raise_()
            self.setCentralWidget(self.main_win_centralwidget)

            self.setWindowTitle("Memory Gain")
            self.setWindowIcon(QtGui.QIcon("icon.ico"))

    def search_deck_btn_clicked(self, deck):
        self.deck_label.setText("Please finish searching the deck.")
        self.add_cards_btn.hide()
        self.search_deck_btn.hide()
        self.del_deck_btn.hide()
        self.back_decks_btn.hide()

        self.search_win = SearchWin(deck)
        self.search_win.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.search_win.exec_()

        self.deck_label.setText(deck)
        self.add_cards_btn.show()
        self.search_deck_btn.show()
        self.del_deck_btn.show()
        self.back_decks_btn.show()

    def add_cards_btn_clicked(self, deck):
        self.deck_label.setText("Please finish adding cards.")
        self.add_cards_btn.hide()
        self.search_deck_btn.hide()
        self.del_deck_btn.hide()
        self.back_decks_btn.hide()

        self.add_cards_win = AddCardsWin(deck)
        self.add_cards_win.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.add_cards_win.exec_()

        self.deck_label.setText(deck)
        self.add_cards_btn.show()
        self.search_deck_btn.show()
        self.del_deck_btn.show()
        self.back_decks_btn.show()

    def back_decks_btn_clicked(self):
        self.home_showing = True
        # Closes the Add cards window and Search window.
        self.add_cards_win = QtWidgets.QWidget()
        self.add_cards_win.close()

        # Clears the deck layout.
        self.deck_label.deleteLater()
        self.search_deck_btn.deleteLater()
        self.search_deck_btn.deleteLater()
        self.back_decks_btn.deleteLater()
        self.del_deck_btn.deleteLater()
        self.add_cards_btn.deleteLater()

        # Re-draws main_win.
        # Finds how many are due today.
        num_to_study = cards.get_num_to_study()

        self.main_win_centralwidget = QtWidgets.QWidget(self)
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

        self.deck_refresher()

        self.setWindowTitle("Memory Gain")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

    def create_deck_btn_clicked(self):
        # self.deck_refresher is passed in as a reference.
        self.create_deck_win = CreateDeckWin(self.deck_refresher)
        self.create_deck_win.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.create_deck_win.exec_()

    def deck_refresher(self):
        if self.home_showing:
            while self.main_win_verticalLayout.count():
                child = self.main_win_verticalLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            font = QtGui.QFont()
            font.setFamily("Verdana")
            font.setPointSize(12)

            for idx, deck in enumerate(decks.get_deck_lines()):
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
                self.deck_btn.setText("  " + deck.replace("\n", ""))
                self.main_win_verticalLayout.addWidget(self.deck_btn)

                # This has to be done as the deck button cannot be assigned the 'idx' variable directly as this will make it
                # such that the argument of all buttons will be the last value of 'idx', i.e. if you write
                # 'self.deck_btn.clicked.connect(lambda: self.deck_btn_clicked(idx))' all buttons will have the final value of 'idx'.
                func = partial(self.deck_btn_clicked, idx)
                self.deck_btn.clicked.connect(func)

            main_win_spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.main_win_verticalLayout.addItem(main_win_spacer2)
            self.main_win_scrollArea.setWidget(self.main_win_scrollAreaWidgetContents)
            self.main_win_gridLayout.addWidget(self.main_win_scrollArea, 3, 1, 1, 1)
            self.setCentralWidget(self.main_win_centralwidget)


class SearchWin(QtWidgets.QDialog):
    def __init__(self, deck):
        super().__init__()
        self.deck = deck
        self.temp_path = tempfile.gettempdir()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(f"Search {self.deck}")
        self.setObjectName("search_win")
        self.resize(700, 500)
        self.setStyleSheet("""
                            QWidget#search_win{
                                background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(40, 10, 40, 255), stop:1 rgba(20, 0, 20, 255));
                            }
                            QScrollBar{
                                background: transparent;
                                width: 10px;
                            }
                            """)
        self.search_win_gridLayout = QtWidgets.QGridLayout(self)
        self.search_win_gridLayout.setObjectName("search_win_gridLayout")
        self.search_win_verticalLayout = QtWidgets.QVBoxLayout()
        self.search_win_verticalLayout.setObjectName("search_win_verticalLayout")
        self.search_win_horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.search_win_horizontalLayout_2.setObjectName("search_win_horizontalLayout_2")

        self.input_search = QtWidgets.QLineEdit(self)
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

        self.search_btn = QtWidgets.QPushButton(self)
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
        self.search_btn.clicked.connect(lambda: self.search_btn_clicked())
        self.setWindowIcon(QtGui.QIcon("feather_601060\\search.svg"))
        self.search_win_verticalLayout.addLayout(self.search_win_horizontalLayout_2)
        self.search_btn.setText("Search")

        self.search_win_horizontalLayout = QtWidgets.QHBoxLayout()
        self.search_win_horizontalLayout.setObjectName("search_win_horizontalLayout")

        self.search_win_verticalLayout.addLayout(self.search_win_horizontalLayout_2)
        self.search_win_gridLayout.addLayout(self.search_win_verticalLayout, 1, 1, 1, 1)
        self.showing = False

    def search_btn_clicked(self):
        import cards

        self.search_query = self.input_search.text()
        self.search_page = 1
        self.search_upto = 0

        if cards.search_query_exists(self.search_query):
            qst, ans, self.amt_cards = cards.search_for_cards(self.deck, self.search_query, self.search_upto)

            if (not self.showing) and (self.amt_cards != 0):
                self.search_qst_label = QtWidgets.QLabel(self)
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

                self.search_qst_text = QtWidgets.QTextEdit(self)
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

                self.search_ans_label = QtWidgets.QLabel(self)
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

                self.search_ans_text = QtWidgets.QTextEdit(self)
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

                self.search_save_btn = QtWidgets.QPushButton(self)
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

                self.search_del_btn = QtWidgets.QPushButton(self)
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
                self.search_del_btn.clicked.connect(lambda: self.search_del_btn_clicked())

                spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.search_win_horizontalLayout.addItem(spacerItem1)

                self.search_left_btn = QtWidgets.QPushButton(self)
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

                self.card_of_card_label = QtWidgets.QLabel(self)
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

                self.search_right_btn = QtWidgets.QPushButton(self)
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
                icon4.addPixmap(QtGui.QPixmap("feather_white\\chevron-right.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
                self.card_of_card_label.setText(f"{self.search_page} of {self.amt_cards}")

            elif self.amt_cards != 0:
                self.search_qst_text.setText(qst)
                self.search_ans_text.setText(ans)
                self.card_of_card_label.setText(f"{self.search_page} of {self.amt_cards}")

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
        cards.save_searched_card(self.deck, self.search_query, self.search_upto, self.search_qst_text.toPlainText(), self.search_ans_text.toPlainText())

    def search_del_btn_clicked(self):
        cards.del_searched_card(self.deck, self.search_query, self.search_upto)

        if self.amt_cards == 1:
            self.close()
        elif self.search_upto == 0:
            qst, ans, self.amt_cards = cards.search_for_cards(self.deck, self.search_query, self.search_upto)

            self.search_qst_text.setText(qst)
            self.search_ans_text.setText(ans)
            self.card_of_card_label.setText(f"{self.search_page} of {self.amt_cards}")
        else:
            self.search_left_btn_clicked()

    def search_right_btn_clicked(self):
        if self.search_page != self.amt_cards:
            self.search_page += 1
            self.search_upto += 1

            qst, ans, self.amt_cards = cards.search_for_cards(self.deck, self.search_query, self.search_upto)

            self.search_qst_text.setText(qst)
            self.search_ans_text.setText(ans)
            self.card_of_card_label.setText(f"{self.search_page} of {self.amt_cards}")

    def search_left_btn_clicked(self):
        if self.search_page != 1:
            self.search_page -= 1
            self.search_upto -= 1

            qst, ans, self.amt_cards = cards.search_for_cards(self.deck, self.search_query, self.search_upto)

            self.search_qst_text.setText(qst)
            self.search_ans_text.setText(ans)
            self.card_of_card_label.setText(f"{self.search_page} of {self.amt_cards}")


class CreateDeckWin(QtWidgets.QDialog):
    def __init__(self, refresher):
        super().__init__()
        self.refresher = refresher
        self.temp_path = tempfile.gettempdir()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("create_deck_win")
        self.resize(600, 150)
        self.setMaximumSize(QtCore.QSize(600, 150))
        self.setStyleSheet("""
                            QWidget#create_deck_win{
                                background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(40, 10, 40, 255), stop:1 rgba(20, 0, 20, 255));
                          }
                          """)
        self.create_deck_gridLayout = QtWidgets.QGridLayout(self)
        self.create_deck_gridLayout.setObjectName("create_deck_gridLayout")
        self.create_deck_verticalLayout = QtWidgets.QVBoxLayout()
        self.create_deck_verticalLayout.setObjectName("create_deck_verticalLayout")
        self.create_deck_horizontalLayout = QtWidgets.QHBoxLayout()
        self.create_deck_horizontalLayout.setObjectName("create_deck_horizontalLayout")

        self.create_prompt_label = QtWidgets.QLabel(self)
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

        self.create_input_text = QtWidgets.QLineEdit(self)
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

        self.create_ok_btn = QtWidgets.QPushButton(self)
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

        self.create_cancel_btn = QtWidgets.QPushButton(self)
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

        self.setWindowTitle("Create deck")
        self.create_prompt_label.setText("Deck:")
        self.create_ok_btn.setText("Ok")
        self.create_cancel_btn.setText("Cancel")

        self.setWindowIcon(QtGui.QIcon("feather_601060\\plus.svg"))

    def create_ok_btn_clicked(self):
        decks_lines = decks.get_deck_lines()

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
        else:
            deck_name = self.create_input_text.text().strip()
            decks.add_deck(deck_name)

            self.refresher()
            self.close()

    def create_cancel_btn_clicked(self):
        self.close()


class AddCardsWin(QtWidgets.QDialog):
    def __init__(self, deck):
        super().__init__()
        self.deck = deck
        self.temp_path = tempfile.gettempdir()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("add_cards_win")
        self.resize(700, 500)
        self.setStyleSheet("""
                            QWidget#add_cards_win{
                                background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(40, 10, 40, 255), stop:1 rgba(20, 0, 20, 255));;
                            }
                            QScrollBar{
                               background: transparent;
                               width: 10px;
                            }
                            """)
        self.add_cards_gridLayout = QtWidgets.QGridLayout(self)
        self.add_cards_gridLayout.setObjectName("add_cards_gridLayout")
        self.add_cards_verticalLayout = QtWidgets.QVBoxLayout()
        self.add_cards_verticalLayout.setObjectName("add_cards_verticalLayout")
        self.qst_label = QtWidgets.QLabel(self)
        font = QtGui.QFont("Verdana")
        font.setPointSize(12)
        self.qst_label.setFont(font)
        self.qst_label.setStyleSheet("""
                                            color: white;
                                            """)
        self.qst_label.setObjectName("qst_label")
        self.add_cards_verticalLayout.addWidget(self.qst_label)

        self.input_qst = QtWidgets.QTextEdit(self)
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

        self.ans_label = QtWidgets.QLabel(self)
        font = QtGui.QFont("Verdana")
        font.setPointSize(12)
        self.ans_label.setFont(font)
        self.ans_label.setStyleSheet("color:white;")
        self.ans_label.setObjectName("ans_label")
        self.add_cards_verticalLayout.addWidget(self.ans_label)

        self.input_ans = QtWidgets.QTextEdit(self)
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

        self.add_card_btn = QtWidgets.QPushButton(self)
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
        self.add_card_btn.clicked.connect(lambda: self.add_card_btn_clicked())

        self.add_cards_verticalLayout.addLayout(self.add_cards_horizontalLayout)
        self.add_cards_gridLayout.addLayout(self.add_cards_verticalLayout, 1, 1, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.add_cards_horizontalLayout.addItem(spacerItem1)

        self.setWindowTitle("Add cards")
        self.qst_label.setText("Question:")
        self.ans_label.setText("Answer:")
        self.add_card_btn.setText("Add")

        self.setWindowIcon(QtGui.QIcon("feather_601060\\plus-square.svg"))

    def add_card_btn_clicked(self):
        if self.input_qst.toPlainText().strip() == "":
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Invalid")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Please enter a question")
            msg.exec_()
            return

        if "DECK^^$=" in self.input_qst.toPlainText() or "QUESTION^^$=" in self.input_qst.toPlainText() or "ANSWER^^$" in self.input_qst.toPlainText() or "EASE^^$" in self.input_qst.toPlainText() or "DUE^^$=" in self.input_qst.toPlainText() or "INTERVAL^^$=" in self.input_qst.toPlainText() or "PHASE^^$=" in self.input_qst.toPlainText() or "DECK^^$=" in self.input_ans.toPlainText() or "QUESTION^^$=" in self.input_ans.toPlainText() or "ANSWER^^$" in self.input_ans.toPlainText() or "EASE^^$" in self.input_ans.toPlainText() or "DUE^^$=" in self.input_ans.toPlainText() or "INTERVAL^^$=" in self.input_ans.toPlainText() or "PHASE^^$=" in self.input_ans.toPlainText():
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Invalid")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Due to the way items are stored, strings cannot contain\n\"DECK^^$=\", \"QUESTION^^$=\", \"ANSWER^^$=\", \"EASE^^$=\"\n\"DUE^^$=\", \"INTERVAL^^$=\", or \"PHASE^^$=\".")
            msg.exec_()
            return

        qst_exists = cards.check_qst_exists(self.input_qst.toPlainText().strip())
        if qst_exists:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Duplicate")
            center = QDesktopWidget().availableGeometry().center()
            msg.move(center)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("That question already exists. Card not added.")
            msg.exec_()
            return

        cards.add_card(self.deck, self.input_qst.toPlainText().strip(), self.input_ans.toPlainText().strip())
        self.input_qst.clear()
        self.input_ans.clear()


if __name__ == "__main__":
    temp_path = tempfile.gettempdir()
    # File and directory checker.
    memorygaindir_on_device = os.path.exists(f"{temp_path}\\..\\MemoryGain")
    cards_on_device = os.path.exists(f"{temp_path}\\..\\MemoryGain\\cards.txt")
    decks_on_device = os.path.exists(f"{temp_path}\\..\\MemoryGain\\decks.txt")

    if not memorygaindir_on_device:
        os.system(f"md {temp_path}\\..\\MemoryGain")

    if not cards_on_device:
        os.system(f"n > {temp_path}\\..\\MemoryGain\\cards.txt")

    if not decks_on_device:
        os.system(f"n > {temp_path}\\..\\MemoryGain\\decks.txt")

    app = QtWidgets.QApplication(sys.argv)
    mw = MainWin()
    mw.show()
    sys.exit(app.exec_())

