# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add_dish.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(540, 618)
        MainWindow.setMinimumSize(QtCore.QSize(540, 0))
        MainWindow.setMaximumSize(QtCore.QSize(540, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalFrame = QtWidgets.QFrame(self.centralwidget)
        self.verticalFrame.setGeometry(QtCore.QRect(0, 0, 542, 608))
        self.verticalFrame.setObjectName("verticalFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalFrame)
        self.verticalLayout.setContentsMargins(22, 11, 22, 22)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(0, -1, -1, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.addDishHeaderLabel = QtWidgets.QLabel(self.verticalFrame)
        self.addDishHeaderLabel.setEnabled(True)
        self.addDishHeaderLabel.setStyleSheet("margin-top: 8px;\n"
"margin-bottom:8px;\n"
"  width: 435px;\n"
"  height: 24px;\n"
"  color: #2d2c2c;\n"
"  font-size: 20px;\n"
"  font-family: Inter, \"Extra Bold\";\n"
"  font-weight: 800;\n"
"  text-align: left;\n"
"  vertical-align: top")
        self.addDishHeaderLabel.setObjectName("addDishHeaderLabel")
        self.verticalLayout_2.addWidget(self.addDishHeaderLabel)
        self.nameOfDishLineEdit = QtWidgets.QLineEdit(self.verticalFrame)
        self.nameOfDishLineEdit.setStyleSheet("background-color:#ffffff;\n"
"border-radius:4%;\n"
"border:2px solid rgba(100, 100, 100, 25);\n"
"\n"
"color: #2d2c2c;\n"
"\n"
"width:360px;\n"
"height:32px;\n"
"\n"
"padding-left: 8px;\n"
"position:absolute;\n"
"text-align:left;\n"
"vertical-align:text-top;\n"
"\n"
"font-size:14px;\n"
"font-family:Inter;\n"
"left:12px;\n"
"top:8px;")
        self.nameOfDishLineEdit.setText("")
        self.nameOfDishLineEdit.setMaxLength(32770)
        self.nameOfDishLineEdit.setCursorPosition(0)
        self.nameOfDishLineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.nameOfDishLineEdit.setClearButtonEnabled(False)
        self.nameOfDishLineEdit.setObjectName("nameOfDishLineEdit")
        self.verticalLayout_2.addWidget(self.nameOfDishLineEdit)
        self.infoDishPlainTextEdit = QtWidgets.QPlainTextEdit(self.verticalFrame)
        self.infoDishPlainTextEdit.setStyleSheet("background-color:#ffffff;\n"
"border-radius:4%;\n"
"border:2px solid rgba(100, 100, 100, 25);\n"
"\n"
"color: #2d2c2c;\n"
"\n"
"width:360px;\n"
"height:32px;\n"
"\n"
"padding: 8px;\n"
"position:absolute;\n"
"text-align:left;\n"
"vertical-align:text-top;\n"
"\n"
"font-size:14px;\n"
"font-family:Inter;\n"
"left:12px;\n"
"top:8px;")
        self.infoDishPlainTextEdit.setPlainText("")
        self.infoDishPlainTextEdit.setObjectName("infoDishPlainTextEdit")
        self.verticalLayout_2.addWidget(self.infoDishPlainTextEdit)
        self.calculateAutoNutritValuecheckBox = QtWidgets.QCheckBox(self.verticalFrame)
        self.calculateAutoNutritValuecheckBox.setEnabled(True)
        self.calculateAutoNutritValuecheckBox.setStyleSheet("margin-top: 8px;\n"
"background-color: none;\n"
"border: none;\n"
"\n"
"text-align:left;\n"
"vertical-align:text-top;\n"
"font-size:12px;\n"
"font-family:Inter;\n"
"line-height:auto;\n"
"border-style:hidden;\n"
"outline:none;\n"
"\n"
"color:#30353b;\n"
"text-align:left;\n"
"vertical-align:text-top;\n"
"font-size:14px;\n"
"font-family:Inter;\n"
"line-height:auto;\n"
"border-style:hidden;\n"
"outline:none;\n"
"width:435px;")
        self.calculateAutoNutritValuecheckBox.setChecked(False)
        self.calculateAutoNutritValuecheckBox.setObjectName("calculateAutoNutritValuecheckBox")
        self.verticalLayout_2.addWidget(self.calculateAutoNutritValuecheckBox)
        self.nutritiansHorizontalLayout = QtWidgets.QHBoxLayout()
        self.nutritiansHorizontalLayout.setObjectName("nutritiansHorizontalLayout")
        self.kaloriesLineEdit = QtWidgets.QLineEdit(self.verticalFrame)
        self.kaloriesLineEdit.setStyleSheet("background-color:#ffffff;\n"
"border-radius:4%;\n"
"border:2px solid rgba(100, 100, 100, 25);\n"
"\n"
"color: #2d2c2c;\n"
"\n"
"width:360px;\n"
"height:32px;\n"
"\n"
"padding-left: 8px;\n"
"position:absolute;\n"
"text-align:left;\n"
"vertical-align:text-top;\n"
"\n"
"font-size:14px;\n"
"font-family:Inter;\n"
"left:12px;\n"
"top:8px;")
        self.kaloriesLineEdit.setText("")
        self.kaloriesLineEdit.setCursorPosition(0)
        self.kaloriesLineEdit.setClearButtonEnabled(False)
        self.kaloriesLineEdit.setObjectName("kaloriesLineEdit")
        self.nutritiansHorizontalLayout.addWidget(self.kaloriesLineEdit)
        self.proteinsLineEdit = QtWidgets.QLineEdit(self.verticalFrame)
        self.proteinsLineEdit.setStyleSheet("background-color:#ffffff;\n"
"border-radius:4%;\n"
"border:2px solid rgba(100, 100, 100, 25);\n"
"\n"
"color: #2d2c2c;\n"
"\n"
"height:32px;\n"
"\n"
"padding-left: 8px;\n"
"position:absolute;\n"
"text-align:left;\n"
"vertical-align:text-top;\n"
"\n"
"font-size:14px;\n"
"font-family:Inter;\n"
"left:12px;\n"
"top:8px;")
        self.proteinsLineEdit.setText("")
        self.proteinsLineEdit.setCursorPosition(0)
        self.proteinsLineEdit.setClearButtonEnabled(False)
        self.proteinsLineEdit.setObjectName("proteinsLineEdit")
        self.nutritiansHorizontalLayout.addWidget(self.proteinsLineEdit)
        self.fatsLineEdit = QtWidgets.QLineEdit(self.verticalFrame)
        self.fatsLineEdit.setStyleSheet("background-color:#ffffff;\n"
"border-radius:4%;\n"
"border:2px solid rgba(100, 100, 100, 25);\n"
"\n"
"color: #2d2c2c;\n"
"\n"
"height:32px;\n"
"\n"
"padding-left: 8px;\n"
"position:absolute;\n"
"text-align:left;\n"
"vertical-align:text-top;\n"
"\n"
"font-size:14px;\n"
"font-family:Inter;\n"
"left:12px;\n"
"top:8px;")
        self.fatsLineEdit.setText("")
        self.fatsLineEdit.setCursorPosition(0)
        self.fatsLineEdit.setClearButtonEnabled(False)
        self.fatsLineEdit.setObjectName("fatsLineEdit")
        self.nutritiansHorizontalLayout.addWidget(self.fatsLineEdit)
        self.carbohLineEdit = QtWidgets.QLineEdit(self.verticalFrame)
        self.carbohLineEdit.setStyleSheet("background-color:#ffffff;\n"
"border-radius:4%;\n"
"border:2px solid rgba(100, 100, 100, 25);\n"
"\n"
"color: #2d2c2c;\n"
"\n"
"height:32px;\n"
"\n"
"padding-left: 8px;\n"
"position:absolute;\n"
"text-align:left;\n"
"vertical-align:text-top;\n"
"\n"
"font-size:14px;\n"
"font-family:Inter;\n"
"left:12px;\n"
"top:8px;")
        self.carbohLineEdit.setText("")
        self.carbohLineEdit.setCursorPosition(0)
        self.carbohLineEdit.setClearButtonEnabled(False)
        self.carbohLineEdit.setObjectName("carbohLineEdit")
        self.nutritiansHorizontalLayout.addWidget(self.carbohLineEdit)
        self.verticalLayout_2.addLayout(self.nutritiansHorizontalLayout)
        self.ingredientsHeaderLabel = QtWidgets.QLabel(self.verticalFrame)
        self.ingredientsHeaderLabel.setEnabled(True)
        self.ingredientsHeaderLabel.setStyleSheet("margin-top: 8px;\n"
"margin-bottom:8px;\n"
"  width: 435px;\n"
"  height: 24px;\n"
"  color: #2d2c2c;\n"
"  font-size: 20px;\n"
"  font-family: Inter, \"Extra Bold\";\n"
"  font-weight: 800;\n"
"  text-align: left;\n"
"  vertical-align: top")
        self.ingredientsHeaderLabel.setObjectName("ingredientsHeaderLabel")
        self.verticalLayout_2.addWidget(self.ingredientsHeaderLabel)
        self.ingrHorizontalLayout1 = QtWidgets.QHBoxLayout()
        self.ingrHorizontalLayout1.setObjectName("ingrHorizontalLayout1")
        self.ingredientComboBox_1 = QtWidgets.QComboBox(self.verticalFrame)
        self.ingredientComboBox_1.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.ingredientComboBox_1.setAccessibleName("")
        self.ingredientComboBox_1.setStyleSheet("                QComboBox {\n"
"                    border: 2px solid rgba(100, 100, 100, 25);\n"
"                    color: #2d2c2c;\n"
"                    border-radius: 4%;\n"
"                    padding: 1px 18px 1px 3px;\n"
"                    max-height: 32px;\n"
"                    min-height: 32px;\n"
"                    font-size: 14px; \n"
"                    font-family: Inter; \n"
"                    padding-left: 8px;\n"
"                }\n"
"                QComboBox::drop-down {\n"
"                    border-left-width: 1px;\n"
"                    border-left-color: gray;\n"
"                    border-left-style: none;\n"
"                    border-top-right-radius: 4%;\n"
"                    border-bottom-right-radius: 4%;\n"
"                    font-size: 14px; \n"
"                    font-family: Inter;\n"
"                    padding-left: 8px; \n"
"                }")
        self.ingredientComboBox_1.setDuplicatesEnabled(False)
        self.ingredientComboBox_1.setFrame(True)
        self.ingredientComboBox_1.setObjectName("ingredientComboBox_1")
        self.ingredientComboBox_1.addItem("")
        self.ingrHorizontalLayout1.addWidget(self.ingredientComboBox_1)
        self.countIngredientsSpinBox_1 = QtWidgets.QSpinBox(self.verticalFrame)
        self.countIngredientsSpinBox_1.setMinimumSize(QtCore.QSize(86, 0))
        self.countIngredientsSpinBox_1.setMaximumSize(QtCore.QSize(86, 16777215))
        self.countIngredientsSpinBox_1.setStyleSheet("                QSpinBox {\n"
"                    border: 2px solid rgba(100, 100, 100, 25);\n"
"                    color: #2d2c2c;\n"
"                    border-radius: 4%;\n"
"                    padding: 1px 18px 1px 3px;\n"
"                    height: 32px;\n"
"                    min-width: 56px;\n"
"                    max-width: 56px;\n"
"                    font-size: 14px; \n"
"                    font-family: Inter; \n"
"                    padding-left: 8px;\n"
"                }")
        self.countIngredientsSpinBox_1.setProperty("value", 1)
        self.countIngredientsSpinBox_1.setObjectName("countIngredientsSpinBox_1")
        self.ingrHorizontalLayout1.addWidget(self.countIngredientsSpinBox_1)
        self.unitIngredLoabel_1 = QtWidgets.QLabel(self.verticalFrame)
        self.unitIngredLoabel_1.setStyleSheet("background-color: none;\n"
"color: #2d2c2c;\n"
"border:none;\n"
"margin-top: 8px;\n"
"margin-bottom:8px;\n"
"\n"
"text-align:left;\n"
"vertical-align:text-top;\n"
"font-size:14px;\n"
"font-family:Inter;\n"
"line-height:auto;\n"
"border-style:hidden;\n"
"outline:none;\n"
"\n"
"min-width: 56px;\n"
"max-width: 56px;")
        self.unitIngredLoabel_1.setScaledContents(False)
        self.unitIngredLoabel_1.setWordWrap(True)
        self.unitIngredLoabel_1.setObjectName("unitIngredLoabel_1")
        self.ingrHorizontalLayout1.addWidget(self.unitIngredLoabel_1)
        self.verticalLayout_2.addLayout(self.ingrHorizontalLayout1)
        self.ingrHorizontalLayout2 = QtWidgets.QHBoxLayout()
        self.ingrHorizontalLayout2.setObjectName("ingrHorizontalLayout2")
        self.ingredientComboBox_2 = QtWidgets.QComboBox(self.verticalFrame)
        self.ingredientComboBox_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.ingredientComboBox_2.setAccessibleName("")
        self.ingredientComboBox_2.setStyleSheet("                QComboBox {\n"
"                    border: 2px solid rgba(100, 100, 100, 25);\n"
"                    color: #2d2c2c;\n"
"                    border-radius: 4%;\n"
"                    padding: 1px 18px 1px 3px;\n"
"                    max-height: 32px;\n"
"                    min-height: 32px;\n"
"                    font-size: 14px; \n"
"                    font-family: Inter; \n"
"                    padding-left: 8px;\n"
"                }\n"
"                QComboBox::drop-down {\n"
"                    border-left-width: 1px;\n"
"                    border-left-color: gray;\n"
"                    border-left-style: none;\n"
"                    border-top-right-radius: 4%;\n"
"                    border-bottom-right-radius: 4%;\n"
"                    font-size: 14px; \n"
"                    font-family: Inter;\n"
"                    padding-left: 8px; \n"
"                }")
        self.ingredientComboBox_2.setDuplicatesEnabled(False)
        self.ingredientComboBox_2.setFrame(True)
        self.ingredientComboBox_2.setObjectName("ingredientComboBox_2")
        self.ingredientComboBox_2.addItem("")
        self.ingrHorizontalLayout2.addWidget(self.ingredientComboBox_2)
        self.countIngredientsSpinBox_2 = QtWidgets.QSpinBox(self.verticalFrame)
        self.countIngredientsSpinBox_2.setMinimumSize(QtCore.QSize(86, 0))
        self.countIngredientsSpinBox_2.setMaximumSize(QtCore.QSize(86, 16777215))
        self.countIngredientsSpinBox_2.setStyleSheet("                QSpinBox {\n"
"                    border: 2px solid rgba(100, 100, 100, 25);\n"
"                    color: #2d2c2c;\n"
"                    border-radius: 4%;\n"
"                    padding: 1px 18px 1px 3px;\n"
"                    height: 32px;\n"
"                    min-width: 56px;\n"
"                    max-width: 56px;\n"
"                    font-size: 14px; \n"
"                    font-family: Inter; \n"
"                    padding-left: 8px;\n"
"                }")
        self.countIngredientsSpinBox_2.setProperty("value", 1)
        self.countIngredientsSpinBox_2.setObjectName("countIngredientsSpinBox_2")
        self.ingrHorizontalLayout2.addWidget(self.countIngredientsSpinBox_2)
        self.unitIngredLoabel_2 = QtWidgets.QLabel(self.verticalFrame)
        self.unitIngredLoabel_2.setStyleSheet("background-color: none;\n"
"color: #2d2c2c;\n"
"border:none;\n"
"margin-top: 8px;\n"
"margin-bottom:8px;\n"
"\n"
"text-align:left;\n"
"vertical-align:text-top;\n"
"font-size:14px;\n"
"font-family:Inter;\n"
"line-height:auto;\n"
"border-style:hidden;\n"
"outline:none;\n"
"\n"
"min-width: 56px;\n"
"max-width: 56px;")
        self.unitIngredLoabel_2.setScaledContents(False)
        self.unitIngredLoabel_2.setWordWrap(True)
        self.unitIngredLoabel_2.setObjectName("unitIngredLoabel_2")
        self.ingrHorizontalLayout2.addWidget(self.unitIngredLoabel_2)
        self.verticalLayout_2.addLayout(self.ingrHorizontalLayout2)
        self.addDishPushButton = QtWidgets.QPushButton(self.verticalFrame)
        self.addDishPushButton.setStyleSheet("QPushButton{\n"
"height:32px;\n"
"width:auto;\n"
"\n"
"color: #30353B;\n"
"background: #ADDC81;\n"
"\n"
"text-align:center;\n"
"vertical-align:center;\n"
"font-size:12px;\n"
"font-family:Inter;\n"
"line-height:auto;\n"
"font-weight: bold;\n"
"\n"
"border-radius:4%;\n"
"border: 2 px solid #ADFF81;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background: #AAAA81;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background: #AAAAFF;\n"
"}\n"
"\n"
"\n"
"")
        self.addDishPushButton.setObjectName("addDishPushButton")
        self.verticalLayout_2.addWidget(self.addDishPushButton)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Умное меню - Добавить блюдо"))
        self.addDishHeaderLabel.setText(_translate("MainWindow", "Заполните информацию о блюде"))
        self.nameOfDishLineEdit.setPlaceholderText(_translate("MainWindow", "Введите название блюда"))
        self.infoDishPlainTextEdit.setPlaceholderText(_translate("MainWindow", "Введите описание блюда"))
        self.calculateAutoNutritValuecheckBox.setText(_translate("MainWindow", "Заполнять калории автоматически"))
        self.kaloriesLineEdit.setPlaceholderText(_translate("MainWindow", "Введите количество калорий"))
        self.proteinsLineEdit.setPlaceholderText(_translate("MainWindow", "Б:"))
        self.fatsLineEdit.setPlaceholderText(_translate("MainWindow", "Ж:"))
        self.carbohLineEdit.setPlaceholderText(_translate("MainWindow", "У:"))
        self.ingredientsHeaderLabel.setText(_translate("MainWindow", "Ингредиенты:"))
        self.ingredientComboBox_1.setCurrentText(_translate("MainWindow", "Помидор"))
        self.ingredientComboBox_1.setItemText(0, _translate("MainWindow", "Помидор"))
        self.unitIngredLoabel_1.setText(_translate("MainWindow", "ед."))
        self.ingredientComboBox_2.setCurrentText(_translate("MainWindow", "Помидор"))
        self.ingredientComboBox_2.setItemText(0, _translate("MainWindow", "Помидор"))
        self.unitIngredLoabel_2.setText(_translate("MainWindow", "ед."))
        self.addDishPushButton.setText(_translate("MainWindow", "Добавить"))