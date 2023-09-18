# подключаем графическую библиотеку для создания интерфейсов
from tkinter import *
from tkinter import messagebox
from  tkinter import ttk
from tkinter.messagebox import showinfo

import psycopg2

def run():
    # создаём класс для работы с базой данных
    class DB:
        # конструктор класса
        def __init__(self):
            # соединяемся с файлом базы данных
            # self.conn = sqlite3.connect("mybooks.db")
            self.conn = psycopg2.connect(
                host="localhost",
                database="korresp",
                user="postgres",
                password="root"
            )

            # создаём курсор для виртуального управления базой данных
            self.cur = self.conn.cursor()

            # если нужной нам таблицы в базе нет — создаём её
            # self.cur.execute("CREATE TABLE IF NOT EXISTS buy (id INTEGER PRIMARY KEY, product TEXT, price TEXT, comment TEXT)")

            # сохраняем сделанные изменения в базе
            self.conn.commit()

            # деструктор класса

        def __del__(self):
            # отключаемся от базы при завершении работы
            self.conn.close()

            # просмотр всех записей

        def view(self):
            # выбираем все записи
            query = """SELECT * FROM sotrudniki"""
            self.cur.execute(query)
            # собираем все найденные записи в колонку со строками
            rows = self.cur.fetchall()
            # print(rows)

            # [(3, 'Уведомление', datetime.date(2022, 1, 17), datetime.date(2022, 1, 20), 2),(1, 'Договор', datetime.date(2022, 1, 15), datetime.date(2022, 1, 25), 1)]
            # возвращаем сроки с записями расходов
            return rows

        # добавляем новую запись
        def insert(self, name, id_sotrudnik):
            try:
                # формируем запрос с добавлением новой записи в БД
                query = """INSERT INTO organization VALUES (%s,%s)"""
                self.cur.execute(query, (name, id_sotrudnik))
                # сохраняем изменения
                self.conn.commit()
                # выводим результат
                count = self.cur.rowcount
                rezult = "Обновлено строк: " + str(count)
                showinfo("Результат операции", rezult)
            except (Exception, psycopg2.Error) as error:
                showinfo("Результат операции", error)
                self.conn.rollback()

        # обновляем информацию о покупке
        def update(self, name, id_sotrudnik):
            try:
                # формируем запрос на обновление записи в БД
                # sql = "UPDATE correspondence SET document_type='?', execution_date='?', receipt_date='?', id_sotrudnik='?' WHERE id=?"
                # data = document_type, execution_date, receipt_date, id_sotrudnik, id
                # self.cur.execute(sql, data)

                query = """UPDATE organization SET name=%s WHERE id_sotrudnik=%s"""
                self.cur.execute(query, (name, id_sotrudnik))
                # сохраняем изменения
                self.conn.commit()
                # выводим результат
                count = self.cur.rowcount
                rezult = "Обновлено строк: " + str(count)
                showinfo("Результат операции", rezult)
            except (Exception, psycopg2.Error) as error:
                showinfo("Результат операции", error)
                self.conn.rollback()

        # удаляем запись
        def delete(self, id_sotrudnik):
            try:
                # формируем запрос на удаление выделенной записи по внутреннему порядковому номеру
                query = """DELETE FROM sotrudniki WHERE id_sotrudnik=%s"""
                # id_korresp = str(id_korresp)
                self.cur.execute(query, (str(id_sotrudnik)))
                # сохраняем изменения
                self.conn.commit()
                # выводим результат
                count = self.cur.rowcount
                rezult = "Обновлено строк: " + str(count)
                showinfo("Результат операции", rezult)
            except (Exception, psycopg2.Error) as error:
                showinfo("Результат операции", error)
                self.conn.rollback()

        # ищем запись по одному заполненному полю
        # нужно в зависимости от количества ввежденных значений формировать запрос
        # с соответствующим числов пунктов в where
        # def search(self, execution_date, receipt_date, id_korresp, document_type, id_sotrudnik):

        def search(self, name=None, id_sotrudnik=None):

            name = e2.get()
            id_sotrudnik = e1.get()


            if name:
                query = """SELECT * FROM sotrudniki WHERE name=%s"""
                self.cur.execute(query, (name,))
                rows = self.cur.fetchall()
                return rows

            if id_sotrudnik:
                query = """SELECT * FROM sotrudniki WHERE id_sotrudnik=%s"""
                self.cur.execute(query, (id_sotrudnik,))
                rows = self.cur.fetchall()
                return rows

        #     # формируем полученные строки и возвращаем их как ответ
    # создаём новый экземпляр базы данных на основе класса
    db = DB()

    # заполняем поля ввода значениями выделенной позиции в общем списке
    def get_selected_row(event):
        # будем обращаться к глобальной переменной
        global selected_tuple
        # получаем позицию выделенной записи в списке
        index = list1.curselection()[0]
        # получаем значение выделенной записи
        selected_tuple = list1.get(index)
        # удаляем старые данные
        e1.delete(0, END)
        e1.insert(END, selected_tuple[0])
        # делаем то же самое с другими полями
        e2.delete(0, END)
        e2.insert(END, selected_tuple[1])


    # обработчик нажатия на кнопку «Посмотреть всё»
    def view_command():
        # очищаем список в приложении
        list1.delete(0, END)
        # проходим все записи в БД
        for row in db.view():
            # и сразу добавляем их на экран
            list1.insert(END, row)


    # обработчик нажатия на кнопку «Поиск»
    def search_command():
        # очищаем список в приложении
        list1.delete(0, END)

        id_sotrudnik = id_sotrudnik_text.get()
        name = name_text.get()

        if id_sotrudnik:
            for row in db.search(id_sotrudnik,):
                list1.insert(END, row)
        if name:
            for row in db.search(name,):
                list1.insert(END, row)

    # обработчик нажатия на кнопку «Добавить»
    def add_command():
        # добавляем запись в БД
        db.insert(id_sotrudnik_text.get(),name_text.get())
        # обновляем общий список в приложении
        view_command()


    # обработчик нажатия на кнопку «Удалить»
    def delete_command():
        # удаляем запись из базы данных по индексу выделенного элемента
        db.delete(selected_tuple[0])
        # обновляем общий список расходов в приложении
        view_command()


    # обработчик нажатия на кнопку «Обновить»
    def update_command():
        # обновляем данные в БД о выделенной записи
        db.update(id_sotrudnik_text.get(),name_text.get())
        # обновляем общий список расходов в приложении
        view_command()

    def clear_entry():
        e1.delete(0, 'end')
        e2.delete(0, 'end')

    def clear_list():
        list1.delete(0, END)


    # подключаем графическую библиотеку
    window = Tk()
    # заголовок окна
    window.title("Сотрудники")

    w = 700 # width for the Tk root
    h = 650 # height for the Tk root

    # get screen width and height
    ws = window.winfo_screenwidth() # width of the screen
    hs = window.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen
    # and where it is placed
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # обрабатываем закрытие окна
    def on_closing():
        # показываем диалоговое окно с кнопкой
        if messagebox.askokcancel("", "Закрыть программу?"):
            # удаляем окно и освобождаем память
            window.destroy()


    # сообщаем системе о том, что делать, когда окно закрывается
    window.protocol("WM_DELETE_WINDOW", on_closing)

    # создаём надписи для полей ввода и размещаем их по сетке
    l1 = Label(window, text="id Сотрудника")
    l1.grid(row=0, column=0)

    l2 = Label(window, text="ФИО Сотрудники")
    l2.grid(row=1, column=0)


    # создаём поле ввода названия покупки, говорим, что это будут строковые переменные и размещаем их тоже по сетке
    #id, document_type, execution_date, receipt_date, id_sotrudnik
    id_sotrudnik_text = StringVar()
    e1 = Entry(window, textvariable=id_sotrudnik_text)
    e1.grid(row=0, column=1)

    name_text = StringVar()
    e2 = Entry(window, textvariable=name_text, width=30)
    e2.grid(row=1, column=1)

    # создаём список, где появятся наши записи из бд
    list1 = Listbox(window, height=25, width=65)
    list1.grid(row=3, column=0, rowspan=6, columnspan=2, pady=(30, 0))


    # на всякий случай добавим сбоку ск`ролл, чтобы можно было быстро прокручивать длинные списки
    sb1 = Scrollbar(window)
    sb1.grid(row=2, column=2, rowspan=6)

    # привязываем скролл к списку
    list1.configure(yscrollcommand=sb1.set)
    sb1.configure(command=list1.yview)

    # привязываем выбор любого элемента списка к запуску функции выбора
    list1.bind('<<ListboxSelect>>', get_selected_row)

    # создаём кнопки действий и привязываем их к своим функциям
    # кнопки размещаем тоже по сетке
    b1 = Button(window, text="Посмотреть все", width=20, command=view_command)
    b1.grid(row=3, column=3, pady=(0, 0))  # size of the button

    b2 = Button(window, text="Отчистить поля", width=20, command=clear_entry)
    b2.grid(row=4, column=3, pady=(0, 0))  # size of the button

    b3 = Button(window, text="Отчистить список", width=20, command=clear_list)
    b3.grid(row=5, column=3, pady=(0, 0))

    b3 = Button(window, text="Поиск по одному полю", width=20, command=search_command)
    b3.grid(row=6, column=3, pady=(0, 0))

    b4 = Button(window, text="Добавить", width=20, command=add_command)
    b4.grid(row=7, column=3, pady=(0, 0))

    b5 = Button(window, text="Обновить", width=20, command=update_command)
    b5.grid(row=8, column=3, pady=(0, 0))

    b6 = Button(window, text="Удалить по номеру ID", width=20, command=delete_command)
    b6.grid(row=9, column=3, pady=(0, 20))

    b7 = Button(window, text="Закрыть", width=20, command=on_closing)
    b7.grid(row=10, column=3, pady=(0, 0))

    # обновляем общий список расходов
    view_command()

    # пусть окно работает всё время до закрытия
    window.mainloop()
run()