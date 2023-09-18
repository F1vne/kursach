import tkinter as tk
from tkinter import ttk
from tkinter import *
import psycopg2

# import test
import correspondenceWindow
window = tk.Tk()
window.geometry('400x400')
# from insert import *

connection = psycopg2.connect(
    host="localhost",
    database="korresp",
    user="postgres",
    password="root"
)


# root = tk.Tk()
# root.title("Траснпортная компания")
# root.geometry('400x400')

# button = tk.Button(root, text="Изменить таблицу correspondence", command=select.createWindow)
# button.pack()
# root.mainloop()
# Выборка ID записи из базы данных
cur = connection.cursor()
# cur.execute("SELECT id FROM correspondence where id_sotrudnik = 2")

id_record = cur.fetchone()[0]

# Создание переменной для текста
id_text = tk.StringVar()

# Назначение переменной текстовому полю ввода
e1 = tk.Entry(window, textvariable=id_text)
e1.grid(row=1, column=1)

# Назначение значения переменной
id_text.set(id_record)

# Закрытие подключения к базе данных
cur.close()
connection.close()

# Запуск окна
window.mainloop()