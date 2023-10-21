import customtkinter as ctk
import tkinter as tk
import sqlite3

root = ctk.CTk()
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

font1 = ('Times New Roman', 16)
font2 = ('Times New Roman', 12)

root.geometry("500x500")

root.title("Profit Loss Calculator")

testTextBox = ctk.CTkTextbox(root, font=font1)
testTextBox.pack()

button = ctk.CTkButton(root, text="IM A BUTTON CLICK ME!", font = font2)
button.pack(padx=15,pady=15)

root.mainloop()