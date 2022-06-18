from sys  import exit as sysExit

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *   # pip install pyqt5 , библиотека для создания интерфейса
from PyQt5.QtWebEngineWidgets import *      # pip install PyQtWebEngine
from ui6 import Ui_MainWindow

import sqlite3 as sq
import os
import folium
import io
import json



is_save_global = 0
data_all, date_name = '', ''
#out_switch_global = ''

global del_btn
del_btn = []



class upload_window(QMainWindow):
    def __init__(self):
        super(upload_window, self).__init__()
        self.setWindowTitle('upload_window')
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

        self.file,_ = QFileDialog.getOpenFileName(None, "Title", "", "JSON (*.json)")#выбираем файл json
        if self.file:
            self.handle = open(self.file, "r")  # открываем файл json
            self.check_button = True
            self.s += self.handle.read()
            #print(self.s)

class statistic_window(QFrame):
    def __init__(self):
        super(statistic_window, self).__init__()
        self.setWindowTitle('statistic_window')

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

class download_window(QFrame):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('download_window')
        self.setFixedSize(800, 691)
        self.setGeometry(300,300,800, 691)
        #self.excel_data()
        
        font = QFont()
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
        self.update_button.setGeometry(QRect(100, 441, 600, 60))
        self.update_button.clicked.connect(self.db_update)




        self.pushbutton.setFont(font)
        self.lineedit.setGeometry(QRect(100, 230, 600, 40))
        self.pushbutton.setGeometry(QRect(100, 510, 600, 60))
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


        '''self.Win1Btn = QPushButton('>>')
                                self.Win1Btn.clicked.connect(parent.RightArrow)'''
        #self.completer.activated.connect(self.cord)


        
        #self.show()

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

class data_vizualize(QFrame):
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
        #print(self.cordinates)


        #self.box = QVBoxLayout()
        self.box = QGridLayout()


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

        with open('walk.json', 'w') as outfile:
            json.dump(self.json_file, outfile)

        m = folium.Map(location=self.cordinates, zoom_start=17)

        folium.Marker(
            location=self.cordinates,
            popup=self.popup,
            tooltip='Сlick me',
            icon=folium.Icon(color="green")).add_to(m)

        walkData = os.path.join('walk.json')

        folium.GeoJson(walkData, name='walk').add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)

        pp = QWebEngineView()
        pp.setHtml(data.getvalue().decode())

        self.cls_btn = QPushButton('Close', self)
        self.cls_btn.clicked.connect(self.close)


        del_btn = two_args_upd(False, OptionButtons('Map', OptionSettings.map_window_display))

        print(f'In map - {del_btn}')
        global upd_btn
        global is_del

        is_del = del_btn[0]
        upd_btn = del_btn[1]
        
        #upd_btn = OptionButtons('Map', OptionSettings.map_window_display)
        #is_del = False

        

        #print(f'Just here we needed for outer, outer now - {out_switch_global}')

        self.cls_btn.clicked.connect(OptionSettings.update_boxes)                   # ВАЖНАЯ ХУЙНЯ, РАСКОММЕНТИТЬ
        self.cls_btn.clicked.connect(self.close)

        self.box.addWidget(pp, 0, 0, 1, 1)
        self.box.addWidget(self.cls_btn, 0, 10, 1, 1)
        self.setLayout(self.box)

        print('updating boxes')
        #OptionSettings.update_boxes
        print('boxes updated')



        '''
            Внести карту в окно
            Разобраться с добавлением новых кнопок и обновлением их списка

            ЛИБО

            Вручную добавить четвертую кнопку для карты
            Если карта не создана - открывать окошко с соответствующим сообщением, иначе - показываем карту
        '''


class OptionSettings(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        self.btnWin1 = OptionButtons('Upload data', self.upload_window_display)
        self.btnWin2 = OptionButtons('Download data', self.download_window_display)
        self.btnWin3 = OptionButtons('Statistics', self.statistic_window_display)

    # Vertical Box for Buttons *************************************
        self.UpLeft  = QVBoxLayout()
        self.UpLeft.addWidget(self.btnWin1)
        self.UpLeft.addWidget(self.btnWin2)
        self.UpLeft.addWidget(self.btnWin3)

        self.UpLeft.addStretch(1)
  # Display Area on Right
      # Widget Flip Display ******************************************
        self.UpRite   = QHBoxLayout()
        self.Contents = QStackedWidget()
        self.Contents.addWidget(QTextEdit('Nothing Selected'))
        self.Contents.addWidget(upload_window())
        self.Contents.addWidget(download_window())
        self.Contents.addWidget(statistic_window())

        self.Contents.setCurrentIndex(1)
        self.UpRite.addWidget(self.Contents)

  # Button and Display Area on Top
        self.Upper = QHBoxLayout()
        self.Upper.addLayout(self.UpLeft)
        self.Upper.addLayout(self.UpRite)

        self.OuterBox = QVBoxLayout()
        self.OuterBox.addLayout(self.Upper)

        global out_switch_global

        out_switch_global = self

        #print(f'self =  {self, type(self), out_switch_global, type(out_switch_global)}')
        #print(f'out_switch_global now is {out_switch_global}')
        #out_switch(self.OuterBox)
        #self.OuterBox.addLayout(self.Lower)

        self.setLayout(self.OuterBox)
        
        self.setWindowTitle('Агрегатор нарушений')
        #Geometry(Left, Top, Width, Hight)
        self.setGeometry(250, 250, 550, 450)
        self.setModal(True)
        self.exec()

    def upload_window_display(self):
        #print(f'Win 1 self = {self}')
        self.Contents.setCurrentIndex(1)

    def download_window_display(self):
        self.Contents.setCurrentIndex(2)

    def statistic_window_display(self):
        self.Contents.setCurrentIndex(3)

    def map_window_display(self):
        self.Contents.setCurrentIndex(4)

    def update_boxes(self):
        print(self, is_del, upd_btn)
        if is_del:
            pass
        else:
            print(self.UpLeft)
            self.UpLeft.addWiget(upd_btn)
            self.Contents.addWidget(data_vizualize)
            self.UpRite.addWidget(self.Contents)


            print(f'here we are\n')
            
        


class OptionButtons(QToolButton):
    # Class OptionButtons ("Text", Connector) inherits from QToolButton
    def __init__(self, Text, Connector):
        QToolButton.__init__(self)

        self.setText(Text)
        self.setStyleSheet("font: bold;color: blue;height: 55px;width: 55px;")
        self.setIconSize(QSize(32,32))
        self.clicked.connect(Connector)

class CenterPanel(QWidget):
    def __init__(self, MainWin):
        QWidget.__init__(self)

        CntrPane = QTextEdit('Center Panel is Placed Here')

        hbox = QHBoxLayout(self)
        hbox.addWidget(CntrPane)

        self.setLayout(hbox)


def is_save_switch(is_save_arg):
    is_save_global = True if is_save_arg else False
    print('is_save_global', is_save_global)

def line_edit_switch(line_edit_object):
    line_edit_internal = line_edit_object

def two_args_upd(f_arg, t_arg):
    is_del = f_arg
    upd_btn = t_arg

    del_btn = [f_arg, t_arg].copy()

    return(del_btn)

    
if __name__ == '__main__':
    MainApp = QApplication([])

    OptionSettings()

    #MainGui = UI_MainWindow()
    #MainGui.show()

    sysExit(MainApp.exec_())