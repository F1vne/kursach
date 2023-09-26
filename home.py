from tkinter import *
import tkinter as tk
from tkinter import messagebox
import hashlib
import psycopg2
import sys
import windows
from main import Storage


class HomeWindow(tk.Toplevel):
	def __init__(self, parent, storage):
		self.storage = storage

		login = self.storage.login

		print('ПЕРЕДАННЫЙ ЛОГИН:' + self.storage.login)
		super().__init__(parent)
		# заголовок окна
		self.title('Выбор таблицы')

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

		def checked_result(login):
			base_padding = {'padx': 10, 'pady': 8}
			if (login == 'admin'):

				correspondence_btn = Button(self, text='Корреспонденции', command=open_correspondence)
				correspondence_btn.pack(**base_padding, expand=True)

				organization_btn = Button(self, text='Организации', command=open_organization)
				organization_btn.pack(**base_padding, expand=True)

				sotrudniki_btn = Button(self, text='Сотрудники', command=open_sotrudniki)
				sotrudniki_btn.pack(**base_padding, expand=True)

				# users_btn = Button(self, text='Пользователи', command=clicked_users)
				# users_btn.pack(**base_padding, expand=True)

				status_label = tk.Label(self, text="")
				status_label.pack()

			elif (login == 'senior_manager'):
				correspondence_btn = Button(self, text='Корреспонденции', command=open_correspondence)
				correspondence_btn.pack(**base_padding)

				organization_btn = Button(self, text='Организации', command=open_organization)
				organization_btn.pack(**base_padding)

				sotrudniki_btn = Button(self, text='Сотрудники', command=open_sotrudniki)
				sotrudniki_btn.pack(**base_padding)

				status_label = tk.Label(self, text="")
				status_label.pack()

			elif (login == 'product_manager'):
				correspondence_btn = Button(self, text='Корреспонденции', command=open_correspondence)
				correspondence_btn.pack(**base_padding)

				organization_btn = Button(self, text='Организации', command=open_organization)
				organization_btn.pack(**base_padding)

				status_label = tk.Label(self, text="")
				status_label.pack()
			else:
				messagebox.showinfo('Ошибка', 'Неверные логин или пароль')

		def open_correspondence():
			import correspondenceWindow
			window = windows.Correspondence(self.storage)
			window.grab_set()
		def open_organization():
			import organizationWindow
			window = windows.Organization(self.storage)
			window.grab_set()
		def open_sotrudniki():
			import sotrudnikiWindow
			window = windows.Sotrudniki(self.storage)
			window.grab_set()

		checked_result(login)
		close_btn = Button(self, text='Закрыть', command=self.destroy)
		close_btn.pack(**base_padding, expand=True)
