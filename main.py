import tkinter as tk
import psycopg2

# Создаем соединение с базой данных
conn = psycopg2.connect(
    host="127.0.0.1",
    database="test_backup",
    user="root",
    password="root"
)

# Создаем курсор для выполнения запросов
cur = conn.cursor()

# Создаем окно tkinter
root = tk.Tk()
root.title("Пример использования tkinter и PostgreSQL")

# Создаем функцию для выполнения запросов к базе данных
def execute_query():
    # Получаем введенный пользователем SQL-запрос
    query = query_text.get("1.0", "end-1c")

    # Выполняем запрос
    cur.execute("SELECT * FROM public.drivers;")

    # Получаем результаты и выводим их в текстовое поле
    rows = cur.fetchall()
    result_text.delete("1.0", "end")
    for row in rows:
        result_text.insert("end", f"{row}")

# Создаем текстовое поле для ввода SQL-запросов
query_text = tk.Text(root)
query_text.pack()

# Создаем кнопку для выполнения запросов
execute_button = tk.Button(root, text="Выполнить", command=execute_query)
execute_button.pack()

# Создаем текстовое поле для вывода результатов
result_text = tk.Text(root)
result_text.pack()

# Запускаем главный цикл tkinter
root.mainloop()

# Закрываем соединение с базой данных
cur.close()
conn.close()
