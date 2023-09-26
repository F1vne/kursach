from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showinfo
import psycopg2
import connection
import tkinter as tk
import hashlib
import sys

class CorrespondenceWindow(tk.Toplevel):
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
				query = """SELECT * FROM correspondence order by id_korresp ASC"""
				self.cur.execute(query)
				# собираем все найденные записи в колонку со строками
				rows = self.cur.fetchall()
				# возвращаем строки с записями расходов
				return rows

			# добавляем новую запись
			def insert(self, id_korresp, document_type, execution_date, receipt_date, id_sotrudnik, id_org):
				try:
					# формируем запрос с добавлением новой записи в БД
					query = """INSERT INTO correspondence VALUES (%s,%s,%s,%s,%s,%s)"""
					self.cur.execute(query, (id_korresp, document_type, execution_date, receipt_date, id_sotrudnik, id_org))
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
			def update(self, document_type, execution_date, receipt_date, id_sotrudnik, id_org, id_korresp):
				try:
					query = """UPDATE correspondence SET document_type=%s, execution_date=%s, receipt_date=%s, id_sotrudnik=%s, id_org=%s WHERE id_korresp=%s"""
					self.cur.execute(query, (document_type, execution_date, receipt_date, id_sotrudnik, id_org, id_korresp))
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
			def delete(self, id_korresp):
				try:
					# формируем запрос на удаление выделенной записи по внутреннему порядковому номеру
					query = """DELETE FROM correspondence WHERE id_korresp=%s"""
					# id_korresp = str(id_korresp)
					self.cur.execute(query, (str(id_korresp)))
					# сохраняем изменения
					self.conn.commit()
					# выводим результат
					count = self.cur.rowcount
					rezult = "Обновлено строк: " + str(count)
					showinfo("Результат операции", rezult)
				except (Exception, psycopg2.Error) as error:
					showinfo("Результат операции", error)
					self.conn.rollback()

			# ищем запист по одному полю
			def search(self, id_korresp=None, document_type=None, execution_date=None, receipt_date=None, id_sotrudnik=None, id_org=None):
				id_korresp = entry1.get();
				document_type = entry2.get();
				execution_date = entry3.get();
				receipt_date = entry4.get();
				id_sotrudnik = entry5.get();
				id_org = entry6.get();

				if id_korresp:
					query = """SELECT * FROM correspondence WHERE id_korresp=%s"""
					self.cur.execute(query, (id_korresp,))
					rows = self.cur.fetchall()
					if rows is None:
						list1.delete(0, END)
					return rows

				elif document_type:
					query = """SELECT * FROM correspondence WHERE document_type=%s"""
					self.cur.execute(query, (document_type,))
					rows = self.cur.fetchall()
					if rows is None:
						list1.delete(0, END)
					return rows

				elif execution_date:
					query = """SELECT * FROM correspondence WHERE execution_date=%s"""
					self.cur.execute(query, (execution_date,))
					rows = self.cur.fetchall()
					if rows is None:
						list1.delete(0, END)
					return rows

				elif receipt_date:
					query = """SELECT * FROM correspondence WHERE receipt_date=%s"""
					self.cur.execute(query, (receipt_date,))
					rows = self.cur.fetchall()
					if rows is None:
						list1.delete(0, END)
					return rows

				elif id_sotrudnik:
					query = """SELECT * FROM correspondence WHERE id_sotrudnik=%s"""
					self.cur.execute(query, (id_sotrudnik,))
					rows = self.cur.fetchall()
					if rows is None:
						list1.delete(0, END)
					return rows

				elif id_org:
					query = """SELECT * FROM correspondence WHERE id_org=%s"""
					self.cur.execute(query, (id_org,))
					rows = self.cur.fetchall()
					if rows is None:
						list1.delete(0, END)
					return rows

		# создаём новый экземпляр базы данных на основе класса
		db = DB(self.storage.login, self.storage.password)
		self.title("Корреспонденции")

		w = 700  # width for the Tk root
		h = 650  # height for the Tk root

		# get screen width and height
		ws = self.winfo_screenwidth()  # width of the screen
		hs = self.winfo_screenheight()  # height of the screen

		# calculate x and y coordinates for the Tk root self
		x = (ws / 2) - (w / 2)
		y = (hs / 2) - (h / 2)

		self.geometry('%dx%d+%d+%d' % (w, h, x, y))

		# создаём надписи для полей ввода и размещаем их по сетке
		label1 = Label(self, text="id записи")
		label1.grid(row=0, column=0)

		label2 = Label(self, text="тип документа")
		label2.grid(row=1, column=0)

		label3 = Label(self, text="дата поступления")
		label3.grid(row=2, column=0)

		label4 = Label(self, text="дата отправки")
		label4.grid(row=0, column=2)

		label5 = Label(self, text="id сотрудника")
		label5.grid(row=1, column=2)

		label6 = Label(self, text="id организации")
		label6.grid(row=2, column=2)

		# создаём поля ввода, говорим, что это будут строковые переменные и размещаем их тоже по сетке
		id_text = StringVar()
		entry1 = Entry(self, textvariable=id_text)
		entry1.grid(row=0, column=1)

		document_type_text = StringVar()
		entry2 = Entry(self, textvariable=document_type_text)
		entry2.grid(row=1, column=1)

		execution_date_text = StringVar()
		entry3 = Entry(self, textvariable=execution_date_text)
		entry3.grid(row=2, column=1)

		receipt_date_text = StringVar()
		entry4 = Entry(self, textvariable=receipt_date_text)
		entry4.grid(row=0, column=3)

		id_sotrudnik_text = StringVar()
		entry5 = Entry(self, textvariable=id_sotrudnik_text)
		entry5.grid(row=1, column=3)

		id_org_text = StringVar()
		entry6 = Entry(self, textvariable=id_org_text)
		entry6.grid(row=2, column=3)

		# создаём список, где появятся наши записи из бд
		list1 = Listbox(self, height=25, width=65)
		list1.grid(row=3, column=0, rowspan=6, columnspan=2, pady=(30, 0))

		# на всякий случай добавим сбоку ск`ролл, чтобы можно было быстро прокручивать длинные списки
		sb1 = Scrollbar(self)
		sb1.grid(row=2, column=2, rowspan=6)

		# привязываем скролл к списку
		list1.configure(yscrollcommand=sb1.set)
		sb1.configure(command=list1.yview)
		# view_command()

		# заполняем поля ввода значениями выделенной позиции в общем списке
		def get_selected_row(event):
			# будем обращаться к глобальной переменной
			global selected_tuple
			if list1.curselection():
				# получаем позицию выделенной записи в списке
				index = list1.curselection()[0]
			else:
				# print(list1.curselection())
				# print('ПЕРЕМЕННАЯ ПУСТАЯ')
				index = 0
			selected_tuple = list1.get(index)
			# получаем значение выделенной записи
			# удаляем старые данные
			entry1.delete(0, END)
			entry1.insert(END, selected_tuple[0])
			# делаем то же самое с другими полями
			entry2.delete(0, END)
			entry2.insert(END, selected_tuple[1])
			entry3.delete(0, END)
			entry3.insert(END, selected_tuple[2])
			entry4.delete(0, END)
			entry4.insert(END, selected_tuple[3])
			entry5.delete(0, END)
			entry5.insert(END, selected_tuple[4])
			entry6.delete(0, END)
			entry6.insert(END, selected_tuple[5])

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

			id = id_text.get()
			document_type = document_type_text.get()
			execution_date = execution_date_text.get()
			receipt_date = receipt_date_text.get()
			id_sotrudnik = id_sotrudnik_text.get()
			id_org = id_org_text.get()

			if id:
				for row in db.search(id, ):
					list1.insert(END, row)
			elif document_type:
				for row in db.search(document_type, ):
					list1.insert(END, row)
			elif execution_date:
				for row in db.search(execution_date, ):
					list1.insert(END, row)
			elif receipt_date:
				for row in db.search(receipt_date, ):
					list1.insert(END, row)
			elif id_sotrudnik:
				for row in db.search(id_sotrudnik, ):
					list1.insert(END, row)
			elif id_org:
				for row in db.search(id_org, ):
					list1.insert(END, row)

		# обработчик нажатия на кнопку «Добавить»
		def add_command():
			# добавляем запись в БД
			db.insert(id_text.get(), document_type_text.get(), execution_date_text.get(), receipt_date_text.get(), id_sotrudnik_text.get(), id_org_text.get())
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
			db.update(document_type_text.get(), execution_date_text.get(), receipt_date_text.get(), id_sotrudnik_text.get(), id_org_text.get(), id_text.get())
			# обновляем общий список в приложении
			view_command()

		def clear_entry():
			entry1.delete(0, 'end')
			entry2.delete(0, 'end')
			entry3.delete(0, 'end')
			entry4.delete(0, 'end')
			entry5.delete(0, 'end')
			entry6.delete(0, 'end')

		def clear_list():
			list1.delete(0, END)

		# обрабатываем закрытие окна
		def on_closing():
			# показываем диалоговое окно с кнопкой
			if messagebox.askokcancel("", "Закрыть программу?"):
				# удаляем окно и освобождаем память
				self.destroy()

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

		button3 = Button(self, text="Поиск", width=20, command=search_command)
		button3.grid(row=6, column=3, pady=(0, 0))

		button4 = Button(self, text="Добавить", width=20, command=add_command)
		button4.grid(row=7, column=3, pady=(0, 0))

		button5 = Button(self, text="Обновить", width=20, command=update_command)
		button5.grid(row=8, column=3, pady=(0, 0))

		button6 = Button(self, text="Удалить по номеру ID", width=20, command=delete_command)
		button6.grid(row=9, column=3, pady=(0, 20))

		button7 = Button(self, text="Закрыть", width=20, command=self.destroy)
		button7.grid(row=10, column=3, pady=(0, 0))

