# импортируем библиотеку tkinter всю сразу
from tkinter import *
import tkinter as tk
import psycopg2
from tkinter import messagebox
import hashlib

# главное окно приложения
window = Tk()
# заголовок окна
window.title('Авторизация')

w = 450 # ширина окна
h = 230 # высота окна

# получаем высоту и ширину экрана
ws = window.winfo_screenwidth() # width of the screen
hs = window.winfo_screenheight() # height of the screen

# считаем координаты для окна
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# сохраняем измерения экрана и где он размещен
window.geometry('%dx%d+%d+%d' % (w, h, x, y))

# можно ли изменять размер окна - нет
window.resizable(False, False)

# кортежи и словари, содержащие настройки шрифтов и отступов
font_header = ('Arial', 15)
font_entry = ('Arial', 12)
label_font = ('Arial', 11)
base_padding = {'padx': 10, 'pady': 8}
header_padding = {'padx': 10, 'pady': 12}

# обработчик нажатия на клавишу 'Войти'
def clicked( ):
    login = username_entry.get()
    password = password_entry.get()

    db_host = 'localhost';
    db_database = 'korresp';
    db_user = 'postgres';
    db_password = 'root';
    conn = psycopg2.connect(
        host = db_host,
        database = db_database,
        user = db_user,
        password = db_password
    )

    cursor = conn.cursor()


    query = """SELECT * FROM public.users WHERE login = %s AND passwd = %s"""

    # cursor.execute(query, (login, password))
    cursor.execute(query, (login, password))
    result = cursor.fetchone()


    if result is None:
        # status_label.config(text="Invalid login or password")
        messagebox.showinfo('Результат', 'Неверные логин или пароль')
    else:
        # status_label.config(text="Login successful")
        messagebox.showinfo('Результат', 'Вход прошел успешно')
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        login = username_entry.get()
        from home import checked_rezult
    #     вызвать функцию для окна с карточками кнопками с таблицами в зависимости от введонного логина admin, senior_manager, product_manager
    cursor.close()
    conn.close()

# заголовок формы: настроены шрифт (font), отцентрирован (justify), добавлены отступы для заголовка
# для всех остальных виджетов настройки делаются также
main_label = Label(window, text='Авторизация', font=font_header, justify=CENTER, **header_padding)
# помещаем виджет в окно по принципу один виджет под другим
main_label.pack()

# метка для поля ввода имени
username_label = Label(window, text='Имя пользователя', font=label_font , **base_padding)
username_label.pack()

# поле ввода имени
username_entry = Entry(window, bg='#fff', fg='#444', font=font_entry)
username_entry.pack()

# метка для поля ввода пароля
password_label = Label(window, text='Пароль', font=label_font , **base_padding)
password_label.pack()

# поле ввода пароля
password_entry = Entry(window, bg='#fff', fg='#444', font=font_entry)
password_entry.pack()

# кнопка отправки формы
send_btn = Button(window, text='Войти', command=clicked)
send_btn.pack(**base_padding)

status_label = tk.Label(window, text="")
status_label.pack()

# запускаем главный цикл окна
window.mainloop()
