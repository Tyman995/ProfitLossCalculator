import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
import sqlite3
import db
import pandas as pd
import re

root = ctk.CTk()
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

font1 = ('Heebo', 16, 'bold')
font2 = ('Heebo', 13, 'bold')
font3 = ('Heebo', 10)
font4 = ('Heebo', 18, 'bold')
font5 = ('Heebo', 18)


root.geometry("1200x600")
root.title("Profit Loss Calculator")
root.resizable(False,False)
try:
    root.iconbitmap(r"../NetProfitLossCalculator/ProfitLossCalculator/GUI/jbns.ico")
except:
    pass
#Menus

my_menu = Menu(root)
root.config(menu=my_menu)


#commands
#def file_new():
#    pass

def file_save():
    db.save_as_csv()
    messagebox.showinfo('Success', 'Output CSV file created')

def search_db():
    lookup_transaction = search_entry.get().upper()
    #close search
    search.destroy()
    #clear treeview
    for transaction in money_tree.get_children():
        money_tree.delete(transaction)
        
    transactions = db.search_query(lookup_transaction)
    for transaction in transactions:
        money_tree.insert('',END, values=transaction)
    remove_labels()
    search_results_display(lookup_transaction)

def lookup_transactions():
    global search_entry, search
    search = Toplevel(root)
    search.title("Lookup Transactions")
    search.geometry("400x200")
    
    #label frame
    search_frame = LabelFrame(search, text="Search")
    search_frame.pack(padx=10, pady=10)

    #entry box
    search_entry = Entry(search_frame, font=font5)
    search_entry.pack(padx=20, pady=20)

    #add button
    search_button = Button(search, text="Search", command=search_db)
    search_button.pack(padx=20, pady=20)

def reset_tree():
    add_db_to_tree()
    remove_labels()
    clear_field()
    results_display()
    
#create menu items
file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
#file_menu.add_command(label="New File", command=file_new)
file_menu.add_command(label="Save File", command=file_save)
file_menu.add_command(label="Exit", command=root.quit)

search_menu = Menu(my_menu, tearoff=0)
my_menu.add_command(label="Search", command=lookup_transactions)
style=ttk.Style()

reset_menu = Menu(my_menu, tearoff=0)
my_menu.add_command(label="Reset", command=reset_tree)

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
    check = check_entry.get()
    note = note_entry.get().upper()
    date = date_entry.get()
    amount = amt_entry.get()
    if(note == NONE):
        note = ""
    if not(t_type and date and amount and check):
        messagebox.showerror('Error','Transaction type, check #, date, and amount must have a value.')
    elif (t_type == "Revenue" and float(amount) < 0):
        messagebox.showerror('Error', 'Revenue cannot have a negative amount')
    elif (t_type == "Expense" and float(amount) > 0):
        messagebox.showerror('Error', 'Expense cannot have a positive amount')
    else:
        db.insert_transaction(t_type, check, note, date, amount)
        add_db_to_tree()
        remove_labels()
        results_display()
        messagebox.showinfo('Success','Transaction has been added.')

def update_button():
    select = money_tree.focus()
    if not select:
        messagebox.showerror('Error', 'Select a transaction to update.')
    else:
        t_type = t_type_option_menu_entry.get()
        check = check_entry.get()
        note = note_entry.get().upper()
        date = date_entry.get()
        amount = amt_entry.get()
        r = money_tree.item(select)['values']
        tid = r[0]
        if(note == NONE):
            note = ""
        if not(t_type and date and amount and check):
            messagebox.showerror('Error','Transaction type, check #, date, and amount must have a value.')
        if (t_type == "Revenue" and float(amount) < 0):
            messagebox.showerror('Error', 'Revenue cannot have a negative amount')
        elif (t_type == "Expense" and float(amount) > 0):
            messagebox.showerror('Error', 'Expense cannot have a positive amount')
        else:
            db.update_transaction(t_type,check,note,date,amount,tid)
            add_db_to_tree()
            clear_field()
            remove_labels()
            results_display()
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
        remove_labels()
        results_display()
        messagebox.showinfo('Success', 'Transaction has been deleted.')

#This function will clear the fields currently filled with values
def clear_field(*clicked):
    if clicked:
        money_tree.selection_remove(money_tree.focus())
        money_tree.focus('')
    t_type_option_menu_entry.set(op1)
    check_entry.delete(0,END)
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
        check_entry.insert(0, r[2])
        note_entry.insert(0, r[3])
        date_entry.insert(0, r[4])
        amt_entry.insert(0, r[5])
    else:#not clicking on a db row
        pass

#Total Rev/Expense/NetProfitLoss
def results_display():
    global total_expense_result, total_revenue_result, total_expense_label, total_revenue_label, net_loss_label, net_loss_result, net_profit_label, net_profit_result
    try:
        total_expense = round(db.calc_total_expense()[0], 2)
    except:
        total_expense = 0
    try:
        total_revenue = round(db.calc_total_revenue()[0], 2)
    except:
        total_revenue = 0
    total_expense_label = ctk.CTkLabel(root, font=font4, text='Total Expenses: ')
    total_expense_label.place(x=480,y=420)
    total_expense_result = ctk.CTkLabel(root, font=font4, text_color='red', text=f"{total_expense}")
    total_expense_result.place(x=970,y=420)
    total_revenue_label = ctk.CTkLabel(root, font=font4, text='Total Revenue: ')
    total_revenue_label.place(x=480,y=480)
    total_revenue_result = ctk.CTkLabel(root, font=font4, text_color='green', text=f"+{total_revenue}")
    total_revenue_result.place(x=970,y=480)
    #net profit/loss calculation
    try:
        net = round(db.calc_total()[0], 2)
    except:
        net = 0
    if(net >= 0.0):
        net_profit_label = ctk.CTkLabel(root, font=font4, text="Net Profit: ")
        net_profit_label.place(x=480,y=540)
        net_profit_result = ctk.CTkLabel(root, font=font4, text_color='green', text=f"+{(net)}")
        net_profit_result.place(x=970,y=540)
    else:
        net_loss_label = ctk.CTkLabel(root, font=font4, text="Net Loss: ")
        net_loss_label.place(x=480,y=540)
        net_loss_result = ctk.CTkLabel(root, font=font4, text_color='red', text=f"{(net)}")
        net_loss_result.place(x=970,y=540)

#Total Rev/Expense/NetProfitLoss for a searched value
def search_results_display(lookup_transaction):
    global total_expense_result, total_revenue_result, total_expense_label, total_revenue_label, net_loss_label, net_loss_result, net_profit_label, net_profit_result
    try:
        total_expense = round(db.search_calc_total_expense(lookup_transaction)[0], 2)
    except:
        total_expense = 0
    try:
        total_revenue = round(db.search_calc_total_revenue(lookup_transaction)[0], 2)
    except:
        total_revenue = 0
    total_expense_result = ctk.CTkLabel(root, font=font4, text_color='red', text=f"{total_expense}")
    total_expense_result.place(x=970,y=420)
    total_revenue_result = ctk.CTkLabel(root, font=font4, text_color='green', text=f"+{total_revenue}")
    total_revenue_result.place(x=970,y=480)
    #net profit/loss calculation
    try:
        net = round(db.search_calc_total(lookup_transaction)[0], 2)
    except:
        net = 0
    if(net >= 0.0):
        net_profit_label = ctk.CTkLabel(root, font=font4, text="Net Profit: ")
        net_profit_label.place(x=480,y=540)
        net_profit_result = ctk.CTkLabel(root, font=font4, text_color='green', text=f"+{(net)}")
        net_profit_result.place(x=970,y=540)
    else:
        net_loss_label = ctk.CTkLabel(root, font=font4, text="Net Loss: ")
        net_loss_label.place(x=480,y=540)
        net_loss_result = ctk.CTkLabel(root, font=font4, text_color='red', text=f"{(net)}")
        net_loss_result.place(x=970,y=540)
    
    #calendar functions
def pick_date(event):
    global cal, d_w
    d_w = Toplevel(background='#282424')
    d_w.grab_set()
    d_w.title("Select date")
    d_w.geometry("250x220+590+370")
    cal = Calendar(d_w, selectmode="day", year= 2023, month=1, day=1, date_pattern="mm-dd-y", background='#1c6cac')
    cal.place(x=0, y=0)
    cal_button = ctk.CTkButton(d_w, text="Submit", command=get_date)
    cal_button.place(x=55, y=189)

def get_date():
    date_entry.delete(0, END)
    date_entry.insert(0, cal.get_date())
    d_w.destroy()

t_type_label = ctk.CTkLabel(root, font=font1, text='Transaction Type: ')
t_type_label.place(x=20,y=20)

def remove_labels():
        try:
            total_expense_result.destroy()
        except:
            pass
        try:
            total_revenue_result.destroy()
        except:
            pass
        try:
            net_profit_label.destroy()
        except:
            pass
        try:
            net_profit_result.destroy()
        except:
            pass
        try:
            net_loss_label.destroy()
        except:
            pass
        try:
            net_loss_result.destroy()
        except:
            pass
#variables for entry menu
op1 = "Revenue"
op2 = "Expense"
t_type_option_menu_entry = ctk.CTkOptionMenu(root, values=[op1,op2])
t_type_option_menu_entry.place(x=225, y=20)

note_label = ctk.CTkLabel(root, font=font1, text='Name (Optional): ')
note_label.place(x=20,y=95)
note_entry = ctk.CTkEntry(root)
note_entry.place(x=225,y=95)

check_label = ctk.CTkLabel(root, font=font1, text='Check Number: ')
check_label.place(x=20, y=170)
check_entry = ctk.CTkEntry(root)
check_entry.place(x=225, y=170)

date_label = ctk.CTkLabel(root, font=font1, text='Transaction Date: ')
date_label.place(x=20,y=245)
date_entry = ctk.CTkEntry(root, placeholder_text="mm-dd-yyyy")
date_entry.place(x=225, y=245)
date_entry.bind("<1>", pick_date)

amount_label = ctk.CTkLabel(root, font=font1, text='Amount: ')
amount_label.place(x=20,y=320)
amt_entry = ctk.CTkEntry(root)
amt_entry.place(x=225, y=320)

#buttons
add_trans_button = ctk.CTkButton(root, command=insert_button, font=font1, text='Add Transaction', corner_radius=25, height=50)
add_trans_button.place(x=20, y=400)
clear_trans_button = ctk.CTkButton(root,command=lambda:clear_field(True), font=font1, text= 'Clear All Fields   ', corner_radius=25, height=50)
clear_trans_button.place(x=20, y=490)
update_trans_button = ctk.CTkButton(root, command=update_button, font=font1, text='Update Transaction', corner_radius=25, height=50)
update_trans_button.place(x=222, y=400)
delete_trans_button = ctk.CTkButton(root, command=delete_button, font=font1, text='Delete Transaction ', corner_radius=25, height=50)
delete_trans_button.place(x=222, y=490)

#Tree View aka the db viewer
style.theme_use("clam")
style.configure("Treeview", font=font2, background="lightgray", foreground="#051650", fieldbackground = "white", rowheight=30)
style.configure("Treeview.Heading", font=font3, background="#1c6cac",foreground="white", relief=FLAT)
style.configure("Treeview.")
style.map('Treeview', background=[('selected','lightblue')], foreground=[('selected','gray')])
#Tree View Frame
tree_frame = Frame(root)
tree_frame.place(x=480, y=20)

#Scrollbar
scrollbar = Scrollbar(tree_frame)
scrollbar.pack(side=RIGHT, fill=Y)

#Tree View Creation
money_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, height=12)

#config Scrollbar
scrollbar.config(command=money_tree.yview)

#column def
money_tree['columns'] = ('T_id', 'T_Type', 'Check #', 'Note', 'Date', 'Amount')

#format columns
money_tree.column('#0', width=0, stretch=tk.NO) #hide the default phantom column
money_tree.column('T_id', anchor=tk.CENTER, width=60)
money_tree.column('T_Type', anchor=tk.CENTER, width=120)
money_tree.column('Check #', anchor=tk.CENTER, width=100)
money_tree.column('Note', anchor=tk.CENTER, width=100)
money_tree.column('Date', anchor=tk.CENTER, width=100)
money_tree.column('Amount', anchor=tk.CENTER, width=180)

#heading of coulumn
money_tree.heading('T_id', text='Tid')
money_tree.heading('T_Type', text='Transaction Type')
money_tree.heading('Check #', text='Check #')
money_tree.heading('Note', text='Name')
money_tree.heading('Date', text='Date')
money_tree.heading('Amount', text='Transaction Amount')
money_tree.pack()
money_tree.bind('<ButtonRelease>', display_selected)

#adds the db values into the tree view
add_db_to_tree()
results_display()
root.mainloop()