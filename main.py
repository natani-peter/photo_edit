import customtkinter as ctk
from tkinter import messagebox
from MainMenu import ImportImage, MainPage, CloseButton
from SideMenu import SidePage
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from settings import *

global side
global main


class Editor(ctk.CTk):
    def __init__(self):
        super(Editor, self).__init__()

        # general attributes
        self.effects_vars = None
        self.color_vars = None
        self.pos_vars = None
        self.side = None
        self.image_output = None
        self.image_tk = None
        self.image_ratio = None
        self.image = None
        self.original = None
        self.canvas_width = 0
        self.canvas_height = 0
        self.width = 0
        self.height = 0
        ctk.set_appearance_mode('dark')
        self.title('PHOTO EDITOR')
        self.geometry('1000x600+500+200')
        self.minsize(900, 500)
        self.init_parameters()

        # layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        # widgets
        self.import_ = ImportImage(self, self.import_image)
        self.mainloop()

    def init_parameters(self):
        self.pos_vars = {
            'rotation': ctk.DoubleVar(value=rotate_default),
            'zoom': ctk.DoubleVar(value=zoom_default),
            'flip': ctk.StringVar(value=flip_options[0]),
        }

        self.color_vars = {
            'brightness': ctk.IntVar(value=brightness_default),
            'vibrance': ctk.DoubleVar(value=vibrance_default),
            'grayscale': ctk.BooleanVar(value=grayscale_default),
            'invert': ctk.BooleanVar(value=invert_default)
        }

        self.effects_vars = {
            'blur': ctk.DoubleVar(value=blur_default),
            'contrast': ctk.DoubleVar(value=contrast_default),
            'effect': ctk.StringVar(value=effect_options[0])
        }

        # tracing
        all_vars = list(self.pos_vars.values()) + list(self.color_vars.values()) + list(self.effects_vars.values())
        for var in all_vars:
            var.trace('w', self.edit_image)

    def edit_image(self, *args):
        self.image = self.original
        # rotate
        if self.pos_vars['rotation'].get() != rotate_default:
            self.image = self.image.rotate(self.pos_vars['rotation'].get())

        # zoom
        if self.pos_vars['zoom'].get() != zoom_default:
            self.image = ImageOps.crop(image=self.image, border=int(self.pos_vars['zoom'].get()))

        # flip
        if self.pos_vars['flip'].get() != 'None':
            if self.pos_vars['flip'].get() == 'X':
                self.image = ImageOps.mirror(self.image)
            if self.pos_vars['flip'].get() == 'Y':
                self.image = ImageOps.flip(self.image)
            if self.pos_vars['flip'].get() == 'Both':
                self.image = ImageOps.mirror(self.image)
                self.image = ImageOps.flip(self.image)

        # vibrance and brightness
        if self.color_vars['brightness'].get() != brightness_default:
            brightness_editor = ImageEnhance.Brightness(self.image)
            self.image = brightness_editor.enhance(self.color_vars['brightness'].get())

        if self.color_vars['vibrance'].get() != vibrance_default:
            vibrance_editor = ImageEnhance.Color(self.image)
            self.image = vibrance_editor.enhance(self.color_vars['vibrance'].get())

        # grayscale and invert
        if self.color_vars['grayscale'].get():
            self.image = ImageOps.grayscale(self.image)

        if self.color_vars['invert'].get():
            self.image = ImageOps.invert(self.image)

        # blur and contrast
        if self.effects_vars['blur'].get() != blur_default:
            self.image = self.image.filter(ImageFilter.GaussianBlur(self.effects_vars['blur'].get()))

        if self.effects_vars['contrast'].get() != contrast_default:
            self.image = self.image.filter(ImageFilter.UnsharpMask(self.effects_vars['contrast'].get()))

        if self.effects_vars['effect'].get() != 'None':
            match self.effects_vars['effect'].get():
                case 'Emboss': self.image = self.image.filter(ImageFilter.EMBOSS)
                case 'Find Edges': self.image = self.image.filter(ImageFilter.FIND_EDGES)
                case 'Contour': self.image = self.image.filter(ImageFilter.CONTOUR)
                case 'Edge enhance': self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)

        self.place_image()

    def import_image(self, path):
        self.original = Image.open(path)
        self.image = self.original
        self.image_ratio = self.image.width / self.image.height
        self.import_.grid_forget()
        self.side = SidePage(self, self.pos_vars, self.color_vars, self.effects_vars,self.export_image)
        self.image_output = MainPage(self, self.resize_image)
        CloseButton(self, self.close)

    def resize_image(self, event):

        canvas_ratio = event.width / event.height
        self.canvas_height = event.height
        self.canvas_width = event.width

        if canvas_ratio > self.image_ratio:  # canvas is wider than the pic
            # print('canvas is wider')
            self.height = int(event.height)
            self.width = self.height * self.image_ratio
        else:
            # print('canvas is taller')
            self.width = int(event.width)
            self.height = self.width / self.image_ratio

        self.place_image()

    def place_image(self):
        self.image_output.delete('all')
        resized_image = self.image.resize((int(self.width), int(self.height)))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image((int(self.canvas_width) / 2, int(self.canvas_height) / 2), image=self.image_tk)

    def close(self):
        self.side.grid_forget()
        self.image_output.grid_forget()
        ImportImage(self, self.import_image)

    def export_image(self,filename,filetype,path):
        export_way = f'{path}/{filename}.{filetype}'
        self.image.save(export_way)
        messagebox.showinfo('SAVING','The Photo has been saved')


Editor()
