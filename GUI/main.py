import customtkinter as ctk
import tkinter as tk
import sqlite3

root = ctk.CTk()
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

font1 = ('Times New Roman', 16)

root.geometry("800x800")

root.title("Profit Loss Calculator")

testTextBox = ctk.CTkTextbox(root, font=font1)
testTextBox.pack()

button = ctk.CTkButton(root, text="IM A BUTTON CLICK ME!", font = ('Times New Roman', 12))
button.pack(padx=15,pady=15)

root.mainloop()