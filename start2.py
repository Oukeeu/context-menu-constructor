"""Контекстное меню параметров для выполнения заданных действий
Программисты Прудниченков Г.В., Голова Р.А., Суздальцев В.Р."""
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import sqlite3

connect = sqlite3.connect('main.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS main(group_name TEXT)""")
connect.commit()

def openfile():  # Открытие файла db
    filetypes = (
        ('database files', '*.db'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    f = open(filename)
    f.read()
def OnDoubleClick(event):
    item = tree.identify('item', event.x, event.y)
    print("you clicked on", tree.item(item, "text"))
def name_group(name):
    text, i = name.get(), 0
    connect = sqlite3.connect('main.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO main(group_name) values(?)", (text,))
    connect.commit()
    while True:
        try:
            tree.insert('', tk.END, text=text, iid=i, open=False)
            break
        except:
            i += 1
            continue
    tree.bind("<Double-1>", OnDoubleClick)


def name_input():  # Окно ввода названия группы
    input = Tk()
    input.geometry('440x200')
    input.resizable(0, 0)
    input.title("Название группы")
    name_lbl = Label(input, text='Введите название группы', font="Arial 14")  # Нужно навести красоту со всем окном
    name_lbl.pack(anchor=N, padx=0, pady=40)
    name = Entry(input, width=50)  # нужно строку ввода выше
    name.pack(anchor=CENTER, padx=0, pady=0)
    save_btn = Button(input, text='Сохранить', width=12, height=1, command=lambda: [name_group(name), input.destroy()])
    save_btn.pack(anchor=S, padx=0, pady=17)
    input.mainloop()


root = Tk()  # Основное окно
root.geometry('960x480')
root.resizable(0, 0)
root.title("Конструктор меню параметров")
mainmenu = Menu(root)  # Верхнее меню (файл)
root.config(menu=mainmenu)
filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть", command=openfile)
filemenu.add_command(label="Новый")
filemenu.add_command(label="Сохранить")  # Сделать сохранение (после привязки к xml/sqlite)
mainmenu.add_cascade(label="Файл", menu=filemenu)
btn_group = Button(root, text="Создать группу", width=16, height=2, command=lambda: [name_input()])
btn_group.pack(anchor=W, padx=70, pady=50)  # Навести красоту с кнопкой
tree = ttk.Treeview(root)  # Виджет директории (древа)
tree.heading('#0', text="Your Project")  # Пример
tree.place(x=0, y=150, height=331, width=250)

#Scrollbar
vsb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
vsb.pack(side = tk.RIGHT,fill = tk.Y)
tree.configure(yscrollcommand=vsb.set)


root.mainloop()