import _thread

from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

from Core.addressBookHandler.addressBookHandler import addressBookHandler
from Core.LibressegeCore import LibressegeCore


class Libressege(App):
    def build(self):
        self.core = LibressegeCore(App().user_data_dir)
        self.addressBook = addressBookHandler(App().user_data_dir)

        self.screen = BoxLayout(orientation="vertical")
        self.screenManager = ScreenManager()

        self.core.start("0.0.0.0", 9091)

        #Menu panel

        self.menu_panel = BoxLayout(size_hint = (1, .22))

        self.menu_RSA_button = Button(background_normal="images/menu_RSA_button.png", background_down="images/menu_RSA_button_down.png")
        self.menu_Address_book_button = Button(background_normal="images/menu_Address_book_button.png", background_down="images/menu_Address_book_button_down.png")
        self.menu_dialog_button = Button(background_normal="images/menu_dialog_button.png", background_down="images/menu_dialog_button_down.png")
        self.menu_Servers_button = Button(background_normal="images/menu_Servers_button.png", background_down="images/menu_Servers_button_down.png")
        self.menu_Exit_button = Button(background_normal="images/menu_Exit_button.png", background_down="images/menu_Exit_button_down.png")

        self.menu_RSA_button.bind(on_press=self.menu_RSA_button_pressed)
        self.menu_Address_book_button.bind(on_press=self.menu_Address_book_button_pressed)
        self.menu_dialog_button.bind(on_press=self.menu_dialog_button_pressed)
        self.menu_Servers_button.bind(on_press=self.menu_Servers_button_pressed)
        self.menu_Exit_button.bind(on_press=self.menu_Exit_button_pressed)

        self.menu_panel.add_widget(self.menu_RSA_button)
        self.menu_panel.add_widget(self.menu_Address_book_button)
        self.menu_panel.add_widget(self.menu_dialog_button)
        self.menu_panel.add_widget(self.menu_Servers_button)
        self.menu_panel.add_widget(self.menu_Exit_button)

        #Screens


        #RSA screen

        self.RSA_screen = Screen(name="RSA")

        self.RSA_screen_main = BoxLayout(orientation="vertical")

        self.RSA_panel = BoxLayout(orientation="vertical")

        self.RSAkey_view = Label()

        self.RSA_buttons = BoxLayout()

        self.RSAgenerate_button = Button(background_normal="images/RSAgenerate_button.png", background_down="images/RSAgenerate_button_down.png")
        self.RSAimport_button = Button(background_normal="images/RSAimport_button.png", background_down="images/RSAimport_button_down.png")

        self.RSAgenerate_button.bind(on_press=self.RSAgenerate_button_pressed)
        self.RSAimport_button.bind(on_press=self.RSAimport_button_pressed)

        self.RSA_buttons.add_widget(self.RSAgenerate_button)
        self.RSA_buttons.add_widget(self.RSAimport_button)

        self.RSAclipboard_buttons = BoxLayout()

        self.RSAclipboard_copy_button = Button(background_normal="images/RSAclipboard_copy_button.png", background_down="images/RSAclipboard_copy_button_down.png")

        self.RSAclipboard_copy_button.bind(on_press=self.RSAclipboard_copy_button_pressed)

        self.RSAclipboard_buttons.add_widget(self.RSAclipboard_copy_button)

        self.RSA_panel.add_widget(self.RSAkey_view)
        self.RSA_panel.add_widget(self.RSA_buttons)
        self.RSA_panel.add_widget(self.RSAclipboard_buttons)

        self.RSA_screen_main.add_widget(self.RSA_panel)

        self.RSA_screen.add_widget(self.RSA_screen_main)


        #Address book screen

        self.Address_book_screen = Screen(name="Book")

        self.Address_book_screen_main = BoxLayout(orientation="vertical")

        self.address_book_panel = BoxLayout(orientation="vertical")

        self.address_book_input = BoxLayout()

        self.recipientName_input = TextInput(multiline = False)
        self.recipientKey_input = TextInput(multiline = False)

        self.address_book_input.add_widget(self.recipientName_input)
        self.address_book_input.add_widget(self.recipientKey_input)

        self.address_book_add_button = Button(background_normal="images/address_book_add_button.png", background_down="images/address_book_add_button_down.png")

        self.address_book_add_button.bind(on_press=self.address_book_add_button_pressed)

        self.address_book_clipboard_paste_button = Button(background_normal="images/address_book_clipboard_paste_button.png", background_down="images/address_book_clipboard_paste_button_down.png")

        self.address_book_clipboard_paste_button.bind(on_press=self.address_book_clipboard_paste_button_pressed)

        self.address_book_panel.add_widget(self.address_book_input)
        self.address_book_panel.add_widget(self.address_book_add_button)
        self.address_book_panel.add_widget(self.address_book_clipboard_paste_button)

        self.Address_book_screen_main.add_widget(self.address_book_panel)

        self.Address_book_screen.add_widget(self.Address_book_screen_main)


        #Dialog screen

        self.dialog_screen = Screen(name="Dialog")

        self.dialog_screen_main = BoxLayout(orientation="vertical")

        self.dialog_panel = BoxLayout(orientation="vertical")

        self.dialog_view = Label()

        self.send_panel = BoxLayout(orientation="vertical")

        self.send_inputs = BoxLayout()

        self.send_message_input = TextInput(multiline=False)
        self.send_recipient_input = TextInput(multiline = False)

        self.send_inputs.add_widget(self.send_message_input)
        self.send_inputs.add_widget(self.send_recipient_input)

        self.send_button = Button(background_normal="images/send_button.png", background_down="images/send_button_down.png")

        self.send_button.bind(on_press=self.send_button_pressed)

        self.send_panel.add_widget(self.send_inputs)
        self.send_panel.add_widget(self.send_button)

        self.dialog_panel.add_widget(self.dialog_view)
        self.dialog_panel.add_widget(self.send_panel)

        self.dialog_screen_main.add_widget(self.dialog_panel)

        self.dialog_screen.add_widget(self.dialog_screen_main)


        #Servers screen

        self.servers_screen = Screen(name="Servers")

        self.servers_screen_main = BoxLayout(orientation="vertical")

        self.conn_panel = BoxLayout(orientation="vertical")

        self.conn_activity = BoxLayout()

        self.conn_activity_view = Label(text="No connections")

        self.conn_activity.add_widget(self.conn_activity_view)

        self.conn_inputs = BoxLayout()

        self.serverIPInput = TextInput(multiline=False, text="93.84.85.241")
        self.serverPORTInput = TextInput(multiline=False, text="9090")
        self.nameInput = TextInput(multiline=False)

        self.conn_inputs.add_widget(self.serverIPInput)
        self.conn_inputs.add_widget(self.serverPORTInput)
        self.conn_inputs.add_widget(self.nameInput)

        self.conn_buttons = BoxLayout()

        self.connect_button = Button(background_normal="images/connect_button.png", background_down="images/connect_button_down.png")
        self.disconnect_button = Button(background_normal="images/disconnect_button.png", background_down="images/disconnect_button_down.png")

        self.connect_button.bind(on_press=self.connect_button_pressed)
        self.disconnect_button.bind(on_press=self.disconnect_button_pressed)

        self.conn_buttons.add_widget(self.connect_button)
        self.conn_buttons.add_widget(self.disconnect_button)
        
        self.conn_panel.add_widget(self.conn_activity)
        self.conn_panel.add_widget(self.conn_inputs)
        self.conn_panel.add_widget(self.conn_buttons)

        self.servers_screen_main.add_widget(self.conn_panel)

        self.servers_screen.add_widget(self.servers_screen_main)


        #ScreenManager

        self.screenManager.switch_to(self.dialog_screen)

        self.screen.add_widget(self.screenManager)
        self.screen.add_widget(self.menu_panel)

        return self.screen

    def menu_RSA_button_pressed(self, instance):
        self.screenManager.switch_to(self.RSA_screen)

    def menu_Address_book_button_pressed(self, instance):
        self.screenManager.switch_to(self.Address_book_screen)

    def menu_dialog_button_pressed(self, instance):
        self.screenManager.switch_to(self.dialog_screen)

    def menu_Servers_button_pressed(self, instance):
        self.screenManager.switch_to(self.servers_screen)

    def menu_Exit_button_pressed(self, instance):
        App.stop(self)

    def RSAgenerate_button_pressed(self, instance):
        self.core.RSAgenrateKey()
        self.RSAkey_view.text = self.core.crypto.publicKeyRSA.decode()

    def RSAimport_button_pressed(self, instance):
        self.core.RSAimportKey()
        self.RSAkey_view.text = self.core.crypto.publicKeyRSA.decode()

    def RSAclipboard_copy_button_pressed(self, instance):
        Clipboard.put(self.RSAkey_view.text)

    def address_book_clipboard_paste_button_pressed(self, instance):
        self.recipientKey_input.text = Clipboard.paste()

    def send_button_pressed(self, instance):
        self.core.sendMessage(self.send_message_input.text, self.send_recipient_input.text, self.addressBook.getKey(self.send_recipient_input.text))
        self.dialog_view.text += "\nYou: " + self.send_message_input.text
        self.send_message_input.text = ""

    def address_book_add_button_pressed(self, instance):
        self.addressBook.newAddress(self.recipientName_input.text, self.recipientKey_input.text)
        self.recipientName_input.text = ""
        self.recipientKey_input.text = ""

    def connect_button_pressed(self, instance):
        self.core.connect(self.nameInput.text, self.serverIPInput.text, int(self.serverPORTInput.text))
        self.conn_activity_view.text = "Connect to " + self.serverIPInput.text + ":" + self.serverPORTInput.text + " with username: " + self.nameInput.text
        self.dialog_view.text = ""
        self.send_message_input.text = ""
        self.send_recipient_input.text = ""
        _thread.start_new_thread(self.printMessages, ())

    def disconnect_button_pressed(self, instance):
        self.core.disconnect()
        self.conn_activity_view.text = "No connections"
        self.dialog_view.text = ""
        self.send_message_input.text = ""
        self.send_recipient_input.text = ""

    def printMessages(self):
        while True:
            data = self.core.getMessage()
            if (data != ""):
                self.dialog_view.text += "\n" + str(data)

if __name__=="__main__":
    app = Libressege()
    app.run() 
