import os
import json
from tkinter import *
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
from tkinter.font import Font
from images import Images
import utils


class Settings:
    def __init__(self, window, download_path, main_frame, populate_widgets):
        self.window = window

        self.images = Images()

        self.main_frame = main_frame
        self.download_path = download_path
        self.populate_widgets = populate_widgets

        self.setting_json = utils.resource_path('settings.json')

    def set_default_settings(self):
        with open(self.setting_json, 'w') as f:
            contents = {
                'default_download_path': self.download_path,
            }

            json.dump(contents, f, indent=4)

    def save_settings(self, event=None):
        '''
        Save settings for the GUI behavior
        '''

        default_path = self.default_download_input.get().strip()

        if os.path.exists(default_path) is False:
            messagebox.showerror('ERR', f'Path does not exists: {default_path}')
            return

        with open(self.setting_json, 'w') as f:
            contents = {
                'default_download_path': default_path,
            }

            json.dump(contents, f, indent=4)

    def get_settings(self):
        '''
        Get settings details
        '''

        try:
            with open(self.setting_json) as f:
                return json.load(f)

        except json.JSONDecodeError:
            self.set_default_settings()

            return self.get_settings()

    def show_settings_widgets(self, event, populate_timer):
        '''
        Show required setting widgets
        '''

        self.window.after_cancel(populate_timer)
        self.main_frame.pack_forget()

        settings = self.get_settings()

        self.window.title('BCA Notices - Settings')

        self.directory_path_var = StringVar()
        self.directory_path_var.set(settings['default_download_path'])

        self.settings_frame = Frame(self.window)
        self.settings_frame.pack()

        self.row_1 = Frame(self.settings_frame)
        self.row_1.pack()

        self.default_download_label = Label(self.row_1, text='Default Save Path', font=Font(family='Calibri', size=13))
        self.default_download_label.pack(side=LEFT, ipadx=10, ipady=10)

        self.default_download_input = ttk.Entry(self.row_1, width=50, textvariable=self.directory_path_var)
        self.default_download_input.pack(side=LEFT)

        self.select_directory_button = Label(self.row_1)
        self.select_directory_button.pack(side=LEFT, ipady=10)
        self.select_directory_button.config(image=self.images.show_in_directory_image)
        self.select_directory_button.bind('<Button-1>', self.file_dialog_box)

        self.buttons_frame = Frame(self.settings_frame)
        self.buttons_frame.pack(side=RIGHT, fill='both', expand=True, padx=5, pady=5)

        self.cancel_button = Label(self.buttons_frame, text='Cancel', font=Font(size=10), highlightthickness=2, highlightbackground='grey', highlightcolor='grey', cursor='hand2')
        self.cancel_button.pack(side=RIGHT, ipadx=10, ipady=5, padx=5)

        self.apply_button = Label(self.buttons_frame, text='Apply', font=Font(size=10), highlightthickness=2, highlightbackground='grey', highlightcolor='grey', cursor='hand2')
        self.apply_button.pack(side=RIGHT, ipadx=10, ipady=5, padx=5)

        self.apply_button.bind('<Button-1>', self.save_settings)
        self.cancel_button.bind('<Button-1>', self.cancel_settings)

    def file_dialog_box(self, event=None):
        '''
        Ask user to select directory to save downloaded pdf
        '''

        directory = filedialog.askdirectory(title="Select Directory")

        if directory:
            self.directory_path_var.set(directory)

    def cancel_settings(self, event=None):
        '''
        When user clicks cancel button
        '''

        self.settings_frame.destroy()
        self.main_frame.pack()

        self.window.after(0, lambda: self.populate_widgets(do_not_fetch=True))
