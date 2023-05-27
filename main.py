from kivy import platform
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.relativelayout import MDRelativeLayout

from user_database import Database

db = Database()

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                         Permission.READ_EXTERNAL_STORAGE])


class ClickableTextField(MDRelativeLayout):
    password = StringProperty()


class CreatePasswordClickableTextField(MDRelativeLayout):
    create_password = StringProperty()


class ConfirmPasswordClickableTextField(MDRelativeLayout):
    confirmpassword = StringProperty()


class FirstWindow(Screen):

    Builder.load_file('firstwindow.kv')

    def login(self):

        # If input(s) are incomplete
        if self.ids.username.text or self.ids.password.passw.text:
            # If username exists
            if db.locateUsername(self.ids.username.text) is True:
                # If password is correct
                if db.locateAcc(self.ids.username.text,
                                self.ids.password.passw.text) is True:
                    self.clear()
                    self.manager.current = "third"
                    self.manager.transition.direction = "left"
                else:
                    self.error_dialog(message="The password is incorrect.")
                    self.ids.password.passw.text = ''
            else:
                self.error_dialog(
                    message="Sorry, we couldn't find an account with that username.")
                self.ids.password.passw.text = ''
        else:
            self.error_dialog(
                message="Make sure that username and password are not empty.")

    def clear(self):
        self.ids.username.text = ''
        self.ids.password.passw.text = ''

    def error_dialog(self, message):

        close_button = MDFlatButton(
            text='CLOSE',
            text_color=[0, 0, 0, 1],
            on_release=self.close_dialog,
        )
        self.dialog = MDDialog(
            title='[color=#FF0000]Ooops![/color]',
            text=message,
            buttons=[close_button],
        )
        self.dialog.open()

    # Close Dialog
    def close_dialog(self, obj):
        self.dialog.dismiss()


class SecondWindow(Screen):

    Builder.load_file('secondwindow.kv')

    def signUp(self):
        username = self.ids.create_username.text
        create_password = self.ids.create_password.create_passw.text
        confirm_password = self.ids.confirm_password.confirm_passw.text

        # If input(s) are incomplete
        if (username or create_password or confirm_password) and (create_password or confirm_password) and username:
            # If username exists
            if db.locateUsername(username) is False:
                # If passwords matched
                if create_password == confirm_password:
                    db.storeAcc(username, create_password)
                    self.ids.create_username.text = ''
                    self.ids.create_password.create_passw.text = ''
                    self.ids.confirm_password.confirm_passw.text = ''
                    self.manager.current = "first"
                    self.manager.transition.direction = "right"
                else:
                    self.error_dialog(message="The password does not match.")
                    self.ids.create_password.create_passw.text = ''
                    self.ids.confirm_password.confirm_passw.text = ''
            else:
                self.error_dialog(
                    message="The username you entered is already in used.")
                self.ids.create_password.create_passw.text = ''
                self.ids.confirm_password.confirm_passw.text = ''
        else:
            self.error_dialog(
                message="Make sure to fill up all the required information to proceed.")

    def clear(self):
        self.ids.create_username.text = ''
        self.ids.create_password.create_passw.text = ''
        self.ids.confirm_password.confirm_passw.text = ''

    def error_dialog(self, message):

        close_button = MDFlatButton(
            text='CLOSE',
            text_color=[0, 0, 0, 1],
            on_release=self.close_dialog,
        )
        self.dialog = MDDialog(
            title='[color=#FF0000]Ooops![/color]',
            text=message,
            buttons=[close_button],
        )
        self.dialog.open()

    # Close Dialog
    def close_dialog(self, obj):
        self.dialog.dismiss()


class ThirdWindow(Screen):

    Builder.load_file('thirdwindow.kv')


"""
    def callback(self):
        print("hehe")
        
    def on_pre_enter(self, *args):
        self.data_tables = MDDataTable(
        size_hint=(0.9, 0.8),
        pos_hint=({'center_x':0.5,'center_y':0.45}),
        use_pagination=True,
        check=True,
        background_color_selected_cell="lightblue",
        background_color_header="lightblue",
        rows_num=15,
        column_data=[
        ("User ID", dp(30)),
        ("Username", dp(30)),
        ("Salted Password", dp(80)),
        ("Hashed Password", dp(120)),
        ],
        # Using loadAcc module to return all the information from the database
        row_data=db.allAcc()
        )
        self.add_widget(self.data_tables)

    def delete_checked_rows(self):

        def deselect_rows(*args):
            self.data_tables.table_data.select_all("normal")

        for data in self.data_tables.get_row_checks():

           db.removeAcc(data[0])
        
        self.data_tables.row_data = db.allAcc()

        Clock.schedule_once(deselect_rows)
"""


class WindowManager(ScreenManager):
    pass


class rawApp(MDApp):

    def build(self):

        return WindowManager()

    def on_start(self, **kwargs):

        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions(
                [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])


if __name__ == '__main__':
    rawApp().run()
