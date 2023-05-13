import tkinter as tk
import psycopg2
from tkinter import ttk

root = tk.Tk()
root.title("БД 3000")
root.geometry('500x500')

# Создаем соединение с базой данных
conn = psycopg2.connect(
    host="127.0.0.1",
    database="test_backup",
    user="root",
    password="root",
    port="5432"
)

# Create cursor
cur = conn.cursor()

# Get all tables in database
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
tables = cur.fetchall()

# Create dropdown list of tables
tk.Label(root, text="Table").grid(row=0, column=0)
table_combobox = ttk.Combobox(root, values=tables)
table_combobox.grid(row=0, column=1)

# Get columns for selected table
def get_columns(*args):
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name=%s", (table_combobox.get(),))
    columns = cur.fetchall()
    for i, column in enumerate(columns):
        tk.Label(root, text=column[0]).grid(row=i+1, column=0)
        entry = tk.Entry(root, width=30)
        entry.insert(0, f"({column[1]})")
        entry.grid(row=i+1, column=1)

table_combobox.bind("<<ComboboxSelected>>", get_columns)

# Create function to insert record into database
def insert_record():
    # Get values from input fields
    values = []
    for child in root.winfo_children():
        if isinstance(child, tk.Entry):
            values.append(child.get())

    # Execute SQL query to insert record
    cur.execute(
        "INSERT INTO {} ({}) VALUES ({})".format(
            table_combobox.get(),
            ", ".join([column[0] for column in cur.description]),
            ", ".join(["%s" for column in cur.description])
        ),
        tuple(values)
    )

    # Commit changes to database
    conn.commit()

    # Show result message
    result_label.config(text="Record inserted successfully!")

# Create button to insert record
insert_button = tk.Button(root, text="Insert record", command=insert_record)
insert_button.grid(row=100, column=0)

# Create label to show result message
result_label = tk.Label(root, text="")
result_label.grid(row=100, column=1)

root.mainloop()

# Close cursor and connection
cur.close()
conn.close()



