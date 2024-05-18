from tkinter import *
from tkinter.font import Font
import utils


class Error:
    def __init__(self, window, main_frame):
        self.window = window
        self.main_frame = main_frame
        self.is_error_message_shown = False

    def has_error_occurred(self, notice):
        """
        Checks for errors related to internet connectivity and the presence of notices.

        This method evaluates two potential error conditions:
            - Lack of internet connectivity.
            - Absence of published notices.

        Returns:
            str: A message describing the error if one has occurred, either:
                - 'Unable to connect to the internet' if there is no internet connection.
                - 'No notices have been published as of yet !!!' if there are no notices.
                None if no errors are found.
        """

        if utils.is_internet() is False:
            return 'Unable to connect to the internet'

        elif len(notice.get_notices()) == 0:
            return 'No notices have been published as of yet !!!'

    def show_error(self, error_message):
        '''
        Display error messages under the following conditions:
            - No internet connection detected
            - No notice published
        '''

        if self.is_error_message_shown is False:
            self.main_frame.pack_forget()
            self.is_error_message_shown = True

            self.inner_frame = Frame(self.window, background='whitesmoke')
            self.inner_frame.pack()

            no_notice_label = Label(self.inner_frame, text=error_message, font=Font(family='Calibri', size=20), justify=CENTER, height=3, background='whitesmoke', foreground='#FF204E')
            no_notice_label.pack(ipadx=10, fill=BOTH)

            re_checking_frame = Frame(self.inner_frame, background='whitesmoke')
            re_checking_frame.pack()

            dot_string_text = StringVar()
            re_checking_info_label = Label(re_checking_frame, text='Continuously trying every minute', font=Font(family='Calibri', size=12), justify=CENTER, height=3, background='whitesmoke', foreground='grey')
            re_checking_info_label.pack(side=LEFT, ipadx=10)

            dot_label = Label(re_checking_frame, textvariable=dot_string_text, width=3, font=Font(family='Calibri', size=15), justify=CENTER, height=3, background='whitesmoke', foreground='grey')
            dot_label.pack(side=RIGHT, ipadx=10)

            self.animate_dot(dot_string_text)

    def animate_dot(self, string_var):
        '''
        Animate '•' in classic loading fashion
        '''

        if self.is_error_message_shown:
            dot_symbol = '•'
            number_of_dots = string_var.get().count(dot_symbol)

            dot_numbering = number_of_dots + 1 if number_of_dots < 3 else 1
            update_dots = dot_symbol * dot_numbering

            string_var.set(update_dots)
            self.animate_dot_timer = self.window.after(1000, lambda: self.animate_dot(string_var))

    def destroy_error_message(self):
        '''
        Remove error messages
        '''

        self.is_error_message_shown = False
        self.inner_frame.pack_forget()
