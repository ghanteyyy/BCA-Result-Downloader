import os
import subprocess
from tkinter import *
import tkinter.ttk as ttk
from tkinter.font import Font
from images import Images
from notices import Notices
from writer import JSON
from error import Error
from settings import Settings


class bca_notice_downloader:
    def __init__(self):
        self.Writer = JSON()
        self.Notices = Notices()
        self.fetched_notices = []
        self.populate_timer = None
        self.downloads_path = self.Notices.downloads_path

        self.window = Tk()
        self.window.withdraw()

        self.main_frame = Frame(self.window)
        self.main_frame.pack()

        self.Images = Images()
        self.Error = Error(self.window, self.main_frame)
        self.Settings = Settings(self.window, self.Notices.downloads_path, self.main_frame, self.populate_notice)

        self.row_1 = Frame(self.main_frame)
        self.row_1.pack(fill='x')

        self.setting_btn = Label(self.row_1, cursor='hand2')
        self.setting_btn.pack(side=RIGHT, ipadx=5)
        self.setting_btn.config(image=self.Images.setting_image)

        self.notice_frame = Frame(self.main_frame)
        self.notice_frame.pack(fill='x', expand=True)

        self.window.after(0, self.center_window)
        self.window.mainloop()

    def center_window(self):
        '''
        Set the position of the window to the center of the screen upon program launch
        '''

        self.populate_notice()

        self.window.update()
        self.window.title('BCA Notice Downloader')
        self.window.iconphoto(False, self.Images.icon_image)

        width, height = self.window.winfo_width(), self.window.winfo_height()
        screenwidth, screenheight = self.window.winfo_screenwidth() // 2, self.window.winfo_screenheight() // 2
        self.window.geometry(f'+{screenwidth - width // 2}+{screenheight - height // 2}')

        self.window.resizable(0, 0)
        self.window.deiconify()

        self.window.resizable(False, False)

    def populate_notice(self, do_not_fetch=False):
        '''
        Create widgets for displaying notices.

        It clears existing widgets, fetches notices from web scraping
        in every minute, and populates the GUI accordingly.

        If there's no internet connection, it displays an error
        message. If there are no notices available, it also displays
        an appropriate message.

        If notices are available, it displays them with options to view or download.
        '''

        error_message = self.Error.has_error_occurred(notice=self.Notices)

        if do_not_fetch is True:
            self.window.withdraw()

        if error_message:
            self.Error.show_error(error_message)

        else:
            if do_not_fetch is False:
                notices = self.Notices.get_notices()

            else:
                notices = self.fetched_notices
                self.window.after(250, self.window.deiconify)

            if do_not_fetch is True or notices != self.fetched_notices:
                self.Error.destroy_error_message()

                for widget in self.notice_frame.winfo_children():
                    widget.destroy()

                self.fetched_notices = notices

                for notice in notices:
                    notice_name = notice['notice_name']

                    per_notice_frame = Frame(self.notice_frame, highlightthickness=2, highlightbackground='grey', highlightcolor='grey')
                    per_notice_frame.pack(fill='x', padx=5, pady=3)

                    date_label = Label(per_notice_frame, text=notice['date'], width=10, font=Font(family='Calibri', size=15), height=3, background='#43766C', foreground='whitesmoke')
                    date_label.pack(side=LEFT, ipadx=5)

                    date_separator = ttk.Separator(per_notice_frame, orient=VERTICAL)
                    date_separator.pack(side=LEFT, fill='y')

                    notice_label = Label(per_notice_frame, text=notice_name, font=Font(family='Calibri', size=15), height=3, background='#43766C', foreground='whitesmoke')
                    notice_label.pack(side=LEFT, fill='x', expand=True, ipadx=20)

                    buttons_frame = Frame(per_notice_frame)
                    buttons_frame.pack(side=LEFT, ipadx=3)

                    is_notice_downloaded = notice['is_pdf_downloaded']

                    if is_notice_downloaded:
                        self.place_buttons_after_downloading(buttons_frame, notice_name)

                    else:
                        download_button = Label(buttons_frame, relief=FLAT, cursor='hand2')
                        download_button.pack(fill=BOTH, expand=True)
                        download_button.config(image=self.Images.download_pdf_image)
                        download_button.bind('<Button-1>', lambda event=Event, frame=buttons_frame, download_link=notice['download_link']: self.download_notice(event, frame, download_link))

        self.populate_timer = self.window.after(60000, self.populate_notice)
        self.setting_btn.bind('<Button-1>', lambda event=Event, populate_timer=self.populate_timer: self.Settings.show_settings_widgets(event, populate_timer))

    def place_buttons_after_downloading(self, frame, notice_name):
        '''
        Place the 'open_in_folder' and 'open_in_browser' buttons after
        the user downloads the PDF, or only place download buttons when
        the PDF has not been downloaded
        '''

        for widget in frame.winfo_children():
            widget.destroy()

        label_common_attributes = {'relief': FLAT, 'cursor': 'hand2'}

        open_in_browser_button = Label(frame, image=self.Images.open_in_browser_image, **label_common_attributes)
        open_in_browser_button.pack()
        open_in_browser_button.config(image=self.Images.open_in_browser_image)
        open_in_browser_button.bind('<Button-1>', lambda event=Event, pdf_name=notice_name: self.show_in_browser(event, pdf_name))

        open_in_explorer_button = Label(frame, **label_common_attributes)
        open_in_explorer_button.pack(fill=BOTH, expand=True)
        open_in_explorer_button.config(image=self.Images.show_in_directory_image)
        open_in_explorer_button.bind('<Button-1>', lambda event=Event, pdf_name=notice_name: self.show_in_explorer(event, pdf_name))

        delete_button = Label(frame, **label_common_attributes)
        delete_button.pack()
        delete_button.config(image=self.Images.delete_image)
        delete_button.bind('<Button-1>', lambda event=Event, frame=frame, pdf_name=notice_name: self.delete_notice(event, frame, pdf_name))

    def download_notice(self, event, frame, download_link):
        """
        Downloads the PDF file from the specified link and updates the GUI accordingly
        """

        pdf_name = os.path.basename(download_link)
        pdf_path = os.path.join(self.downloads_path, pdf_name)

        with open(pdf_path, 'wb') as f:  # Saving pdf to the download path
            content = self.Notices.session.get(download_link, stream=True)
            contents = content.content
            f.write(contents)

        self.place_buttons_after_downloading(frame, pdf_name)

    def show_in_browser(self, event, pdf_name):
        """
        Open the downloaded pdf in default browser.
        """

        pdf_path = os.path.join(self.downloads_path, pdf_name)
        os.startfile(pdf_path)

    def show_in_explorer(self, event, pdf_name):
        """
        Open the file explorer and reveal the downloaded PDF.
        """

        pdf_path = os.path.join(self.downloads_path, pdf_name)
        FILE_BROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

        subprocess.run([FILE_BROWSER_PATH, '/select,', pdf_path])

    def delete_notice(self, event, frame, pdf_name):
        '''
        Remove the downloaded pdf from the device
        '''

        pdf_path = os.path.join(self.downloads_path, pdf_name)

        os.remove(pdf_path)
        frame.master.destroy()

        self.Writer.write_json(pdf_name)


if __name__ == '__main__':
    bca_notice_downloader()
