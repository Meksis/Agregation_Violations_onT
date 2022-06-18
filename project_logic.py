import sys
import openpyxl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from ui4 import Ui_MainWindow
import pandas as pd
import sqlite3 as sq
import pymysql
from pymysql import *
from auth_info import *
import os

user_name = 'GSP_main'
user_data = auth_info[user_name]


class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        #self.setFixedSize(round(screen_w / 2), round(screen_w / 1.9))
        #self.setFixedSize(800, 691)
        self.setFixedSize(800, 950)
        #self.setFixedSize()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.is_save = False

        self.ui.data.setInputMask('00.00.0000  00:00')
        self.ui.shirota.setInputMask('00.000000')
        self.ui.dolgota.setInputMask('00.000000')

        self.ui.pushButton.clicked.connect(self.text_data)
        #self.ui.pushButton.clicked.connect(self.saveex)
        self.ui.pushButton.clicked.connect(self.data_uploading)

        self.ui.pushButton_2.clicked.connect(self.ui.data.clear)
        self.ui.pushButton_2.clicked.connect(self.ui.object.clear)
        self.ui.pushButton_2.clicked.connect(self.ui.organization.clear)
        self.ui.pushButton_2.clicked.connect(self.ui.fio_insp.clear)
        self.ui.pushButton_2.clicked.connect(self.ui.violation.clear)
        self.ui.pushButton_2.clicked.connect(self.ui.fionar.clear)
        self.ui.pushButton_2.clicked.connect(self.ui.fiopro.clear)
        self.ui.pushButton_2.clicked.connect(self.ui.fiodoc.clear)
        self.ui.pushButton_2.clicked.connect(self.ui.shirota.clear)
        self.ui.pushButton_2.clicked.connect(self.ui.dolgota.clear)

    def text_data(self):
        data_correct = 1
        self.mas_data=[]
        data = self.ui.data.text().replace('.', '-')
        latitude = self.ui.shirota.text()
        longitude = self.ui.dolgota.text()




        if len(data) < 16:
            data_correct = 0
            print('Insufficient length of data or time')
            QMessageBox.critical(self, "Ошибка ", f"Пожалуйста, введите дату и время в форматах dd.mm.yyyy и hh:mm:ss соответственно", QMessageBox.Ok)

        if len(latitude) < 9 or len(longitude) < 9:
            data_correct = 0
            print('Incorrect length of coordinates')
            QMessageBox.critical(self, "Ошибка ", f"Пожалуйста, введите полные координаты точки", QMessageBox.Ok)

        if data_correct:
            time = data[ -6 : ].split(':')              # Время необходимо указывать в формате hh:mm:ss
            date = data[  : -7 ].split('-')            # Дату необходимо указывать в формате dd.mm.yyyy
            date = str(date[2] + '-' + date[1] + '-' + date[0]).split('-')

            time_err = 0
            date_err = 0

            for counter, time_in in enumerate(time):
                if counter == 0:
                    if int(date[counter + 1]) not in range(0, 13):
                        date_err = 1

                    if int(time_in) not in range(0, 25):
                        time_err = 1

                elif counter == 1:
                    if int(date[counter + 1]) not in range(1, 32):
                        date_err = 1

                    if int(time_in) not in range(0, 60):
                        time_err = 1
                else:
                    if int(time_in) not in range(0, 60):
                        time_err = 1

            if date_err or time_err:
                time_new = ''
                time_new += '        ' if date_err else f'{date[0]}{date[1]}{date[2]} '
                time_new += '      ' if time_err else f'{time[0]}{time[1]}'
                self.ui.data.setText(time_new)

                if date_err and time_err:
                    message_out = 'введенные дату и время'
                elif date_err:
                    message_out = 'введенную дату'
                else:
                    message_out = 'введенное время'

                print('Date or time error')
                QMessageBox.critical(self, "Ошибка ", f"Пожалуйста, исправьте {message_out}", QMessageBox.Ok)
                
            else:
                self.is_save = 1   

            if self.is_save:
                data = '-'.join(date) + ' ' + ':'.join(time)
                object=self.ui.object.text()
                organization=self.ui.organization.text()
                fio_insp=self.ui.fio_insp.text()
                violation=self.ui.violation.text()
                fionar=self.ui.fionar.text()
                fiopro=self.ui.fiopro.text()
                fiodoc=self.ui.fiodoc.text()
                shirota = self.ui.shirota.text()
                dolgota = self.ui.dolgota.text()
                self.mas_data.append(data)
                self.mas_data.append(object)
                self.mas_data.append(organization)
                self.mas_data.append(fio_insp)
                self.mas_data.append(violation)
                self.mas_data.append(fionar)
                self.mas_data.append(fiopro)
                self.mas_data.append(fiodoc)
                self.mas_data.append(shirota)
                self.mas_data.append(dolgota)

    '''def saveex(self):
        df= pd.read_excel('PAA.xlsx')
        excel_file = openpyxl.open('PAA.xlsx',read_only=False)
        sheet=excel_file.active
        rows = df.shape[0]+2
        #if len(self.mas_data) % 2 == 0 and len(self.mas_data) >= 8:
        for i in self.mas_data:
            sheet[f'A{rows}'] = self.mas_data[-10]
            sheet[f'B{rows}'] = self.mas_data[-9]
            sheet[f'C{rows}'] = self.mas_data[-8]
            sheet[f'D{rows}'] = self.mas_data[-7]
            sheet[f'E{rows}'] = self.mas_data[-6]
            sheet[f'F{rows}'] = self.mas_data[-5]
            sheet[f'G{rows}'] = self.mas_data[-4]
            sheet[f'H{rows}'] = self.mas_data[-3]
            sheet[f'I{rows}'] = self.mas_data[-2]
            sheet[f'J{rows}'] = self.mas_data[-1]
            excel_file.save('PAA.xlsx')




        self.mas_data = []

                #if '.' and ':' not in self.mas_data[-8]:
                #    QMessageBox.critical(self, "Ошибка ", "Исправьте поле с датой", QMessageBox.Ok)
                #    break
                #else:
                #    excel_file.save('PAA.xlsx')
    '''

    def data_uploading(self):

        '''os.mkdir('Databases/Violations/') if not os.path.isdir("Databases/Violations/") else print()


        connect = sq.connect('Databases/Violations/violations.db')
        '''

        if self.is_save:

            try:
                connection = connect(
                    host = user_data['host'],
                    user = user_name,
                    password = user_data['password'],
                    database = user_data['db_name'],
                    charset='utf8',
                    cursorclass = cursors.DictCursor
                    )

                print('connection established')

            except Error as e:
                print(e)
                raise e
            
            try:
                cursor = connection.cursor()

                send_commitcursor.execute('''
                    CREATE TABLE IF NOT EXISTS VIOLATIONS (
                    Дата_и_время varchar(128), 
                    Объект varchar(128), 
                    Оганизация_инспектора varchar(128), 
                    ФИО_инспектора varchar(128), 
                    Нарушение varchar(128), 
                    ФИО_нарушителя varchar(128), 
                    ФИО_проверяющего varchar(128), 
                    ФИО_докладчика varchar(128), 
                    Широта real, 
                    Долгота real
                    )
                    CHARACTER SET utf8
                    ''', connection, cursor)


                print('table checked')

                cursor.execute('''INSERT INTO VIOLATIONS VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                        (self.mas_data[-10],
                        self.mas_data[-9],
                        self.mas_data[-8],
                        self.mas_data[-7],
                        self.mas_data[-6],
                        self.mas_data[-5],
                        self.mas_data[-4],
                        'Я русский',
                        float(self.mas_data[-2]),
                        float(self.mas_data[-1]))
                        )

                connection.commit()

            except:
                print()

            finally:
                cursor.execute('''SELECT * FROM VIOLATIONS''')
                all_data = cursor.fetchall()[-1]
                print(all_data)
                search_res = table_searching(cursor, ['1111-11-11  00:00', '2000-12-31  23:59'])

                for i in search_res:
                    print(i, '\n')

                connection.close()
                print('data saved into table')


def send_commit(sql_req, connect, curs, args=[]):
    curs.execute(f''' {sql_req} ''', args)
    connect.commit()

def table_searching(cursor, search_limits):

    cursor.execute('''
        SELECT count(*) FROM VIOLATIONS WHERE Дата_и_время BETWEEN %s AND %s;
        ''', (search_limits[0], search_limits[1]))
    prnt(cursor.fetchall(), '\n')

    cursor.execute('''
        SELECT * FROM VIOLATIONS WHERE Дата_и_время BETWEEN %s AND %s;
        ''', (search_limits[0], search_limits[1]))

    return(cursor.fetchall())

app = QtWidgets.QApplication([])


screen = app.primaryScreen().availableGeometry()        # Получаем значения доступного для использования пространства монитора 
screen_w=screen.width()                                 # Записываем доступную ширину монитора
screen_h=screen.height()                                # Записываем доступную высоту монитора

screen_w=1080
screen_h=720

'''980 * 736
1080 * 720
1920 * 1080'''

application = Example()

application.setObjectName('MainWindow')             # Присваиваем экземпляру внутреннее программное имя
application.setWindowTitle('Ввод данных')

application.show()

sys.exit(app.exec())