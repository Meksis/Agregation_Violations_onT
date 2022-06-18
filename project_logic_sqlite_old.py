import sys
import openpyxl
from openpyxl import *
from PyQt5.QtWidgets import *   # pip install pyqt5 , библиотека для создания интерфейса
import PyQt5.QtWidgets
from PyQt5.QtWebEngineWidgets import *      # pip install PyQtWebEngine
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from ui6 import Ui_MainWindow
import pandas as pd
import sqlite3 as sq
#import pymysql
#from pymysql import *
#from auth_info import *
import os




#user_name = 'GSP_main'
#user_data = auth_info[user_name]

is_save_global = 0



class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        #self.setFixedSize(round(screen_w / 2), round(screen_w / 1.9))
        #self.setFixedSize(800, 691)
        self.setFixedSize(800, 950)
        #self.setFixedSize()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.is_save = False
        self.check_button = False
        self.s = ''
        

        self.ui.data.setInputMask('00.00.0000  00:00')
        self.ui.shirota.setInputMask('00.00000000000000000000')
        self.ui.dolgota.setInputMask('00.00000000000000000000')

        self.ui.pushButton_4.clicked.connect(self.jsonsave)
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


        if len(data) < 17:
            data_correct = 0
            print('Insufficient length of data or time')
            QMessageBox.critical(self, "Ошибка ", f"Пожалуйста, введите дату и время в форматах dd.mm.yyyy и hh:mm:ss соответственно", QMessageBox.Ok)

        if len(latitude) < 10 or len(longitude) < 10:
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

                print('\nDate or time error')
                is_save_switch(self.is_save)
                QMessageBox.critical(self, "Ошибка ", f"Пожалуйста, исправьте {message_out}", QMessageBox.Ok)
                
            else:

                self.is_save = True
                is_save_switch(self.is_save)
                #is_save_global = True if self.is_save else False

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

                #is_save_global = True if self.is_save else False
                #print(f'\nis_save_global in text data - {is_save_global}\n')

    def data_uploading(self):

        if self.is_save:
            #is_save_global = True if self.is_save else False
            #print('\n', is_save_global, 'is_save_global\n')
            self.is_save = False
            try:
                '''connection = connect(
                                                                    host = user_data['host'],
                                                                    user = user_name,
                                                                    password = user_data['password'],
                                                                    database = user_data['db_name'],
                                                                    charset='utf8',
                                                                    cursorclass = cursors.DictCursor
                                                                    )'''
                os.mkdir('Databases/Violations/') if not os.path.isdir("Databases/Violations/") else print()
                connection = sq.connect('Databases/Violations/violations.db')
                
                print('connection established')

            except Error as e:
                print(e)
                raise e
            
            try:
                cursor = connection.cursor()

                cursor.execute('''
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
                    ''')

                connection.commit()

                print('Table checked')


                cursor.execute('''INSERT INTO VIOLATIONS VALUES (?,?,?,?,?,?,?,?,?,?)''',
                        [self.mas_data[-10],
                        self.mas_data[-9],
                        self.mas_data[-8],
                        self.mas_data[-7],
                        self.mas_data[-6],
                        self.mas_data[-5],
                        self.mas_data[-4],
                        self.mas_data[-3],
                        float(self.mas_data[-2]),
                        float(self.mas_data[-1])]

                        )

                connection.commit()
                print('Insertion completed\n')

            finally:
                #cursor.execute('''SELECT * FROM VIOLATIONS''')
                #all_data = cursor.fetchall()[-1]
                pass
                #print(is_save_global, 'ISSAVEGLOBALHERE')
                '''search_res = table_searching(cursor, data_slice, is_save_global)

                for i in search_res:
                    print(i, '\n')

                connection.close()
                print('data saved into table')
                '''

    def jsonsave(self):


        self.file,_ = QFileDialog.getOpenFileName(None, "Title", "", "JSON (*.json)")#выбираем файл json
        if self.file:
            self.handle = open(self.file, "r")  # открываем файл json
            self.check_button = True
            self.s += self.handle.read()


class search_window(QWidget):
    def __init__(self):
        super(search_window, self).__init__()
        self.setFixedSize(800, 950)
        self.is_save = is_save_global
        #self.search_limits = search_limits
        self.is_correct = False


        self.setupUI()

    def setupUI(self):

        self.setObjectName('SearchWindow')
        self.setWindowTitle('Статистика нарушений')

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName('search_grid_layout')


        

        

        self.area = QScrollArea(self)               # Создание объекта, способного реализовывать прокрутку своего содержимого. При множестве найденных результатов поиска это - лучшее решение
        #self.area.setFont(font)                     # Форматируем объект. В данном случае - только меняем размер шрифта
        self.area.setWidgetResizable(True)          # Говорим проге, что содержимое можно прокручивать

        self.data_begin_input = QLineEdit(self)
        self.data_end_input = QLineEdit(self)

        self.data_begin_input.setObjectName('data_1')
        self.data_end_input.setObjectName('data_2')

        self.data_begin_input.setPlaceholderText('Время начала выборки (гггг.мм.дд чч:мм)')
        self.data_end_input.setPlaceholderText('Время конца выборки (гггг.мм.дд чч:мм)')

        #self.data_begin_pod = QLabel(self)
        #self.data_end_pod = QLabel(self)

        #self.data_begin_pod.setText('Введите дату и время начала выборки в формате гггг.мм.дд чч:мм')
        #self.data_end_pod.setText('Введите дату и время конца выборки в формате гггг.мм.дд чч:мм')

        self.data_begin_input.setInputMask('00.00.0000  00:00')
        self.data_end_input.setInputMask('00.00.0000  00:00')

        self.find_button = QPushButton(self)
        self.find_button.setText('Поиск')
        self.find_button.clicked.connect(self.find_button_reaction)



       # data_slice = ['1111-11-11  00:00', '1111-12-30  20:59']

        self.grid_layout.addWidget(self.find_button, 10, 0)
        self.grid_layout.addWidget(self.data_begin_input, 8, 0)
        #self.grid_layout.addWidget(self.area, row, column, row_span, column_span)

        self.grid_layout.addWidget(self.data_end_input, 9, 0)
        self.grid_layout.addWidget(self.area, 0, 0, 2, 1)
        #self.grid_layout.addWidget(self.area, 3, 1, 2, 1)
        #self.grid_layout.addWidget(self.area, 3, 1, 2, 1)

    def find_button_reaction(self):
        data_correct = 1
        # 1111.11.11  11:11
        #print('search button pressed')
        data_begin = self.data_begin_input.text().replace('.', '-')
        data_end = self.data_end_input.text().replace('.', '-')
        
        if len(data_begin) < 17 or len(data_end) < 17:
            data_correct = 0
            print('Insufficient length of data or time')
            #QMessageBox.critical(self, "Ошибка ", f"Пожалуйста, введите дату и время в форматах dd.mm.yyyy и hh:mm:ss соответственно", QMessageBox.Ok)


        data_lst = [data_begin, data_end]
        search_limits = []

        print(f'''{'Inputed data correct' if data_correct else 'Inputed data incorrect'}\n''')

        if data_correct:
            for counter, data in enumerate(data_lst): 
                time = data[ -6 : ].split(':')              # Время необходимо указывать в формате hh:mm:ss
                date = data[  : -7 ].split('-')            # Дату необходимо указывать в формате dd.mm.yyyy
                date = str(date[2] + '-' + date[1] + '-' + date[0]).split('-')

                #print(f'Date here - {date}, time - {time}')


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
                    #self.ui.data.setText(time_new)

                    if date_err and time_err:
                        message_out = 'введенные дату и время'
                    elif date_err:
                        message_out = 'введенную дату'
                    else:
                        message_out = 'введенное время'

                    print('\nDate or time error')
                    #is_save_switch(self.is_save)

                    self.findChild(QLineEdit, f'data_{counter}').setText(time_new)

                    data_correct = False

                    

                else:
                    data_add = '-'.join(date) + ' ' + ':'.join(time)
                    #print(data_add)
                    search_limits.append(data_add)

            print(f'search_limits builded')


        if data_correct:
            #print(search_limits)

            date_slice_begin = search_limits[0][ : 10].split('-')
            date_time_begin = ''.join(search_limits[0][ -6 : ])
            date_slice_end = search_limits[1][ : 10].split('-')
            date_time_end = ''.join(search_limits[1][ -6 : ])

            #print(f'slices here:\nbegin_slice - {date_slice_begin}\nend_slice - {date_slice_end}')


            year_begin, month_begin, day_begin = int(''.join(date_slice_begin[0])), int(''.join(date_slice_begin[1])), int(''.join(date_slice_begin[2]))
            year_end, month_end, day_end = int(''.join(date_slice_end[0])), int(''.join(date_slice_end[1])), int(''.join(date_slice_end[2]))

            monthes_count_vio = (year_end - year_begin) * 12 + month_end - month_begin + 1
            monthes_stat_vio = []

            #print(f'begin - {year_begin, month_begin, day_begin}\nend - {year_end, month_end, day_end}\nmonthes in  this slice - {monthes_count_vio}')


            os.mkdir('Databases/Violations/') if not os.path.isdir("Databases/Violations/") else print()
            connection = sq.connect('Databases/Violations/violations.db')
            cursor = connection.cursor()

            print('db directory checked')


            for month_num in range(monthes_count_vio):
                #print(month_num, month_num == monthes_count_vio - 1)
                if month_num == 0:
                    date_begin = '-'.join(date_slice_begin)  + '  ' + date_time_begin
                    date_end = date_begin[ : 8 ] + '31' + '  23:59'
                    # ['1111-11-11  00:00', '2000-12-31  23:59']

                    #print(f'date_begin - {date_begin}\ndate_end - {date_end}\n')

                elif month_num == monthes_count_vio - 1:
                    date_begin = '-'.join('-'.join(date_slice_end).split('-')[ : 2]) + '-01'  + '  00:00'
                    date_end = '-'.join(date_slice_end) + '  ' + date_time_end
                    #print(f'date_begin - {date_begin}\ndate_end - {date_end}\nEND\n')

                else:
                    #print(''.join(date_end[ 5 : 7 ]))
                    month_prev = int(''.join(date_end[ 5 : 7 ]))
                    

                    if month_prev + 1 > 12:
                        year_now = str(int(''.join(date_end[ : 4])) + 1)
                        month_now = '01'
                        
                    else:
                        year_now = str(date_end[ : 4])
                        month_now = '0' + str(int(month_prev) + 1) if len(str(int(month_prev) + 1)) < 2 else str(int(month_prev) + 1)

                    date_begin = year_now + '-' + month_now + '-' + '01' + '  00:00'

                    #0000-00-01  00:00

                    date_end = date_begin[ : 8] + '31' + '  23:59'


                    #print(f'year_now - {year_now}, month_prev - {month_prev}, mont_now - {month_now}, date_end - {date_end}')

                cursor.execute('''
                    SELECT count(*) FROM VIOLATIONS WHERE Дата_и_время BETWEEN ? AND ?
                    ''', [date_begin, date_end])

                
                #print(f'violatons in this month - {fetched}, {[date_begin, date_end]}\n')

                monthes_stat_vio.append([date_end[ : 7 ], cursor.fetchall()[0][0]])

            cursor.execute('''
                SELECT count(*) FROM VIOLATIONS WHERE Дата_и_время BETWEEN ? AND ?;
                ''', [search_limits[0], search_limits[1]])

            print('Searching completed')

            viols_in = cursor.fetchall()[0][0]

            monthes_stat_vio.insert(0, viols_in)

            text = f'Всего нарушений за выбранный промежуток - {monthes_stat_vio[0]}\n'

            for i in range(1, len(monthes_stat_vio)):
                month_stat = monthes_stat_vio[i]
                text += f'''{month_stat[0] + '  -  ' + str(month_stat[1])}{'          <===' if month_stat[1] > 0 else ''}\n'''
            
            self.scrollAreaWidgetContents = QLabel(f'Нарушения по месяцам заданной выборки:\n{text}')   # Изменяем текст прокручиваемого окна на найденные страны
            self.area.setWidget(self.scrollAreaWidgetContents)

            connection.close()

            return(monthes_stat_vio)

        else:
            message_out = ' введённ(-ую, -ое, -ые) дату и/или время'
            QMessageBox.critical(self, "Ошибка ", f"Пожалуйста, исправьте {message_out}", QMessageBox.Ok)




def send_commit(sql_req, connect, curs, data_slice, args=[]):
    curs.execute(f''' {sql_req} ''', args)
    connect.commit()



def is_save_switch(is_save_arg):
    is_save_global = True if is_save_arg else False
    print('is_save_global', is_save_global)

app = QApplication([])


screen = app.primaryScreen().availableGeometry()        # Получаем значения доступного для использования пространства монитора 
screen_w=screen.width()                                 # Записываем доступную ширину монитора
screen_h=screen.height()                                # Записываем доступную высоту монитора

screen_w=1080
screen_h=720


'''980 * 736
1080 * 720
1920 * 1080'''




application = Example()
search_win = search_window()

#is_save_global = application.
#print(vars(application))


application.setObjectName('MainWindow')             # Присваиваем экземпляру внутреннее программное имя
application.setWindowTitle('Ввод данных')

application.show()
search_win.show()

sys.exit(app.exec())