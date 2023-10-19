import customtkinter as ctk
from tkinter import filedialog
from settings import *


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super(Panel, self).__init__(master=parent, fg_color=dark_gray)
        self.pack(fill='x', pady=4, ipady=8)


class SliderPanel(Panel):
    def __init__(self, parent, title, action, min_, max_):
        super(SliderPanel, self).__init__(parent=parent)

        # grid
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.rowconfigure((0, 1), weight=1, uniform='a')

        # attributes
        self.title = title
        self.action = action
        self.action.trace('w', self.update_text)
        self.min = min_
        self.max = max_
        self.value_label = None

        # widgets
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text=self.title).grid(column=0, row=0, sticky='w', padx=5)
        self.value_label = ctk.CTkLabel(self, text=self.action.get())
        self.value_label.grid(column=1, row=0, sticky='e', padx=5)
        ctk.CTkSlider(self, from_=self.min, to=self.max, fg_color=slider,
                      variable=self.action).grid(
            column=0, row=1, columnspan=2, sticky='ew', padx=5)

    def update_text(self, *args):
        self.value_label.configure(text=round(self.action.get(), 2))


class Segmented(Panel):
    def __init__(self, parent, text, variable, options):
        super(Segmented, self).__init__(parent=parent)
        ctk.CTkLabel(self, text=text).pack()
        ctk.CTkSegmentedButton(self, values=options, variable=variable).pack(expand=True, fill='both', padx=4, pady=4)


class Switch(Panel):
    def __init__(self, parent, *args):
        super(Switch, self).__init__(parent=parent)

        for text, var in args:
            switch = ctk.CTkSwitch(self, text=text, variable=var, button_color=blue, fg_color=slider)
            switch.pack(side='left', fill='x', expand=True, padx=5, pady=5)


class FileName(Panel):
    def __init__(self, parent, filename, filetype):
        super(FileName, self).__init__(parent=parent)
        self.filename = filename
        self.filename.trace('w', self.update_text)
        self.filetype = filetype
        ctk.CTkEntry(self, textvariable=self.filename).pack(fill='x', padx=20, pady=20)
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=20, pady=5, ipady=10)
        ctk.CTkCheckBox(self.frame, text='JPG', command=lambda: self.click('jpg'), onvalue='jpg', offvalue='png',
                        variable=self.filetype).pack(side='left', padx=5)
        ctk.CTkCheckBox(self.frame, text='PNG', command=lambda: self.click('png'), onvalue='png', offvalue='jpg',
                        variable=self.filetype).pack(side='left', padx=5)

        self.output_name = ctk.CTkLabel(self, text=" ")
        self.output_name.pack(fill='x', expand=True)

    def update_text(self, *args):
        if self.filename.get():
            text = self.filename.get().replace(' ', '_') + '.' + self.filetype.get()
            self.output_name.configure(text=text)

    def click(self, value):
        self.filetype.set(value)
        self.update_text()


class FilePath(Panel):
    def __init__(self,parent,filepath):
        super(FilePath, self).__init__(parent=parent)
        self.filepath = filepath

        ctk.CTkButton(self,text='OPEN EXPLORER',command=self.open_path).pack(pady=5)
        ctk.CTkEntry(self,textvariable=self.filepath).pack(fill='x',expand=True,padx=5)

    def open_path(self,*args):
        path = filedialog.askdirectory()
        self.filepath.set(path)


class DropDownPanel(Panel):
    def __init__(self, parent, var, options):
        super(DropDownPanel, self).__init__(parent=parent)

        ctk.CTkOptionMenu(self, values=options, variable=var, dropdown_fg_color='black', dropdown_text_color='white',
                          dropdown_hover_color='#aaaaaa', fg_color=dark_gray).pack(fill='x', expand=True, padx=4,
                                                                                   pady=4)


class Revert(ctk.CTkButton):
    def __init__(self, parent, *args):
        self.values = args
        super(Revert, self).__init__(master=parent, command=self.reset, text='Revert')
        self.place(relx=0.5, rely=0.88, anchor='center')

    def reset(self):
        for prop, value in self.values:
            prop.set(value)


class SaveButton(ctk.CTkButton):
    def __init__(self,parent,func,name,filetype,path):
        super(SaveButton, self).__init__(master=parent,command=self.save,text='Save')
        self.place(relx=0.5, rely=0.88, anchor='center')
        self.name = name
        self.filetype = filetype
        self.export_func = func
        self.path = path

    def save(self):
        self.export_func(self.name.get(),self.filetype.get(),self.path.get())
