from PyQt5 import QtWidgets, uic
from datetime import datetime
import sqlite3

from db_controller import DatabaseController

class InspectDishWindow:
    def __init__(self):

        self.win = uic.loadUi("static/ui/ispect_dish.ui")
        self.db = DatabaseController()
        # self.load_dish_data(dish_id)

        print("Окно открыто")

        # Подключение обработчиков кнопок
        # self.win.addStoragePushButton.clicked.connect(self.add_storage_item)
        # self.win.cancelStorageItemPushButton.clicked.connect(self.win.close)

        self.win.show()

    def load_dish_data(self, dish_id):
        pass