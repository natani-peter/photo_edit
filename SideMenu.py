from abc import ABC
from panels import *


class SidePage(ctk.CTkTabview, ABC):
    def __init__(self, parent, position, color, effect, export):
        super(SidePage, self).__init__(master=parent, fg_color=gray)
        self.grid(column=0, row=0, sticky='news', padx=5, pady=5)

        # tabs
        self.add('Position')
        self.add('Color')
        self.add('Effects')
        self.add('Export')

        # widgets
        Position(self.tab('Position'), position)
        Color(self.tab('Color'), color)
        Effects(self.tab('Effects'), effect)
        Export(self.tab('Export'), export)


class Position(ctk.CTkFrame):
    def __init__(self, parent, position, ):
        super(Position, self).__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        SliderPanel(self, 'Rotation', position['rotation'], 0, 360)
        SliderPanel(self, 'Zoom', position['zoom'], 0, 500)
        Segmented(self, 'Flip', position['flip'], flip_options)
        Revert(self,
               (position['rotation'], rotate_default),
               (position['zoom'], zoom_default),
               (position['flip'], flip_options[0])
               )


class Color(ctk.CTkFrame):
    def __init__(self, parent, color):
        super(Color, self).__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        Switch(self, ('B/W', color['grayscale']), ('Invert', color['invert']))
        SliderPanel(self, 'Brightness', color['brightness'], 0, 5)
        SliderPanel(self, 'Vibrance', color['vibrance'], 0, 5)
        Revert(self,
               (color['grayscale'], grayscale_default),
               (color['invert'], invert_default),
               (color['brightness'], brightness_default),
               (color['vibrance'], vibrance_default)
               )


class Effects(ctk.CTkFrame):
    def __init__(self, parent, effect):
        super(Effects, self).__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        DropDownPanel(self, effect['effect'], effect_options)
        SliderPanel(self, 'Blur', effect['blur'], 0, 10)
        SliderPanel(self, 'Contrast', effect['contrast'], 0, 10)
        Revert(self,
               (effect['effect'], effect_options[0]),
               (effect['blur'], blur_default),
               (effect['contrast'], contrast_default),
               )


class Export(ctk.CTkFrame):
    def __init__(self, parent, export):
        super(Export, self).__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        filename = ctk.StringVar()
        filetype = ctk.StringVar(value='jpg')
        filepath = ctk.StringVar()

        FileName(self, filename, filetype)
        FilePath(self, filepath)
        SaveButton(self, export, filename, filetype, filepath)
