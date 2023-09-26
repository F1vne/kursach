from tkinter import *
import psycopg2
from tkinter import messagebox
import connection
import re
import tkinter as tk
from tkinter import ttk
import windows

class Storage:
	pass

storage = Storage()

# класс для нового окна
class Window(tk.Toplevel):
	def __init__(self, parent):
		super().__init__(parent)

		self.geometry('300x100')
		self.title('Toplevel Window')

		ttk.Button(self, text='Close', command=self.destroy).pack(expand=True)

class App(tk.Tk):
	def __init__(self):
		super().__init__()

		self.storage = Storage()

		self.title('Авторизация')

		w = 450 # ширина окна
		h = 230 # высота окна

		# получаем высоту и ширину экрана
		ws = self.winfo_screenwidth() # width of the screen
		hs = self.winfo_screenheight() # height of the screen

		# считаем координаты для окна
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)

		# сохраняем измерения экрана и где он размещен
		self.geometry('%dx%d+%d+%d' % (w, h, x, y))

		# можно ли изменять размер окна - нет
		self.resizable(False, False)

		# кортежи и словари, содержащие настройки шрифтов и отступов
		font_header = ('Arial', 15)
		font_entry = ('Arial', 12)
		label_font = ('Arial', 11)
		base_padding = {'padx': 10, 'pady': 8}
		header_padding = {'padx': 10, 'pady': 12}

		# обработчик нажатия на клавишу 'Войти'
		main_label = Label(self, text='Авторизация', font=font_header, justify=CENTER, **header_padding).pack(expand=True)
		# метка для поля ввода имени
		username_label = Label(self, text='Имя пользователя', font=label_font , **base_padding).pack(expand=True)
		# поле ввода имени
		self.username_entry = Entry(self, bg='#fff', fg='#444', font=font_entry)
		self.username_entry.pack(expand=True)
		# метка для поля ввода пароля
		password_label = Label(self, text='Пароль', font=label_font , **base_padding).pack(expand=True)
		# поле ввода пароля
		self.password_entry = Entry(self, bg='#fff', fg='#444', font=font_entry, show="*")
		self.password_entry.pack(expand=True)
		# кнопка отправки формы
		send_btn = Button(self, text='Войти', command=self.clicked).pack(**base_padding, expand=True)


	def open_window(self):
		import home
		window = home.Home(self)
		window.grab_set()

	def clicked(self):
		login = self.username_entry.get()
		password = self.password_entry.get()
		self.storage.login = login
		self.storage.password = password
		try:
			conn = psycopg2.connect(
				host=connection.host,
				database=connection.database,
				user=login,
				password=password
			)
			cursor = conn.cursor()
			query = "SELECT * FROM pg_roles WHERE rolname = %s AND rolpassword = %s"

			cursor.execute(query, (login, password))
		except psycopg2.Error as e:
			print('НЕ ЧЕТКО')
			messagebox.showinfo('Результат', 'Неверные логин или пароль')
		else:
			print('ВСЕ ЧЕТКО')
			messagebox.showinfo('Результат', 'Вход прошел успешно')
			self.username_entry.delete(0, 'end')
			self.password_entry.delete(0, 'end')

			window = windows.Home(self, self.storage)
			window.grab_set()
			# вот тут я должен записать user = login; password = password; в файл connec

if __name__ == "__main__":
	app = App()
	app.mainloop()
