import sys
#import openpyxl
#from openpyxl import *
from PyQt5.QtWidgets import *   # pip install pyqt5 , библиотека для создания интерфейса
import PyQt5.QtWidgets
from PyQt5.QtWebEngineWidgets import *      # pip install PyQtWebEngine
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QIcon
from PyQt5 import QtGui,QtCore, QtWidgets
from ui6 import Ui_MainWindow
#import pandas as pd
import sqlite3 as sq
#import pymysql
#from pymysql import *
#from auth_info import *
import os
import folium
import io
import json
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#from subprocess import run, STDOUT, PIPE
'''import subprocess

cmd = 'pip install -r rq.txt'
output = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
print(f'\n---Libraries checked---')'''


#user_name = 'GSP_main'
#user_data = auth_info[user_name]


matplotlib.use('Qt5Agg')


is_save_global = 0
data_all, date_name = '', ''

icon_file = 'icon.png'



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
        self.ui.pushButton_2.clicked.connect(self.text_data)
        self.ui.pushButton_2.clicked.connect(self.data_uploading)
        

        self.ui.pushButton_3.clicked.connect(self.ui.data.clear)
        self.ui.pushButton_3.clicked.connect(self.ui.object.clear)
        self.ui.pushButton_3.clicked.connect(self.ui.organization.clear)
        self.ui.pushButton_3.clicked.connect(self.ui.fio_insp.clear)
        self.ui.pushButton_3.clicked.connect(self.ui.violation.clear)
        self.ui.pushButton_3.clicked.connect(self.ui.fionar.clear)
        self.ui.pushButton_3.clicked.connect(self.ui.fiopro.clear)
        self.ui.pushButton_3.clicked.connect(self.ui.fiodoc.clear)
        self.ui.pushButton_3.clicked.connect(self.ui.dolgota.clear)
        self.ui.pushButton_3.clicked.connect(self.ui.shirota.clear)

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

        if self.s == '':
            data_correct = False
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, загрузите json-файл с указанными точками маршрута', QMessageBox.Ok)


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
                os.mkdir('Violations/') if not os.path.isdir("Violations/") else print()
                connection = sq.connect('Violations/violations.db')
                
                print('connection established')

            finally:
                pass
            
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
                    Долгота real,
                    Маршрут varchar(2048)
                    )
                    ''')

                connection.commit()

                print('Table checked')


                cursor.execute('''INSERT INTO VIOLATIONS VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                        [self.mas_data[-10],
                        self.mas_data[-9],
                        self.mas_data[-8],
                        self.mas_data[-7],
                        self.mas_data[-6],
                        self.mas_data[-5],
                        self.mas_data[-4],
                        self.mas_data[-3],
                        float(self.mas_data[-2]),
                        float(self.mas_data[-1]),
                        self.s]

                        )

                connection.commit()
                print('Insertion completed\n')
            finally:
                pass

    def jsonsave(self):

        #global path_file
        self.path_file,_ = QFileDialog.getOpenFileName(None, "Title", "", "GEOJSON (*.geojson)")#выбираем файл json
        #self.file,_ = QFileDialog.getOpenFileName(None, "Title", "", "JSON (*.json)")#выбираем файл json
        #self.s = ''
        if self.path_file:
            self.handle = open(self.path_file, "r")  # открываем файл json
            self.check_button = True
            self.s = self.handle.read()
            #print(self.s, '\n')


'''class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)'''

class Canvas(FigureCanvasQTAgg):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        connection = sq.connect('Violations/violations.db')
        cursor = connection.cursor()
        cursor.execute("SELECT substr(Дата_и_время,1,4), COUNT(Дата_и_время) FROM VIOLATIONS GROUP BY substr(Дата_и_время,1,4)")
        data = cursor.fetchall()

        print(data)

        datelist = []
        datecount = []

        for i in range(len(data)):
            print(data[i][0])
            datelist.append(data[i][0])
            datecount.append(data[i][1])
        print(datelist)
        print(datecount)

        fig, ax = plt.subplots()

        years = datelist
        counts = datecount

        ax.bar(years, counts)#, label=bar_labels, color='red')#bar_colors

        ax.set_ylabel('Кол-во нарушений')
        ax.set_xlabel('Год')
        ax.set_title('Кол-во нарушений по годам')

class search_window(QWidget):
    def __init__(self):
        super(search_window, self).__init__()
        self.setFixedSize(1000, 640)
        self.is_save = is_save_global
        #self.search_limits = search_limits
        self.is_correct = False
        self.setStyleSheet('''QWidget {
                            background-color:#22222e;
                            color:white
                            }''')
        self.setupUI()
        #self.area = 

    def setupUI(self):


        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)


        #self.grid_layout = QGridLayout(self)
        self.grid_layout = QVBoxLayout(self)
        self.grid_layout.setObjectName('search_grid_layout')

        #self.area = QScrollArea(self)               # Создание объекта, способного реализовывать прокрутку своего содержимого. При множестве найденных результатов поиска это - лучшее решение
        #self.area.setFont(font)                     # Форматируем объект. В данном случае - только меняем размер шрифта
        #self.area.setWidgetResizable(True)          # Говорим проге, что содержимое можно прокручивать

    

        self.data_begin_input = QLineEdit(self)
        self.data_end_input = QLineEdit(self)

        self.date_begin_hint = QLabel('Дата и время начала выборки', self)
        self.date_end_hint = QLabel('Дата и время конца выборки', self)
        #self.area = QLabel('Здесь будет отображено количество нарушений за указанный период', self)
        self.filter_hint = QLabel('Фильтрация', self)
        self.graph_type = QLabel('Тип графика:', self)
        self.graph_parameter = QLabel('Параметр построения:', self)

        # !! верхний блок

        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.frame.setStyleSheet("background-color:#22222e")
        #self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        #self.frame.setObjectName("frame")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(42, 15, 441, 61))
        self.label.setFont(font)
        self.label.setText('ОБЗОР СТАТИСТИКИ')
        self.label.setStyleSheet("color:white")
        self.label.setStyleSheet("background-color: #22222e")

        #self.graphs_label = QtWidgets.QLabel(self)
        self.graphs_label = Canvas(self)
        self.graphs_label.setGeometry(QtCore.QRect(350, 20, 640, 540))
        self.graphs_label.setFont(font)
        self.label.setObjectName("label")

        font.setPointSize(12)

        self.data_begin_input.setObjectName('data_1')
        self.data_end_input.setObjectName('data_2')

        self.data_begin_input.setPlaceholderText('Время начала выборки (гггг.мм.дд чч:мм)')
        self.data_end_input.setPlaceholderText('Время конца выборки (гггг.мм.дд чч:мм)')

        self.date_begin_hint.setStyleSheet("color:white")
        self.date_end_hint.setStyleSheet("color:white")
        self.date_begin_hint.setFont(font)
        self.date_end_hint.setFont(font)
        #self.area.setFont(font)
        self.filter_hint.setFont(font)
        self.graph_type.setFont(font)
        self.graph_parameter.setFont(font)



        self.search_mode_swaper = QComboBox(self)
        self.search_mode_swaper.setObjectName('search_mode_swaper')
        self.search_mode_swaper.addItem('Объект')
        self.search_mode_swaper.addItem('Не важно')

        self.graph_type_swaper = QComboBox(self)
        self.graph_type_swaper.setObjectName('graph_type_swaper')
        self.graph_type_swaper.addItem('Линейный')
        self.graph_type_swaper.addItem('Столбчатая диаграмма')
        self.graph_type_swaper.addItem('Круговая диаграмма')

        self.graph_parameter_swaper = QComboBox(self)
        self.graph_parameter_swaper.setObjectName('graph_parameter_swaper')
        self.graph_parameter_swaper.addItem('По дате')
        self.graph_parameter_swaper.addItem('По компаниям')
        self.graph_parameter_swaper.addItem('По нарушителям')

        
        #self.search_mode_swaper.addItem('Нарушитель')
        #print(self.search_mode_swaper.currentText())
        #self.search_mode_swaper.currentIndexChanged.connect(lambda ch, name=self.search_mode_swaper.objectName() : self.index_change_reaction(name, self.findChild(QComboBox, name).currentText()))

        #self.data_begin_pod = QLabel(self)
        #self.data_end_pod = QLabel(self)

        #self.data_begin_pod.setText('Введите дату и время начала выборки в формате гггг.мм.дд чч:мм')
        #self.data_end_pod.setText('Введите дату и время конца выборки в формате гггг.мм.дд чч:мм')

        self.data_begin_input.setInputMask('00.00.0000  00:00')
        self.data_end_input.setInputMask('00.00.0000  00:00')

        self.data_begin_input.setFont(font)
        self.data_begin_input.setStyleSheet("color:white")

        self.data_end_input.setFont(font)
        self.data_end_input.setStyleSheet("color:white")

        self.find_button = QPushButton('ПОИСК', self)
        self.find_button.setStyleSheet("QPushButton {\n"
                                  "    color:white;\n"
                                  "    background-color:#fb5b5d;\n"
                                  "    border-radius:15;\n"
                                  "\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed{\n"
                                  "    background-color:#fa4244\n"
                                  "}")

        self.saving_button = QPushButton('СОХРАНИТЬ В ФАЙЛ', self)
        self.saving_button.setStyleSheet("QPushButton {\n"
                                  "    color:white;\n"
                                  "    background-color:#fb5b5d;\n"
                                  "    border-radius:15;\n"
                                  "\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed{\n"
                                  "    background-color:#fa4244\n"
                                  "}")

        self.map_open_button = QPushButton('ПОКАЗАТЬ НА КАРТЕ', self)
        self.map_open_button.setStyleSheet("QPushButton {\n"
                                  "    color:white;\n"
                                  "    background-color:#fb5b5d;\n"
                                  "    border-radius:15;\n"
                                  "\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed{\n"
                                  "    background-color:#fa4244\n"
                                  "}")

        # !! Расположение виджетов

        self.find_button.setFont(font)
        self.find_button.setGeometry(QtCore.QRect(25, 425, 300, 50))
        self.find_button.clicked.connect(self.find_button_action)
        self.find_button.clicked.connect(self.setter)

        self.saving_button.setFont(font)
        self.saving_button.setGeometry(QtCore.QRect(25, 485, 300, 50))
        self.saving_button.clicked.connect(self.saving_button_reaction)
        #self.saving_button.clicked.connect(self.setter)

        self.map_open_button.setFont(font)
        self.map_open_button.setGeometry(QtCore.QRect(25, 545, 300, 50))
        self.map_open_button.clicked.connect(self.find_button_reaction) #self.map_open_button.clicked.connect(self.map_open_button_reaction)
        #self.saving_button.clicked.connect(self.setter)
        
        #self.area.setGeometry(QtCore.QRect(0, 300, 800, 400))
        self.data_begin_input.setGeometry(QtCore.QRect(90, 160, 160, 30))
        self.data_end_input.setGeometry(QtCore.QRect(90, 250, 160, 30))

        self.date_begin_hint.setGeometry(QtCore.QRect(50, 120, 260, 30))
        self.date_end_hint.setGeometry(QtCore.QRect(50, 210, 260, 30))
        self.filter_hint.setGeometry(QtCore.QRect(115, 290, 150, 30))

        self.graph_type.setGeometry(QtCore.QRect(360, 570, 150, 30))
        self.graph_type_swaper.setGeometry(QtCore.QRect(480, 572, 150, 26))

        self.graph_parameter.setGeometry(QtCore.QRect(635, 570, 260, 30))
        self.graph_parameter_swaper.setGeometry(QtCore.QRect(835, 572, 150, 26))

        self.search_mode_swaper.setGeometry(QtCore.QRect(90, 330, 160, 30))


        #self.data_begin_input.setText('01.01.2020 00:00')
        #self.data_end_input.setText('31.12.2023 23:59')


        #self.area.setGeometry(QtCore.QRect(X, Y, width, height))
        '''         |----------> X
                    |
                    |
                    |
                    ...Y '''


       # data_slice = ['1111-11-11  00:00', '1111-12-30  20:59']

        #self.grid_layout.addWidget(self.find_button, 7, 0)
        #self.grid_layout.addWidget(self.data_begin_input, 6, 0)
        
        #self.grid_layout.addWidget(self.area, row, column, row_span, column_span)

        #self.grid_layout.addWidget(self.data_end_input, 5, 0)
        #self.grid_layout.addWidget(self.area, 0, 0, 2, 1)

        #self.grid_layout.addWidget(self.area, 3, 1, 2, 1)
        #self.grid_layout.addWidget(self.area, 3, 1, 2, 1)

        #self.grid_layout.addWidget(self.area)
        
        #self.grid_layout.addWidget(self.data_begin_input)
        #self.grid_layout.addWidget(self.area, row, column, row_span, column_span)

        #self.grid_layout.addWidget(self.data_end_input)
        #self.grid_layout.addWidget(self.find_button)
        

    def index_change_reaction(self, object_name, object_text):
        print(f'{object_name} : {object_text}')

    '''
        Тест функции кнопки поиска. Строку №418:

        self.find_button.clicked.connect(self.find_button_reaction)

        Переделал в:
        self.find_button.clicked.connect(self.find_button_reaction)

    '''

    def find_button_action(self):
        print('Обработка кнопки поиска')

    def saving_button_reaction(self):
        print('Обработка кнопки сохранения')

    def map_open_button_reaction(self):
        print('Обработчик кнопки карты')

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

                    #self.findChild(QLineEdit, f'data_{counter}').setText(time_new)

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

            #print(search_limits)

            #print(f'slices here:\nbegin_slice - {date_slice_begin}\nend_slice - {date_slice_end}')


            year_begin, month_begin, day_begin = int(''.join(date_slice_begin[0])), int(''.join(date_slice_begin[1])), int(''.join(date_slice_begin[2]))
            year_end, month_end, day_end = int(''.join(date_slice_end[0])), int(''.join(date_slice_end[1])), int(''.join(date_slice_end[2]))

            monthes_count_vio = (year_end - year_begin) * 12 + month_end - month_begin + 1
            monthes_stat_vio = []

            #print(f'begin - {year_begin, month_begin, day_begin}\nend - {year_end, month_end, day_end}\nmonthes in  this slice - {monthes_count_vio}')


            os.mkdir('Violations/') if not os.path.isdir("Violations/") else print()
            connection = sq.connect('Violations/violations.db')
            cursor = connection.cursor()

            print('db directory checked')

            

            
            self.viols_all = []

            cursor.execute(''' 
                SELECT * FROM VIOLATIONS WHERE Дата_и_время BETWEEN ? AND ? ORDER BY Дата_и_время
                ''', [search_limits[0], search_limits[1]])
            
            self.data_add = ['Дата и время: ', 'Объект: ', 'Организация инспектора: ', 'ФИО инспектора: ', 'Нарушение: ', 'ФИО Нарушителя: ', 'ФИО проверяющего: ', 'ФИО докладчика: ', 'Широта: ', 'Долгота: ', 'Маршрут: ']


            for data in cursor.fetchall():
                self.add_prep = []

                for element_counter, data_element in enumerate(data):
                    self.add_prep.append(self.data_add[element_counter] + str(data_element))
                
                self.viols_all.append(self.add_prep)


            #print(self.viols_all, len(self.viols_all))

            #print(self.viols_all if len(self.viols_all) != 0 else 'Нарушений не обнаружено')

            if len(self.viols_all) > 0:
                self.sort_mode = False
                self.data_dict = {}
                self.viol_counter = 0
                self.search_mode = self.search_mode_swaper.currentText()

                self.map = folium.Map(zoom_start=17)

                if self.search_mode_swaper.currentText() == 'Объект':

                    print(f'\nObject sorting pushed\n')

                    for counter, violation_one in enumerate(self.viols_all):
                        #print(violation_one,'\n')
                        if violation_one[1][ 8 : ] not in self.data_dict:
                            #print(f'\n---Added new object {violation_one[1][ 8 : ]}---')
                            self.data_dict.update( { violation_one[1][ 8 : ] : [[f'id: {self.viol_counter}'] + violation_one] } )
                            
                        else:
                            #print(f'mid res - {self.violations_object_tuple[violence_one[1][ 8 : ]] + violation_one}\n')
                            self.data_dict.update( { violation_one[1][ 8 : ] : self.data_dict[violation_one[1][ 8 : ]] + [[f'id: {self.viol_counter}'] + violation_one] } )
                            #print(f'\nObject-based tupled violations - {self.data_dict}\n')
                        self.viol_counter += 1
                    self.sort_mode = 'Объект'
                    
                    #print(self.data_dict)
                

                

                if self.sort_mode:
                    self.marker_colors = [
                                    'red',
                                    'blue',
                                    'gray',
                                    'darkred',
                                    'lightred',
                                    'orange',
                                    'beige',
                                    'green',
                                    'darkgreen',
                                    'lightgreen',
                                    'darkblue',
                                    'lightblue',
                                    'purple',
                                    'darkpurple',
                                    'pink',
                                    'cadetblue',
                                    'lightgray',
                                    'black'
                                ]
                    #    {name : [[ ], [ ]], name_2 : [[ ], [ ]]}
                    
                    
                    self.markers = {}

                    #print(self.data_dict)
                    for color_counter, key in enumerate(self.data_dict):
                        #print(f'\ndict key is {key}\n')

                        self.marker_color = self.marker_colors[color_counter - color_counter // len(self.marker_colors) * len(self.marker_colors)]

                        for violation in self.data_dict[key]:
                            #print(violation[0], violation[1], violation[2])
                            

                            self.json_file=eval(violation[-1][ 9 : ])

                            self.html = f"""
                                <ul>
                                    <li>{violation[1]}</li>
                                    <li>{violation[2]}</li>
                                    <li>{violation[3]}</li>
                                    <li>{violation[4]}</li>
                                    <li>{violation[5]}</li>
                                    <li>{violation[6]}</li>
                                    <li>{violation[7]}</li>
                                    <li>{violation[8]}</li>
                                    -----------------------
                                </ul>
                                """
                            #print(self.html, '\n\n')

                            with open('founded_path.geojson', 'w') as outfile:
                                json.dump(self.json_file, outfile)


                            # СДЕЛАТЬ БУФЕРНЫЙ СЛОВАРЬ ДЛЯ ИЗБЕЖАНИЯ НАЛОЖЕНИЯ МАРШРУТОВ ДРУГ НА ДРУГА


                            self.marker_cords = f'{violation[ 9 ][ 8 : ]}, {violation[ 10 ][ 9 : ]}'

                            if self.marker_cords not in self.markers:
                                self.markers.update({ self.marker_cords : [self.html, self.marker_color, key] })
                                #print(f'added new note - {self.marker_cords, [self.html, self.marker_color, key]}')
                                
                            else:
                                #self.markers.update({ self.marker_cords : self.markers[self.marker_cords] + [self.html, self.marker_color] })

                                self.markers.update({ self.marker_cords : [self.markers[self.marker_cords][0] + '\n\n' + self.html, self.markers[self.marker_cords][1], key]})
                                #print('dict updated and now it is -', self.marker_cords, [self.markers[self.marker_cords][0] + '\n\n' + self.html, self.markers[self.marker_cords][1], key])

                            walkData = os.path.join('founded_path.geojson')

                            folium.GeoJson(walkData).add_to(self.map)


                    
                

                    for mark_key in self.markers:
                        #print(f'Key now = {mark_key}, {self.markers[mark_key][2]}\n\n')
                        #print(self.markers[mark_key], '\n')

                        self.html_input = f'''<h3>{self.search_mode} - {self.markers[mark_key][2]}</h3>\n\n{self.markers[mark_key][0]}'''
                        self.iframe = folium.IFrame(html= self.html_input, width=300, height=300)
                        self.popup = folium.Popup(self.iframe, max_width=2650)
                        folium.Marker(
                                        location = mark_key.split(', '), 
                                        icon=folium.Icon(color = self.markers[mark_key][1]), 
                                        popup=self.popup
                                    ).add_to(self.map)


                        
                        #for mark_data in self.markers[marker_key]:
                        #print(self.markers[mark_key], '\n')
                    #print(self.markers)


                    print('Markers placed') 

                    
  

                    data = ''
                    data = io.BytesIO()
                    self.map.save(data, close_file=False)

                    self.persons_map_window = persons_map_viz(data)

                    #self.persons_map_window.show()

                    # Объединять информацию в маркерах, если координаты двух или более маркеров совпадают, помечая, что к чему относится
                    # Доделать визуализацию для случаев, когда не выбраны варианты сортировки


                    #self.show()

                    #self.map.show()


                else:
                    self.markers = {}

                    for data in self.viols_all:
                        self.marker_cords = f'''{data[8].split(': ')[1]}, {data[9].split(': ')[1]}'''
                        #print(data, '\n\n', self.marker_cords, '\n')
                        
                        self.html = f"""
                                <ul>
                                    <li>{data[0]}</li>
                                    <li>{data[1]}</li>
                                    <li>{data[2]}</li>
                                    <li>{data[3]}</li>
                                    <li>{data[4]}</li>
                                    <li>{data[5]}</li>
                                    <li>{data[6]}</li>
                                    <li>{data[7]}</li>
                                    -----------------------
                                </ul>
                                """

                        if self.marker_cords not in self.markers:
                            self.markers.update({ self.marker_cords : [self.html, data[-1]]})
                        else:
                            json_pathes = self.markers[self.marker_cords][1]
                            if data[-1] not in json_pathes:
                                json_pathes.append(data[-1])

                            self.markers.update({ self.marker_cords : [self.markers[self.marker_cords][0] + '\n\n' + self.html, json_pathes] })


                    self.marker_colors = [
                                    'red',
                                    'blue',
                                    'gray',
                                    'darkred',
                                    'lightred',
                                    'orange',
                                    'beige',
                                    'green',
                                    'darkgreen',
                                    'lightgreen',
                                    'darkblue',
                                    'lightblue',
                                    'purple',
                                    'darkpurple',
                                    'pink',
                                    'cadetblue',
                                    'lightgray',
                                    'black'
                                ]
                    

                    for color_counter, marker_key in enumerate(self.markers):
                        self.marker_color = self.marker_colors[color_counter - color_counter // len(self.marker_colors) * len(self.marker_colors)]

                        self.iframe = folium.IFrame(html = self.markers[marker_key][0], width=300, height=300)
                        self.popup = folium.Popup(self.iframe, max_width=2650)
                        #print('\nmarker_data - ',(self.markers[marker_key][-1].split(': ')[1] ))
                        #print(f'all data - {self.markers[marker_key]}\n\n-------')
                        for marker_data in self.markers[marker_key]:

                            #print('marker data -', self.markers[marker_key][-1][9 :] )

                            path = eval(self.markers[marker_key][-1][9 :] )
                            with open('founded_path.geojson', 'w') as outfile:
                                json.dump(path, outfile)
                                #print('file dumped\n')

                            walkData = os.path.join('founded_path.geojson')
                            #print(f'WalkData - {walkData}, {outfile}, path - {path}\n')

                            folium.GeoJson(walkData).add_to(self.map)

        

                        

                        


                        folium.Marker(
                                        location = marker_key.split(', '), 
                                        icon=folium.Icon(color = self.marker_color), 
                                        popup=self.popup
                                    ).add_to(self.map)
                            
                        
                    data = io.BytesIO()
                    self.map.save(data, close_file=False)

                    self.buffer_window = persons_map_viz(data)



            cursor.execute('''
                SELECT count(*) FROM VIOLATIONS WHERE Дата_и_время BETWEEN ? AND ?;
                ''', [search_limits[0], search_limits[1]])

                                                    # self.violations_object_tuple - Нарушения, отсортированные по объектам
            viols_in = cursor.fetchall()[0][0]      # Количество нарушений за указанный промежуток времени

            print('Searching completed')

            monthes_stat_vio.insert(0, viols_in)

            text = f'Всего нарушений за выбранный промежуток - {monthes_stat_vio[0]}\n'

            #self.area.setText(text)

            for i in range(1, len(monthes_stat_vio)):
                month_stat = monthes_stat_vio[i]
                text += f'''{month_stat[0] + '  -  ' + str(month_stat[1])}{'          <===' if month_stat[1] > 0 else ''}\n'''
            
            #self.scrollAreaWidgetContents = QLabel(f'Нарушения по месяцам заданной выборки:\n{text}')   # Изменяем текст прокручиваемого окна на найденные страны
            #self.area.setWidget(self.scrollAreaWidgetContents)

            connection.close()

            return(monthes_stat_vio)

        else:
            message_out = ' введённ(-ую, -ое, -ые) дату и/или время'
            QMessageBox.critical(self, "Ошибка ", f"Пожалуйста, исправьте {message_out}", QMessageBox.Ok)

    def setter(self):
        self.comp_arg = self.search_mode_swaper.currentText()


class persons_map_viz(QWidget):
    def __init__(self, data):
        super(persons_map_viz, self).__init__()
        self.setWindowTitle('Статистическая карта')

        self.box = QVBoxLayout()
        pp = QWebEngineView()
        pp.setHtml(data.getvalue().decode())
        self.box.addWidget(pp)
        self.setLayout(self.box)

        self.show()

        # Объединять информацию в маркерах, если координаты двух или более маркеров совпадают, помечая, что к чему относится
        # Доделать визуализацию для случаев, когда не выбраны варианты сортировки




class data_viz_input(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 691)
        self.setGeometry(300,300,800, 691)
        #self.excel_data()
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.setStyleSheet("background-color:#22222e")
        self.lineedit=QLineEdit(self)
        self.lineedit.setPlaceholderText('Введите дату или имя нарушителя')
        self.lineedit.setFont(font)
        self.lineedit.setStyleSheet("color:white")

        self.pushbutton = QPushButton('ОЧИСТИТЬ',self)
        self.pushbutton.setStyleSheet("QPushButton {\n"
                                  "    color:white;\n"
                                  "    background-color:#fb5b5d;\n"
                                  "    border-radius:30;\n"
                                  "\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed{\n"
                                  "    background-color:#fa4244\n"
                                  "}")

        self.update_button = QPushButton('ОБНОВИТЬ', self)
        self.update_button.setStyleSheet("QPushButton {\n"
                                  "    color:white;\n"
                                  "    background-color:#fb5b5d;\n"
                                  "    border-radius:30;\n"
                                  "\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed{\n"
                                  "    background-color:#fa4244\n"
                                  "}")
        self.update_button.setFont(font)
        self.update_button.setGeometry(QtCore.QRect(100, 441, 600, 60))

        self.update_button.clicked.connect(self.db_update)




        self.pushbutton.setFont(font)
        self.lineedit.setGeometry(QtCore.QRect(100, 230, 600, 40))
        self.pushbutton.setGeometry(QtCore.QRect(100, 510, 600, 60))
        #self.completer = QCompleter(self.spisok)  # подсказки

        self.bd_data()


        self.completer = QCompleter(self.date_name)  # подсказки

       # ''' SELECT * FROM VIOLATIONS WHERE Дата_и_время = ? and ФИО_нарушителя = ?''', [. , .]
       # '''SELECT Дата_и_время, ФИО_нарушителя FROM VIOLATIONS'''

        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(0)  # реакция метода на нажатие одной из подсказок
        self.lineedit.setCompleter(self.completer)
        self.lineedit.completer()
        self.pushbutton.clicked.connect(self.lineedit.clear)
        self.completer.activated.connect(self.show_window_2)

        #self.completer.activated.connect(self.cord)


        
        self.show()

    def bd_data(self):
        
        os.mkdir('Violations/') if not os.path.isdir("Violations/") else print()
        connection = sq.connect('Violations/violations.db')

        print('Connection established')
        
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
                    Долгота real,
                    Маршрут varchar(2048)
                    )
                    ''')

        connection.commit()

        print('Table checked')

        cursor.execute('''SELECT Дата_и_время, ФИО_нарушителя FROM VIOLATIONS''')
        self.date_name_prepare = cursor.fetchall()
        self.date_name = []

        for entry in self.date_name_prepare:
            self.date_name.append(f'{entry[0]}, {entry[1]}')

        connection.close()
        #line_edit_switch(self.lineedit)


        #print(f'date_name = {self.date_name}, date_all = {self.date_all}')

    def db_update(self):
        self.bd_data()
        print(self.date_name)
        self.completer = QCompleter(self.date_name)  # подсказки
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(0)  # реакция метода на нажатие одной из подсказок
        self.completer.activated.connect(self.show_window_2)
        self.lineedit.setCompleter(self.completer)
        self.lineedit.completer()

    def show_window_2(self):
        self.w2 = data_vizualize(self.lineedit)
        self.w2.show()

class data_vizualize(QWidget):
    def __init__(self, line_edit_internal):
        super(data_vizualize, self).__init__()
        self.lineedit = line_edit_internal
        self.setObjectName('MapOut')
        self.setWindowTitle('Карта происшествий')

        os.mkdir('Violations/') if not os.path.isdir("Violations/") else print()
        connection = sq.connect('Violations/violations.db')

        print('Connection established')
        
        cursor = connection.cursor()
        
        cursor.execute('''SELECT * FROM VIOLATIONS WHERE Дата_и_время = ? and ФИО_нарушителя = ?''', [self.lineedit.text()[ : 17 ], self.lineedit.text()[ 19 : ]])

        self.date_all_prep = cursor.fetchall()[0]
        self.date_all = []
        self.cordinates = []
        self.json_downloaded = ''

        for counter, element in enumerate(self.date_all_prep):
            if counter < len(self.date_all_prep) - 3:
                self.date_all.append(element)

            elif counter < len(self.date_all_prep) - 1:
                self.cordinates.append(element)

            else:
                self.json_downloaded = element

        #print(self.json_downloaded)
        print(self.cordinates)


        self.box = QVBoxLayout()


        self.json_file=eval(self.json_downloaded)    #преобразует строку в json

        self.html = f"""
                                <h1> Данные</h1>
                                <ul>
                                    <li>Дата и время:   {self.date_all[0]}</li>
                                    <li>Объект:         {self.date_all[1]}</li>
                                    <li>Организация инспектора: {self.date_all[2]}</li>
                                    <li>ФИО инспектора: {self.date_all[3]}</li>
                                    <li>Нарушение:      {self.date_all[4]}</li>
                                    <li>ФИО Нарушителя: {self.date_all[5]}</li>
                                    <li>ФИО проверяющего: {self.date_all[6]}</li>
                                    <li>ФИО докладчика: {self.date_all[7]}</li>                                </ul>
                                </p>
                                """
        self.iframe = folium.IFrame(html=self.html, width=300, height=300)
        self.popup = folium.Popup(self.iframe, max_width=2650)

        with open('founded_path.geojson', 'w') as outfile:
            json.dump(self.json_file, outfile)

        m = folium.Map(location=self.cordinates, zoom_start=17)
        folium.Marker(
            location=self.cordinates,
            popup=self.popup,
            tooltip='Информация',
            icon=folium.Icon(color="green")).add_to(m)

        walkData = os.path.join('founded_path.geojson')

        folium.GeoJson(walkData).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)

        pp = QWebEngineView()
        pp.setHtml(data.getvalue().decode())
        self.box.addWidget(pp)
        self.setLayout(self.box)


def send_commit(sql_req, connect, curs, data_slice, args=[]):
    curs.execute(f''' {sql_req} ''', args)
    connect.commit()

def is_save_switch(is_save_arg):
    is_save_global = True if is_save_arg else False
    print('is_save_global', is_save_global)

def line_edit_switch(line_edit_object):
    line_edit_internal = line_edit_object

app = QApplication([])

application = Example()
search_win = search_window()
data_input = data_viz_input()

app.setWindowIcon(QtGui.QIcon('ico.ico'))


#icon = QtGui.QIcon()
#icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)


application.setObjectName('MainWindow')             # Присваиваем экземпляру внутреннее программное имя
application.setWindowTitle('Ввод данных')
#application.setWindowIcon(icon)

search_win.setObjectName('SearchWindow')             # Присваиваем экземпляру внутреннее программное имя
search_win.setWindowTitle('Обзор статистики')
#search_win.setWindowIcon(icon)

data_input.setObjectName('DataWindow')             # Присваиваем экземпляру внутреннее программное имя
data_input.setWindowTitle('Поиск данных')
#data_input.setWindowIcon(icon)



application.show()
search_win.show()
data_input.show()

sys.exit(app.exec())