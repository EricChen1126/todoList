import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('錯誤', '任務欄不能為空')
    else:
        tasks.append(task_string)
        the_cursor.execute('insert into tasks values (?)', (task_string ,))
        list_update()
        task_field.delete(0, 'end')


def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('delete from tasks where title = ?', (the_value,))
    except:
        messagebox.showinfo('錯誤', '請選擇要刪除的事項')

def update_tasks():
    try:
        # 取得被選定的項目
        selected_index = task_listbox.curselection()[0]
        selected_task = tasks[selected_index]
        
        # 取得輸入框中的新任務內容
        task_string = task_field.get()
        
        if len(task_string) == 0:
            messagebox.showinfo('錯誤', '任務欄不能為空')
            return
        
        message_box = messagebox.askyesno('更新', f'您確定要將 "{selected_task}" 更新為 "{task_string}" 嗎？')

        if message_box:
            the_cursor.execute('update tasks set title = ? where title = ?', (task_string, selected_task))
            tasks[selected_index] = task_string
            list_update()
            task_field.delete(0, 'end')

    except IndexError:
        messagebox.showinfo('錯誤', '請選擇要更新的事項')

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    the_connection.commit()
    the_cursor.close()
    gui.destroy()

def retrieve_database():
    while(len(tasks) != 0):
        tasks.pop()

    for row in the_cursor.execute('select title from tasks'):
        tasks.append(row[0])


if __name__ == "__main__":

    # 設定視窗
    gui = tk.Tk()
    gui.title("Side Project : ToDo List")
    gui.geometry("500x450+750+250")
    gui.resizable(0, 0)
    gui.configure(bg = "#FAEBD7")

    # 連接SQLite
    the_connection = sql.connect('todoList.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')

    # 設一個空list，顯示資料庫的值在終端機上。
    tasks = []

    header_frame = tk.Frame(gui, bg = "#FAEBD7")
    functions_frame = tk.Frame(gui, bg = "#FAEBD7")
    listbox_frame = tk.Frame(gui, bg = "#FAEBD7")


    header_frame.pack(fill = "both")
    functions_frame.pack(side = "left", expand = True, fill = "both")
    listbox_frame.pack(side = "right", expand = True, fill = "both")


    header_label = ttk.Label(
        header_frame,
        text = "待 辦 事 項",
        font = ("Consolas", "55", "bold"),
        background = "#FAEBD7",
        foreground = "#8B4513"
    )

    header_label.pack(padx = 30, pady = 30)

    task_label = ttk.Label(
        functions_frame,
        text = "請輸入待辦事項 : ",
        font = ("Consolas", "11", "bold"),
        background = "#FAEBD7",
        foreground = "#000000"
    )

    task_label.place(x = 30, y = 40)

    task_field = ttk.Entry(
        functions_frame,
        font = ("Consolas", "12"),
        width = 18,
        background = "#FFF8DC",
        foreground = "#A52A2A"
    )

    task_field.place(x = 30, y = 80)

    add_button = ttk.Button(
        functions_frame,
        text = "新       增",
        width = 24,
        command = add_task
    )
    update_button = ttk.Button(
        functions_frame,
        text = "更       新",
        width = 24,
        command = update_tasks
    )
    del_button = ttk.Button(
        functions_frame,
        text = "刪       除",
        width = 24,
        command = delete_task
    )
    exit_button = ttk.Button(
        functions_frame,
        text = "退       出",
        width = 24,
        command = close
    )

    add_button.place(x = 30, y = 120)
    update_button.place(x = 30, y = 160)
    del_button.place(x = 30, y = 200)
    exit_button.place(x = 30, y = 240)

    task_listbox = tk.Listbox(
        listbox_frame,
        width = 26,
        height = 13,
        selectmode = 'SINGLE',
        background = "#FFFFFF",
        foreground = "#000000",
        selectbackground = "#CD853F",
        selectforeground = "#FFFFFF"
    )

    task_listbox.place(x = 10, y = 20)

    retrieve_database()
    list_update()
    gui.mainloop()
    the_connection.commit()
    the_cursor.close()
