import customtkinter as ctk
import tkinter as tk
from PIL import ImageTk
from tkinter import filedialog
from settings import *


class ImportImage(ctk.CTkFrame):
    def __init__(self, parent, func):
        self.func = func
        super(ImportImage, self).__init__(master=parent)

        ctk.CTkButton(self, command=self.get_path, text='OPEN IMAGE').place(relx=0.5, rely=0.5, anchor='center')
        self.grid(column=0, row=0, columnspan=2, sticky='news')

    def get_path(self):
        path = filedialog.askopenfile()
        if path:
            self.func(path.name)
        else:
            pass


class MainPage(tk.Canvas):
    def __init__(self, parent, func):
        super(MainPage, self).__init__(master=parent, highlightthickness=0, borderwidth=0, background=dark_gray,
                                       relief='ridge')

        self.parent = parent
        self.resize = func

        self.grid(column=1, row=0, sticky='news', padx=5, pady=5)
        self.bind('<Configure>', self.resize)


class CloseButton(ctk.CTkButton):
    def __init__(self, parent, func):
        super(CloseButton, self).__init__(master=parent)
        ctk.CTkButton(master=parent, corner_radius=0, text='X', command=func, fg_color='red', width=45,
                      height=45).place(relx=0.99, rely=0.01, anchor='ne')
