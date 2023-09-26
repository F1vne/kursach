from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showinfo
import psycopg2
import connection
import tkinter as tk
import hashlib
import sys

class OrganizationWindow(tk.Toplevel):
	def __init__(self, storage):
		self.storage = storage
		super().__init__()
		# создаём класс для работы с базой данных
		class DB:
			# конструктор класса
			def __init__(self, login, password):
				# соединяемся с файлом базы данных
				self.conn = psycopg2.connect(
					host=connection.host,
					database=connection.database,
					user = login,
					password = password
				)

				# создаём курсор для виртуального управления базой данных
				self.cur = self.conn.cursor()

				# сохраняем сделанные изменения в базе
				self.conn.commit()

				# деструктор класса

			def __del__(self):
				# отключаемся от базы при завершении работы
				self.conn.close()

				# просмотр всех записей

			def view(self):
				# выбираем все записи
				query = """SELECT * FROM organization order by id_org ASC"""
				self.cur.execute(query)
				# собираем все найденные записи в колонку со строками
				rows = self.cur.fetchall()
				return rows

			# добавляем новую запись
			def insert(self, name, ownership, id_org):
				try:
					# формируем запрос с добавлением новой записи в БД
					query = """INSERT INTO organization VALUES (%s,%s,%s)"""
					self.cur.execute(query, (name, ownership, id_org))
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
			def update(self, name, ownership, id_org):
				try:
					query = """UPDATE organization SET name=%s, ownership=%s WHERE id_org=%s"""
					self.cur.execute(query, (name, ownership, id_org))
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
			def delete(self, id_org):
				try:
					# формируем запрос на удаление выделенной записи по внутреннему порядковому номеру
					query = """DELETE FROM organization WHERE id_org=%s"""
					# id_korresp = str(id_korresp)
					self.cur.execute(query, (str(id_org)))
					# сохраняем изменения
					self.conn.commit()
					# выводим результат
					count = self.cur.rowcount
					rezult = "Обновлено строк: " + str(count)
					showinfo("Результат операции", rezult)
				except (Exception, psycopg2.Error) as error:
					showinfo("Результат операции", error)
					self.conn.rollback()

			def search(self, name=None, ownership=None, id_org=None):
				name = entry1.get()
				ownership = entry2.get()
				id_org = entry3.get()

				if name:
					query = """SELECT * FROM organization	 WHERE name=%s"""
					self.cur.execute(query, (name,))
					rows = self.cur.fetchall()
					if rows is None:
						list1.delete(0, END)
					return rows

				elif ownership:
					query = """SELECT * FROM organization	 WHERE ownership=%s"""
					self.cur.execute(query, (ownership,))
					rows = self.cur.fetchall()
					if rows is None:
						list1.delete(0, END)
					return rows

				elif id_org:
					query = """SELECT * FROM organization	 WHERE id_org=%s"""
					self.cur.execute(query, (id_org,))
					rows = self.cur.fetchall()
					if rows is None:
						list1.delete(0, END)
					return rows
		# создаём новый экземпляр базы данных на основе класса
		db = DB(self.storage.login, self.storage.password)

		# заголовок окна
		self.title("Организации")

		w = 700 # width for the Tk root
		h = 650 # height for the Tk root

		# get screen width and height
		ws = self.winfo_screenwidth() # width of the screen
		hs = self.winfo_screenheight() # height of the screen

		# calculate x and y coordinates for the Tk root self
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)

		self.geometry('%dx%d+%d+%d' % (w, h, x, y))

		# создаём надписи для полей ввода и размещаем их по сетке
		label1 = Label(self, text="Наименование оранизации")
		label1.grid(row=0, column=0)

		label2 = Label(self, text="Тип оранизации")
		label2.grid(row=1, column=0)

		label3 = Label(self, text="id организации")
		label3.grid(row=2, column=0)

		id_org_text = StringVar()
		entry1 = Entry(self, textvariable=id_org_text)
		entry1.grid(row=0, column=1)

		name_text = StringVar()
		entry2 = Entry(self, textvariable=name_text)
		entry2.grid(row=1, column=1)

		ownership_text = StringVar()
		entry3 = Entry(self, textvariable=ownership_text)
		entry3.grid(row=2, column=1)

		# создаём список, где появятся наши записи из бд
		list1 = Listbox(self, height=25, width=65)
		list1.grid(row=3, column=0, rowspan=6, columnspan=2, pady=(30, 0))

		# на всякий случай добавим сбоку ск`ролл, чтобы можно было быстро прокручивать длинные списки
		sb1 = Scrollbar(self)
		sb1.grid(row=2, column=2, rowspan=6)

		# привязываем скролл к списку
		list1.configure(yscrollcommand=sb1.set)
		sb1.configure(command=list1.yview)

		# заполняем поля ввода значениями выделенной позиции в общем списке
		def get_selected_row(event):
			# будем обращаться к глобальной переменной
			global selected_tuple
			# получаем позицию выделенной записи в списке
			index = list1.curselection()[0]
			# получаем значение выделенной записи
			selected_tuple = list1.get(index)
			# удаляем старые данные
			entry1.delete(0, END)
			entry1.insert(END, selected_tuple[0])
			# делаем то же самое с другими полями
			entry2.delete(0, END)
			entry2.insert(END, selected_tuple[1])
			entry3.delete(0, END)
			entry3.insert(END, selected_tuple[2])

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

			id = id_org_text.get()
			name = name_text.get()
			ownership = ownership_text.get()

			if id:
				for row in db.search(id,):
					list1.insert(END, row)
			if name:
				for row in db.search(name,):
					list1.insert(END, row)
			if ownership:
				for row in db.search(ownership,):
					list1.insert(END, row)

		# обработчик нажатия на кнопку «Добавить»
		def add_command():
			# добавляем запись в БД
			db.insert(id_org_text.get(),name_text.get(), ownership_text.get())
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
			db.update(id_org_text.get(),name_text.get(), ownership_text.get())
			# обновляем общий список расходов в приложении
			view_command()

		def clear_entry():
			entry1.delete(0, 'end')
			entry2.delete(0, 'end')
			entry3.delete(0, 'end')

		def clear_list():
			list1.delete(0, END)

		# обрабатываем закрытие окна

		# привязываем выбор любого элемента списка к запуску функции выбора
		list1.bind('<<ListboxSelect>>', get_selected_row)

		# создаём кнопки действий и привязываем их к своим функциям
		# кнопки размещаем тоже по сетке
		button1 = Button(self, text="Посмотреть все", width=20, command=view_command)
		button1.grid(row=3, column=3, pady=(0, 0))  # size of the button

		button2 = Button(self, text="Отчистить поля", width=20, command=clear_entry)
		button2.grid(row=4, column=3, pady=(0, 0))  # size of the button

		button3 = Button(self, text="Отчистить список", width=20, command=clear_list)
		button3.grid(row=5, column=3, pady=(0, 0))

		button3 = Button(self, text="Поиск по одному полю", width=20, command=search_command)
		button3.grid(row=6, column=3, pady=(0, 0))

		button4 = Button(self, text="Добавить", width=20, command=add_command)
		button4.grid(row=7, column=3, pady=(0, 0))

		button5 = Button(self, text="Обновить", width=20, command=update_command)
		button5.grid(row=8, column=3, pady=(0, 0))

		button6 = Button(self, text="Удалить по номеру ID", width=20, command=delete_command)
		button6.grid(row=9, column=3, pady=(0, 20))

		button7 = Button(self, text="Закрыть", width=20, command=self.destroy)
		button7.grid(row=10, column=3, pady=(0, 0))
