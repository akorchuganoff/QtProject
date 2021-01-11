# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin_cabinet.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sqlite3
import sys
import csv
from PyQt5 import uic

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTextEdit, QFileDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets


# Данная функция отвечает за возврат из окна заполнения проблемы к основному окну
def returnmainwindow():
    global ex, OW
    ex.show()
    OW.close()


# Класс OtherWindow является реализацией диалогового окна, которое отвечает
# за создание проблемы и занесение ее в таблицу проблем
class OtherWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_problem.ui', self)
        self.pushButton.clicked.connect(self.add_problem)

    # Данная функция отвечает
    # за создание проблемы номера и занесения ее в таблицу проблем
    def add_problem(self):
        # Файл problems.csv это файл формата .csv
        # в котором находятся данные о состоянии номеров.
        # Он состоит из n рядов, каждый из которых состоит из двух значений,
        # разделенных ; одно из которых является названием номера, а другое его проблемами
        with open('problems.csv', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            data = []
            for index, row in enumerate(reader):
                data.append(row)
            csvfile.close()

            f = open('problems.csv', encoding='utf-8', mode='w', newline='')
            writer = csv.writer(
                f, delimiter=';', quotechar='"',
                quoting=csv.QUOTE_MINIMAL)

            # из виджета QcomboBox получают значение.
            # Значения являются названиями номеров.
            # Далее запускается цикл по данным из .csv,
            # если значение в первом столбце совпадает с значением  comboBox,
            # то значение проблемы данного номера заменяется на текст полученый из QTextEdit
            a = self.comboBox.currentText()
            problem = self.textEdit.toPlainText()
            print(problem)
            for i in range(len(data)):
                row = [data[i][0]]
                if str(data[i][0]) == str(a):
                    row.append(str(problem))
                    print(1)
                else:
                    row.append(data[i][1])
                writer.writerow(row)
            print('done')
            csvfile.close()
            returnmainwindow()


# Данный класс является реальзацией главного окна
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('admin_cabinet.ui', self)
        # Кнопка поиск
        self.pushButton.clicked.connect(self.run2)
        # Кнопка Показать в окне Свободные номера
        self.pushButton_2.clicked.connect(self.run3)
        # Кнопка Добавить в окне Добавить карточку гостя
        self.pushButton_3.clicked.connect(self.run)
        # Кнопка забронировать в окне Свободные номера
        self.pushButton_4.clicked.connect(self.book)
        # Кнопка Отменить бронирование в окне с=Свободные номера
        self.pushButton_5.clicked.connect(self.unbook)
        # Кнопка Добавить проблему в окне Проблемы номеров
        self.pushButton_6.clicked.connect(self.open_dialog_window)
        # Кнопка Обновить информацию в окне Проблемы номеров
        self.pushButton_7.clicked.connect(self.set_table)
        self.beg = 0
        self.end = 0
        self.beg_index = 0
        self.end_index = 0

        self.pixmap = QPixmap('../проект переписаный/bg.jpg')
        self.bg_1.setPixmap(self.pixmap)
        self.bg_2.setPixmap(self.pixmap)
        self.bg_3.setPixmap(self.pixmap)
        self.zbg_4.setPixmap(self.pixmap)

    # Данная функция отвечает за внесение нового гостя в базу данных.
    # В ней считываются значения из виджетов QlineEdit,
    # и создается новая запись в базе данных 'tourist_base_db.sqlite' в таблице Guests.
    # Затем значения в полях для ввода меняются на пустые строки.
    def run(self):
        con = sqlite3.connect('tourist_base_db.sqlite')
        cur = con.cursor()
        surname = self.lineEdit.text()
        name = self.lineEdit_2.text()
        middle_name = self.lineEdit_3.text()
        city = self.lineEdit_4.text()
        phone = self.lineEdit_5.text()
        car_number = self.lineEdit_6.text()
        date_of_arrival = self.lineEdit_7.text()
        date_of_departure = self.lineEdit_8.text()
        date_of_birth = self.lineEdit_9.text()
        room_number = self.lineEdit_11.text()
        res = cur.execute("""INSERT INTO Guests(Surname, Name, Middle_name, City, Phone, Car_number, Arrival_date,
                                Departure_date, Date_of_birth, Room_number)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (surname, name, middle_name, city, phone, car_number, date_of_arrival,
                                                  date_of_departure, date_of_birth, room_number, ))
        con.commit()
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.lineEdit_9.setText('')
        self.lineEdit_11.setText('')

    # Данная функция отвечает за поиск гостя в базе данных по определенному критерию.
    def run2(self):
        con = sqlite3.connect('tourist_base_db.sqlite')
        cur = con.cursor()
        column = self.comboBox.currentText()
        data = self.lineEdit_17.text()
        # В column записываются критерии, в data - параметры.
        # Если column = Фамилия, осуществляется поиск по фамилии
        if column == 'Фамилия':
            res = cur.execute("""SELECT * FROM Guests
            WHERE Surname = ?""", (data, )).fetchall()
            con.commit()
        # Если column = Имя, осуществляется поиск по имени
        elif column == 'Имя':
            res = cur.execute("""SELECT * FROM Guests
                        WHERE Name = ?""", (data,)).fetchall()
            con.commit()
        # Если column = Период проживания, осуществляется поиск по периоду проживания
        elif column == 'Период проживания в формате ГГГГ-ММ-ДД:ГГГГ-ММ-ДД':
            print(1)
            arrival_date, departure_date = data.split(':')
            a = arrival_date.split('-')
            b = departure_date.split('-')
            print(a, b)
            # Данный блок условий осуществляет проверку на корректность введенных данных
            if len(a) < 3:
                self.lable_13.setText('Неверный формат')
                print(1)
                return
            elif len(b) < 3:
                print(2)
                self.lable_13.setText('Неверный формат')
                return
            elif len(a[0]) != 4 or len(b[0]) != 4:
                print(3)
                self.lable_13.setText('Неверный формат')
                return
            elif len(a[1]) != 2 or len(b[1]) != 2:
                print(4)
                self.lable_13.setText('Неверный формат')
                return
            elif len(a[2]) != 2 or len(b[2]) != 2:
                print(5)
                self.lable_13.setText('Неверный формат')
                return
            else:
                print(6)
                print(arrival_date, departure_date)
                res = cur.execute("""SELECT * FROM Guests
                                    WHERE (Arrival_date >= ? AND Arrival_date <= ?) OR 
                                    (Departure_date >= ? AND Departure_date <= ?)""",
                                  (str(arrival_date), str(departure_date),
                                   str(arrival_date), str(departure_date),)).fetchall()
                print(res)
                con.commit()
                self.label_13.setText('')
        # Если column = Город, осуществляется поиск по городу проживания
        elif column == 'Город':
            res = cur.execute("""SELECT * FROM Guests
                        WHERE City = ?""", (data,)).fetchall()
            con.commit()
        # Если column = Дню рождения, осуществляется поиск по дате рождения
        elif column == 'День рождения':
            res = cur.execute("""SELECT * FROM Guests
                        WHERE Date_of_birth = ?""", (data,)).fetchall()
            con.commit()
        # в этом блоке осужествляется запись полученых данных в таблицу
        self.tableWidget.setRowCount(len(res))
        for i in range(len(res)):
            for j in range(len(res[0])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(res[i][j])))

    # Данная функция отвечает за создание таблицы бронирования.
    def run3(self):
        # Файл booking.csv это файл формата .csv
        # в котором находятся данные о бронировании номеров.
        # Первая строка является строкой заголовков. В ней записаны даты летних месяцев.
        # Дальше идут n рядов, каждый из которых состоит из 93 значений,
        # разделенных ; первое из которых является названием номера, а другие его состоянием в определенную дату.
        with open('booking.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            data = []
            for index, row in enumerate(reader):
                data.append(row)
            a = self.lineEdit_10.text()
            self.beg, self.end = a.split('-')
            self.beg_index = 0
            self.end_index = 0

            q = self.beg.split('/')
            w = self.end.split('/')

            # Проверка корректности даты
            if q[1] > w[1]:
                self.lineEdit_10.setText('Не верный формат')
                return
            elif q[1] == w[1] and q[0] > w[0]:
                self.lineEdit_10.setText('Не верный формат')
                return
            # Создание таблицы основываясь на полученых данных из файла booking.csv
            if (str(self.beg) in data[0]) and (str(self.end) in data[0]):
                for i in range(len(data[0])):
                    if str(data[0][i]) == self.beg:
                        self.beg_index = i
                    if str(data[0][i]) == self.end:
                        self.end_index = i
                self.tableWidget_2.setColumnCount(self.end_index - self.beg_index + 1)
                self.tableWidget_2.setRowCount(len(data) - 1)

                vertheaders = []
                horheaders = []
                for i in range(self.beg_index, self.end_index + 1):
                    horheaders.append(str(data[0][i]))
                for i in range(1, len(data)):
                    vertheaders.append(str(data[i][0]))

                self.tableWidget_2.setVerticalHeaderLabels(vertheaders)
                self.tableWidget_2.setHorizontalHeaderLabels(horheaders)

                for i in range(1, len(data)):
                    for j in range(self.beg_index, self.end_index + 1):
                        self.tableWidget_2.setItem(i - 1, j - self.beg_index, QTableWidgetItem(data[i][j]))
            else:
                self.lineEdit_10.setText('Неверный формат')

    # Данная функция отвечает за бронирование номера.
    # При клике на кнопку состояние выбраной ячейки меняется на 'booked',
    # а также происходит смена состояния в файле booking.csv
    def book(self):
        # Чтения из файла
        with open('booking.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            data = []
            for index, row in enumerate(reader):
                data.append(row)
            csvfile.close()
        # Запись в файл
        with open('booking.csv', 'w', newline='') as csvfile:
            writer = csv.writer(
                csvfile, delimiter=';', quotechar='"',
                quoting=csv.QUOTE_MINIMAL)
            # выбраных элементов
            massive = self.tableWidget_2.selectedItems()
            # массив координат выбранных элементов
            mas = []
            for elem in massive:
                # добавление координат в массив. Их получение происходит посредством методов .row и .count
                mas.append((elem.row() + 1, elem.column() + self.beg_index))
            # Запись измененных данных в файл
            for i in range(len(data)):
                row = []
                for j in range(len(data[0])):
                    if (i, j) in mas:
                        row.append('booked')
                    else:
                        row.append(data[i][j])
                writer.writerow(row)
            csvfile.close()
        # Обновление таблицы
        self.run3()

    # функция отвечает за смены состояния ячейки таблицы с 'booked' на 'free'.
    # Работает идентично функции self.book()
    def unbook(self):
        with open('booking.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            data = []
            for index, row in enumerate(reader):
                data.append(row)
            csvfile.close()
        with open('booking.csv', 'w', newline='') as csvfile:
            writer = csv.writer(
                csvfile, delimiter=';', quotechar='"',
                quoting=csv.QUOTE_MINIMAL)
            massive = self.tableWidget_2.selectedItems()
            mas = []
            for elem in massive:
                mas.append((elem.row() + 1, elem.column() + self.beg_index))
            for i in range(len(data)):
                row = []
                for j in range(len(data[0])):
                    if (i, j) in mas:
                        row.append('Free')
                    else:
                        row.append(data[i][j])
                writer.writerow(row)
            csvfile.close()
        self.run3()

    # Данная функция отвечает за открытие диалогового окна
    # с формой записи проблем номера
    def open_dialog_window(self):
        global OW
        ex.hide()
        OW.show()
        self.set_table()

    # Данная функция отвечает за обновление данных в таблице с проблемами
    def set_table(self):
        with open('problems.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            data = []
            for index, row in enumerate(reader):
                data.append(row)
            csvfile.close()
        self.tableWidget_3.setColumnCount(1)
        self.tableWidget_3.setRowCount(len(data))
        vertheaders = []
        horheaders = ['Проблемы']
        for i in range(len(data)):
            vertheaders.append(str(data[i][0]))
        self.tableWidget_3.setVerticalHeaderLabels(vertheaders)
        self.tableWidget_3.setHorizontalHeaderLabels(horheaders)
        for i in range(0, len(data)):
            a = QTextEdit()
            a.setText(str(data[i][1]))
            self.tableWidget_3.setCellWidget(i, 0, a)
        self.tableWidget_3.resizeColumnToContents(0)
        for i in range(len(data)):
            self.tableWidget_3.resizeRowToContents(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    OW = OtherWindow()
    ex.show()
    sys.exit(app.exec())