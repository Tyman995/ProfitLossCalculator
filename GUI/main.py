import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import db
root = ctk.CTk()
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

font1 = ('Heebo', 16, 'bold')
font2 = ('Heebo', 13, 'bold')
font3 = ('Heebo', 10)

root.geometry("1200x600")
root.title("Profit Loss Calculator")
root.resizable(False,False)

#Menus

my_menu = Menu(root)
root.config(menu=my_menu)


#commands
def a_command():
    pass
def file_new():
    pass
def file_save():
    pass

#create menu items
file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New File", command=file_new)
file_menu.add_command(label="Save File", command=file_save)
file_menu.add_command(label="Exit", command=root.quit)

search_menu = Menu(my_menu)
my_menu.add_command(label="Search", command=a_command)
style=ttk.Style()
#Functions
#This function is used to view the db in the tree view on the application
def add_db_to_tree():
    transactions = db.fetch_transactions()
    money_tree.delete(*money_tree.get_children()) #prevent entering same row multiple times
    for transaction in transactions:
        money_tree.insert('',END, values=transaction)

#This function is used by the add transaction button to add the variable fields into the db
def insert_button():
    t_type = t_type_option_menu_entry.get()
    note = note_entry.get().upper()
    date = date_entry.get()
    amount = amt_entry.get()
    if(note == NONE):
        note = ""
    if not(t_type and date and amount):
        messagebox.showerror('Error','Transaction type, date, and amount must have a value.')
    elif (t_type == "Revenue" and float(amount) < 0):
        messagebox.showerror('Error', 'Revenue cannot have a negative amount')
    elif (t_type == "Expense" and float(amount) > 0):
        messagebox.showerror('Error', 'Expense cannot have a positive amount')
    else:
        db.insert_transaction(t_type, note, date, amount)
        add_db_to_tree()
        messagebox.showinfo('Success','Transaction has been added.')

def update_button():
    select = money_tree.focus()
    if not select:
        messagebox.showerror('Error', 'Select a transaction to update.')
    else:
        t_type = t_type_option_menu_entry.get()
        note = note_entry.get().upper()
        date = date_entry.get()
        amount = amt_entry.get()
        r = money_tree.item(select)['values']
        tid = r[0]
        db.update_transaction(t_type,note,date,amount, tid)
        add_db_to_tree()
        clear_field()
        messagebox.showinfo('Success', 'Transaction has been updated.')

def delete_button():
    select = money_tree.focus()
    if not select:
        messagebox.showerror('Error', 'Select a transaction to delete')
    else:
        r = money_tree.item(select)['values']
        tid = r[0]
        db.delete_transaction(tid)
        add_db_to_tree()
        clear_field()
        messagebox.showinfo('Success', 'Transaction has been deleted.')

#This function will clear the fields currently filled with values
def clear_field(*clicked):
    if clicked:
        money_tree.selection_remove(money_tree.focus())
        money_tree.focus('')
    t_type_option_menu_entry.set(op1)
    note_entry.delete(0,END)
    date_entry.delete(0,END)
    amt_entry.delete(0,END)

#This function grabs the values selected by the focused row in the treeview and places them in the entry fields 
def display_selected(event):
    select = money_tree.focus()
    if select:#clicking on a db row
        r = money_tree.item(select)['values']
        clear_field()
        t_type_option_menu_entry.set(r[1])
        note_entry.insert(0, r[2])
        date_entry.insert(0, r[3])
        amt_entry.insert(0, r[4])
    else:#not clicking on a db row
        pass
  
t_type_label = ctk.CTkLabel(root, font=font1, text='Transaction Type: ')
t_type_label.place(x=20,y=20)

#variables for entry menu
op1 = "Revenue"
op2 = "Expense"
t_type_option_menu_entry = ctk.CTkOptionMenu(root, values=[op1,op2])
t_type_option_menu_entry.place(x=225, y=20)

note_label = ctk.CTkLabel(root, font=font1, text='Name (Optional): ')
note_label.place(x=20,y=120)
note_entry = ctk.CTkEntry(root)
note_entry.place(x=225,y=120)

date_label = ctk.CTkLabel(root, font=font1, text='Transaction Date: ')
date_label.place(x=20,y=220)
date_entry = ctk.CTkEntry(root)
date_entry.place(x=225, y=220)

amount_label = ctk.CTkLabel(root, font=font1, text='Amount: ')
amount_label.place(x=20,y=320)
amt_entry = ctk.CTkEntry(root)
amt_entry.place(x=225, y=320)

#buttons
add_trans_button = ctk.CTkButton(root, command=insert_button, font=font1, text='Add Transaction')
add_trans_button.place(x=20, y=380)
clear_trans_button = ctk.CTkButton(root,command=lambda:clear_field(True), font=font1, text= 'Clear All Fields')
clear_trans_button.place(x=20, y=440)
update_trans_button = ctk.CTkButton(root, command=update_button, font=font1, text='Update Transaction')
update_trans_button.place(x=20, y=500)
delete_trans_button = ctk.CTkButton(root, command=delete_button, font=font1, text='Delete Transaction')
delete_trans_button.place(x=20, y=560)

#Tree View aka the db viewer
style.theme_use("clam")
style.configure("Treeview", font=font2, background="lightgray", foreground="#051650", fieldbackground = "white", rowheight=30)
style.configure("Treeview.Heading", font=font3, background="#1c6cac",foreground="white", relief=FLAT)

style.map('Treeview', background=[('selected','lightblue')], foreground=[('selected','gray')])
money_tree = ttk.Treeview(root, height=12)

#column def
money_tree['columns'] = ('T_id', 'T_Type', 'Note', 'Date', 'Amount')

#format columns
money_tree.column('#0', width=0, stretch=tk.NO) #hide the default phantom column
money_tree.column('T_id', anchor=tk.CENTER, width=60)
money_tree.column('T_Type', anchor=tk.CENTER, width=120)
money_tree.column('Note', anchor=tk.CENTER, width=120)
money_tree.column('Date', anchor=tk.CENTER, width=120)
money_tree.column('Amount', anchor=tk.CENTER, width=200)

#heading of coulumn
money_tree.heading('T_id', text='Tid')
money_tree.heading('T_Type', text='Transaction Type')
money_tree.heading('Note', text='Name')
money_tree.heading('Date', text='Date')
money_tree.heading('Amount', text='Transaction Amount')
money_tree.place(x=480, y=20)
money_tree.bind('<ButtonRelease>', display_selected)

#adds the db values into the tree view
add_db_to_tree()

root.mainloop()