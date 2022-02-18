try:
    import os
    import sys
    import requests
    import time

    from functools import partial
    from math import sqrt, pow

    from PyQt5 import uic
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPixmap
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow
except ImportError as err:
    print("Could't load module. %s" % (err))
    sys.exit(2)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Map")
        MainWindow.resize(702, 561)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.yandex_map = QLabel(self.centralwidget)
        self.yandex_map.setGeometry(QtCore.QRect(10, 10, 561, 401))
        self.yandex_map.setObjectName("yandex_map")
        self.schemeButton = QtWidgets.QPushButton(self.centralwidget)
        self.schemeButton.setGeometry(QtCore.QRect(590, 10, 101, 31))
        self.schemeButton.setObjectName("schemeButton")
        self.satteliteButton = QtWidgets.QPushButton(self.centralwidget)
        self.satteliteButton.setGeometry(QtCore.QRect(590, 50, 101, 31))
        self.satteliteButton.setObjectName("satteliteButton")
        self.hybridButton = QtWidgets.QPushButton(self.centralwidget)
        self.hybridButton.setGeometry(QtCore.QRect(590, 90, 101, 31))
        self.hybridButton.setObjectName("hybridButton")
        self.input_text = QtWidgets.QLineEdit(self.centralwidget)
        self.input_text.setGeometry(QtCore.QRect(150, 420, 421, 21))
        self.input_text.setObjectName("input_text")
        self.Input_name = QtWidgets.QLabel(self.centralwidget)
        self.Input_name.setGeometry(QtCore.QRect(10, 420, 121, 16))
        self.Input_name.setObjectName("Input_name")
        self.findButton = QtWidgets.QPushButton(self.centralwidget)
        self.findButton.setGeometry(QtCore.QRect(580, 420, 111, 21))
        self.findButton.setObjectName("findButton")
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(580, 480, 111, 31))
        self.clearButton.setObjectName("clearButton")
        self.output_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.output_text.setGeometry(QtCore.QRect(150, 480, 421, 31))
        self.output_text.setMouseTracking(True)
        self.output_text.setObjectName("output_text")
        self.output_name = QtWidgets.QLabel(self.centralwidget)
        self.output_name.setGeometry(QtCore.QRect(10, 480, 101, 31))
        self.output_name.setObjectName("output_name")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(150, 450, 101, 21))
        self.checkBox.setObjectName("checkBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 702, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.schemeButton.setText(_translate("MainWindow", "Scheme"))
        self.satteliteButton.setText(_translate("MainWindow", "Satettite"))
        self.hybridButton.setText(_translate("MainWindow", "Hybrid"))
        self.Input_name.setText(_translate("MainWindow", "Enter a request:"))
        self.findButton.setText(_translate("MainWindow", "Find"))
        self.clearButton.setText(_translate("MainWindow", "Clear"))
        self.output_name.setText(_translate("MainWindow", "Full address:"))
        self.checkBox.setText(_translate("MainWindow", "postal code"))


class Api_map(QMainWindow, Ui_MainWindow):
    # create Map class
    def __init__(self, coord):
        super().__init__()
        self.setupUi(self)
        self.coord = coord
        self.zoom = 12
        self.direction_x, self.direction_y = 0, 0
        self.pt = None
        self.map_file = "map.png"
        self.type = "map"

        self.get_map()

        # layers
        self.hybridButton.clicked.connect(partial(self.change_layer, "skl"))
        self.schemeButton.clicked.connect(partial(self.change_layer, "map"))
        self.satteliteButton.clicked.connect(partial(self.change_layer, "sat"))

        # search buttons
        self.findButton.clicked.connect(self.search_object)
        self.clearButton.clicked.connect(self.clear_object)

    def clear_object(self):
        self.input_text.setText('')
        self.output_text.setText('')
        self.pt = None
        self.get_map()

    def search_object(self):
        address = self.input_text.text()

        try:
            geocoder_requests = "http://geocode-maps.yandex.ru/1.x/?apikey={0}&geocode={1}&format={2}".format(
                "40d1649f-0493-4b70-98ba-98533de7710b", address, 'json'
            )
            response = requests.get(geocoder_requests)

            if response:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_address = 'Address: ' + toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                toponym_coodrinates = toponym["Point"]["pos"]
                if self.checkBox.isChecked():
                    toponym_address += '\npostall code : ' + toponym["metaDataProperty"] \
                        ["GeocoderMetaData"]["Address"]["postal_code"]
                self.output_text.setText(toponym_address)
                self.coord = ','.join(toponym_coodrinates.split())
                self.pt = self.coord
                self.get_map()
            else:
                print("Ошибка исполнения запроса: ", geocoder_requests)
                print("Http status:", response.status_code, f'({response.reason})')
        except Exception as error:
            print(error)
            self.output_text.setText("Error")

    def change_layer(self, layer):
        self.type = layer
        self.get_map()

    def get_map(self):
        # get map screen
        search_api_server = "https://static-maps.yandex.ru/1.x/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
        search_params = {
            "apikey": api_key,
            "ll": self.coord,
            "z": self.zoom,
            'l': self.type
        }
        if self.pt is not None:
            search_params['pt'] = f"{self.pt},pmwtm1~{self.pt},org"
        response = requests.get(search_api_server, params=search_params)

        # recording a screenshot to a file
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        image = QPixmap(self.map_file)
        self.yandex_map.setPixmap(image)

    def change_coord(self):
        x, y = map(float, self.coord.split(','))
        x -= self.direction_x * pow(2, 15 - self.zoom)
        y += self.direction_y * pow(2, 15 - self.zoom)
        self.direction_y, self.direction_x = 0, 0
        coord = str(x) + ',' + str(y)
        self.coord = coord
        self.get_map()

    def keyPressEvent(self, event):
        # key input

        # change coord
        if event.key() == Qt.Key_Up or event.key() == Qt.Key_W:
            self.direction_y = 0.008
        elif event.key() == Qt.Key_Down or event.key() == Qt.Key_S:
            self.direction_y = -0.008
        elif event.key() == Qt.Key_Left or event.key() == Qt.Key_A:
            self.direction_x = 0.008
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_D:
            self.direction_x = - 0.008
        # change size
        elif event.key() == Qt.Key_PageUp:
            if self.zoom < 19:
                self.zoom += 1
        elif event.key() == Qt.Key_PageDown:
            if self.zoom > 1:
                self.zoom -= 1
        else:
            # ignore input
            return
        self.change_coord()
        self.get_map()

    def closeEvent(self, event):
        # delete all files
        os.remove(self.map_file)


if __name__ == '__main__':
    # start program
    app = QApplication(sys.argv)
    ex = Api_map(coord="29.914783,59.891574")
    ex.show()
    sys.exit(app.exec())
