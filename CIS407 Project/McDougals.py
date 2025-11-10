import tkinter as tk
from tkinter.ttk import *
from tkinter import PhotoImage

#main application window
root = tk.Tk()
root.title ("Welcome to McDougals")
root.geometry("300x550")

img = PhotoImage(file='CIS407 Project/Assets/McDonalds arch.png')
image_label = tk.Label(root, image=img)
image_label.pack(
)


loginButton = tk.Button(root, text="Login")
registerButton = tk.Button(root, text="Register")

loginButton.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

registerButton.pack(
    ipadx=5,
    ipady=5
)

root.mainloop()