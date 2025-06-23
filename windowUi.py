# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QWidget)

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(500, 500)
        MainWidget.setMinimumSize(QSize(500, 500))
        MainWidget.setMaximumSize(QSize(500, 500))
        self.loginPage = QWidget()
        self.loginPage.setObjectName(u"loginPage")
        self.horizontalLayout_2 = QHBoxLayout(self.loginPage)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.loginButton = QPushButton(self.loginPage)
        self.loginButton.setObjectName(u"loginButton")

        self.horizontalLayout.addWidget(self.loginButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        MainWidget.addWidget(self.loginPage)
        self.mainPage = QWidget()
        self.mainPage.setObjectName(u"mainPage")
        self.horizontalLayout_3 = QHBoxLayout(self.mainPage)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.mainPageTitle = QLabel(self.mainPage)
        self.mainPageTitle.setObjectName(u"mainPageTitle")
        self.mainPageTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.mainPageTitle, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 3, 0, 1, 1)

        self.userInput = QLineEdit(self.mainPage)
        self.userInput.setObjectName(u"userInput")

        self.gridLayout.addWidget(self.userInput, 4, 1, 1, 1)

        self.userButton = QPushButton(self.mainPage)
        self.userButton.setObjectName(u"userButton")

        self.gridLayout.addWidget(self.userButton, 5, 1, 1, 1)

        self.progressLabel = QLabel(self.mainPage)
        self.progressLabel.setObjectName(u"progressLabel")

        self.gridLayout.addWidget(self.progressLabel, 1, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 3, 2, 1, 1)

        self.userLabel = QLabel(self.mainPage)
        self.userLabel.setObjectName(u"userLabel")
        self.userLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.userLabel, 3, 1, 1, 1)

        self.progressBar = QProgressBar(self.mainPage)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout.addWidget(self.progressBar, 2, 1, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout)

        MainWidget.addWidget(self.mainPage)

        self.retranslateUi(MainWidget)

        MainWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QCoreApplication.translate("MainWidget", u"StackedWidget", None))
        self.loginButton.setText(QCoreApplication.translate("MainWidget", u"Entre com Spotify", None))
        self.mainPageTitle.setText(QCoreApplication.translate("MainWidget", u"Playlist Creator", None))
        self.userButton.setText(QCoreApplication.translate("MainWidget", u"Enviar", None))
        self.progressLabel.setText(QCoreApplication.translate("MainWidget", u"TextLabel", None))
        self.userLabel.setText(QCoreApplication.translate("MainWidget", u"Nome de usu\u00e1rio do Last.FM", None))
    # retranslateUi

