import _thread

from functools import partial

from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from Core.addressBookHandler.addressBookHandler import addressBookHandler, connectBookHandler, dialogsBookHandler
from Core.LibressegeCore import LibressegeCore


class Libressege(App):
    def build(self):
        self.core = LibressegeCore(App().user_data_dir)
        self.addressBook = addressBookHandler(App().user_data_dir)
        self.connectBook = connectBookHandler(App().user_data_dir)
        self.dialogsBook = dialogsBookHandler(App().user_data_dir)

        self.CipherScreen = self.CreateCipherScreen()
        self.AddressBookScreen = self.CreateAddressBookScreen()
        self.DialogsScreen = self.CreateDialogsScreen()
        self.ConnectScreen = self.CreateConnectScreen()

        self.screenManager = ScreenManager()

        self.interlocutor = None

        self.core.start("0.0.0.0", 9091)

        mainScreen = BoxLayout(orientation="vertical")
        mainScreen.add_widget(self.screenManager)

        self.MainScreen = Screen(name="Main")
        MainScreenLayout = BoxLayout(orientation="vertical")

        self.MainScreenScreenManager = ScreenManager()
        self.MainScreenScreenManager.switch_to(self.DialogsScreen)

        MainScreenScreenLayout = BoxLayout()
        MainScreenScreenLayout.add_widget(self.MainScreenScreenManager)

        MenuWidget = self.CreateMenuWidget()

        MainScreenLayout.add_widget(MainScreenScreenLayout)
        MainScreenLayout.add_widget(MenuWidget)

        self.MainScreen.add_widget(MainScreenLayout)

        self.NewDialogScreen = self.CreateNewDialogScreen()
        self.DialogScreen = self.CreateDialogScreen()

        self.screenManager.switch_to(self.MainScreen)

        return mainScreen

#Screen Creators

    def CreateConnectScreen(self):
        screen = Screen(name="Connect")

        conn_panel = BoxLayout(orientation="vertical")

        self.ConnectView = ScrollView(do_scroll_x=False, do_scroll_y=True)

        self.ConnectViewItems = BoxLayout(orientation="vertical")

        for name in self.connectBook.getServers():
            viewItem = BoxLayout()
            view = Label(text=name)
            ConnectBookViewItemButtonChoice = Button(text="choise", background_color=(.18, .56, .81, 1))
            ConnectBookViewItemButtonChoice.bind(on_press=partial(self.ConnectBookViewItemButtonChoice_pressed, name=name))
            ConnectBookViewItemButtonDelete = Button(text="delete", background_color=(.18, .56, .81, 1))
            ConnectBookViewItemButtonDelete.bind(on_press=partial(self.ConnectBookViewItemButtonDelete_pressed, name=name))
            viewItem.add_widget(view)
            viewItem.add_widget(ConnectBookViewItemButtonChoice)
            viewItem.add_widget(ConnectBookViewItemButtonDelete)
            self.ConnectViewItems.add_widget(viewItem)

        self.ConnectView.add_widget(self.ConnectViewItems)

        conn_activity = BoxLayout()

        self.conn_activity_view = Label(text="No connections")

        conn_activity.add_widget(self.conn_activity_view)

        conn_inputs = BoxLayout()

        self.serverIPInput = TextInput(multiline=False)
        self.serverPORTInput = TextInput(multiline=False)
        self.nameInput = TextInput(multiline=False)

        conn_inputs.add_widget(self.serverIPInput)
        conn_inputs.add_widget(self.serverPORTInput)
        conn_inputs.add_widget(self.nameInput)

        conn_buttons = BoxLayout()

        connect_button = Button(text="connect", background_color=(.18, .56, .81, 1))
        disconnect_button = Button(text="disconnect", background_color=(.18, .56, .81, 1))

        connect_button.bind(on_press=self.connect_button_pressed)
        disconnect_button.bind(on_press=self.disconnect_button_pressed)

        conn_buttons.add_widget(connect_button)
        conn_buttons.add_widget(disconnect_button)

        self.conn_add_input = TextInput(multiline=False)

        conn_add_button = Button(text="Add to connect book", background_color=(.18, .56, .81, 1))
        conn_add_button.bind(on_press=self.conn_add_button_pressed)
        
        conn_panel.add_widget(self.ConnectView)
        conn_panel.add_widget(conn_activity)
        conn_panel.add_widget(conn_inputs)
        conn_panel.add_widget(conn_buttons)
        conn_panel.add_widget(self.conn_add_input)
        conn_panel.add_widget(conn_add_button)

        screen.add_widget(conn_panel)

        return screen

    def CreateDialogScreen(self):
        screen= Screen(name="Dialog")

        dialog_panel = BoxLayout(orientation="vertical")

        back_button = Button(text="back", background_color=(.18, .56, .81, 1))
        back_button.bind(on_press=partial(self.back_button_pressed, screen=self.MainScreen))

        self.dialog_view = Label()

        send_panel = BoxLayout(orientation="vertical")

        self.DialogView = ScrollView(do_scroll_x=False, do_scroll_y=True)

        self.DialogViewItems = BoxLayout(orientation="vertical")

        self.DialogView.add_widget(self.DialogViewItems)

        send_inputs = BoxLayout()

        self.send_message_input = TextInput(multiline=False)
        

        send_inputs.add_widget(self.send_message_input)

        send_button = Button(text="send", background_color=(.18, .56, .81, 1))
        send_button.bind(on_press=self.send_button_pressed)

        send_panel.add_widget(send_inputs)
        send_panel.add_widget(send_button)

        dialog_panel.add_widget(back_button)
        dialog_panel.add_widget(self.DialogView)
        dialog_panel.add_widget(self.dialog_view)
        dialog_panel.add_widget(send_panel)

        screen.add_widget(dialog_panel)

        return screen

    def CreateDialogsScreen(self):
        screen = Screen(name="Dialogs")

        dialogs_panel = BoxLayout(orientation="vertical")

        self.DialogsView = ScrollView(do_scroll_x=False, do_scroll_y=True)

        self.DialogsViewItems = BoxLayout(orientation="vertical")

        for dialog in self.dialogsBook.getDialogs():
            viewItem = BoxLayout()
            dialog_button = Button(text=dialog, background_color=(.39, .78, 1, 1))
            dialog_button.bind(on_press=self.dialog_button_pressed)
            DialogsViewItemButtonDelete = Button(text="delete", background_color=(.18, .56, .81, 1))
            DialogsViewItemButtonDelete.bind(on_press=partial(self.DialogsViewItemButtonDelete_pressed, name=dialog))
            viewItem.add_widget(dialog_button)
            viewItem.add_widget(DialogsViewItemButtonDelete)
            self.DialogsViewItems.add_widget(viewItem)

        self.DialogsView.add_widget(self.DialogsViewItems)

        new_dialog_button = Button(text="new dialog", background_color=(.18, .56, .81, 1), size_hint=(1, .30))
        new_dialog_button.bind(on_press=self.new_dialog_button_pressed)

        dialogs_panel.add_widget(self.DialogsView)
        dialogs_panel.add_widget(new_dialog_button)

        screen.add_widget(dialogs_panel)

        return screen

    def CreateNewDialogScreen(self):
        screen = Screen(name="New dialog")

        new_dialog_panel = BoxLayout(orientation="vertical")

        back_button = Button(text="back", background_color=(.18, .56, .81, 1))
        back_button.bind(on_press=partial(self.back_button_pressed, screen=self.MainScreen))

        self.create_dialog_recipient_input = TextInput(multiline = False)

        new_dialog_button = Button(text="create dialog", background_color=(.18, .56, .81, 1))
        new_dialog_button.bind(on_press=self.create_dialog_button_pressed)
        
        new_dialog_panel.add_widget(back_button)
        new_dialog_panel.add_widget(self.create_dialog_recipient_input)
        new_dialog_panel.add_widget(new_dialog_button)

        screen.add_widget(new_dialog_panel)

        return screen

    def CreateAddressBookScreen(self):
        screen = Screen(name="AddressBook")

        address_book_panel = BoxLayout(orientation="vertical")

        self.AddressBookView = ScrollView(do_scroll_x=False, do_scroll_y=True)

        self.AddressBookViewItems = BoxLayout(orientation="vertical")

        for name in self.addressBook.getNames():
            viewItem = BoxLayout()
            view = Label(text=name)
            AddressBookViewItemButton = Button(text="delete", background_color=(.18, .56, .81, 1))
            AddressBookViewItemButton.bind(on_press=partial(self.AddressBookViewItemButton_pressed, name=name))
            viewItem.add_widget(view)
            viewItem.add_widget(AddressBookViewItemButton)
            self.AddressBookViewItems.add_widget(viewItem)

        self.AddressBookView.add_widget(self.AddressBookViewItems)

        address_book_input = BoxLayout()

        self.recipientName_input = TextInput(multiline = False)
        self.recipientKey_input = TextInput(multiline = False)

        address_book_input.add_widget(self.recipientName_input)
        address_book_input.add_widget(self.recipientKey_input)

        address_book_add_button = Button(text="add", background_color=(.18, .56, .81, 1))

        address_book_add_button.bind(on_press=self.address_book_add_button_pressed)

        address_book_clipboard_paste_button = Button(text="paste key", background_color=(.18, .56, .81, 1))

        address_book_clipboard_paste_button.bind(on_press=self.address_book_clipboard_paste_button_pressed)

        address_book_panel.add_widget(self.AddressBookView)
        address_book_panel.add_widget(address_book_input)
        address_book_panel.add_widget(address_book_add_button)
        address_book_panel.add_widget(address_book_clipboard_paste_button)

        screen.add_widget(address_book_panel)

        return screen

    def CreateCipherScreen(self):
        screen = Screen(name="Cipher")

        RSA_panel = BoxLayout(orientation="vertical")

        self.RSAkey_view = Label()

        RSA_buttons = BoxLayout()

        RSAgenerate_button = Button(text="generate key", background_color=(.18, .56, .81, 1))
        RSAimport_button = Button(text="import key", background_color=(.18, .56, .81, 1))

        RSAgenerate_button.bind(on_press=self.RSAgenerate_button_pressed)
        RSAimport_button.bind(on_press=self.RSAimport_button_pressed)

        RSA_buttons.add_widget(RSAgenerate_button)
        RSA_buttons.add_widget(RSAimport_button)

        RSAclipboard_buttons = BoxLayout()

        RSAclipboard_copy_button = Button(text="copy key", background_color=(.18, .56, .81, 1))

        RSAclipboard_copy_button.bind(on_press=self.RSAclipboard_copy_button_pressed)

        RSAclipboard_buttons.add_widget(RSAclipboard_copy_button)

        RSA_panel.add_widget(self.RSAkey_view)
        RSA_panel.add_widget(RSA_buttons)
        RSA_panel.add_widget(RSAclipboard_buttons)

        screen.add_widget(RSA_panel)

        return screen

#Widget Creators

    def CreateMenuWidget(self):
        Widget = BoxLayout(size_hint = (1, .18))

        RSA_button = Button(text="RSA", background_color=(.18, .56, .81, 1))
        address_book_button = Button(text="addressBook", background_color=(.18, .56, .81, 1))
        dialog_button = Button(text="dialogs", background_color=(.18, .56, .81, 1))
        servers_button = Button(text="connect", background_color=(.18, .56, .81, 1))
        exit_button = Button(text="exit", background_color=(.18, .56, .81, 1))

        RSA_button.bind(on_press=self.menu_RSA_button_pressed)
        address_book_button.bind(on_press=self.menu_Address_book_button_pressed)
        dialog_button.bind(on_press=self.menu_dialog_button_pressed)
        servers_button.bind(on_press=self.menu_Servers_button_pressed)
        exit_button.bind(on_press=self.menu_Exit_button_pressed)

        Widget.add_widget(RSA_button)
        Widget.add_widget(address_book_button)
        Widget.add_widget(dialog_button)
        Widget.add_widget(servers_button)
        Widget.add_widget(exit_button)

        return Widget

#Button click Handlers

    def menu_RSA_button_pressed(self, instance):
        self.MainScreenScreenManager.switch_to(self.CipherScreen)

    def menu_Address_book_button_pressed(self, instance):
        self.MainScreenScreenManager.switch_to(self.AddressBookScreen)

    def menu_dialog_button_pressed(self, instance):
        self.MainScreenScreenManager.switch_to(self.DialogsScreen)

    def menu_Servers_button_pressed(self, instance):
        self.MainScreenScreenManager.switch_to(self.ConnectScreen)

    def menu_Exit_button_pressed(self, instance):
        App.stop(self)

    def RSAgenerate_button_pressed(self, instance):
        self.core.RSAgenrateKey()
        self.RSAkey_view.text = self.core.GhostConnect.publicKeyRSA.decode()

    def RSAimport_button_pressed(self, instance):
        self.core.RSAimportKey()
        self.RSAkey_view.text = self.core.GhostConnect.publicKeyRSA.decode()

    def RSAclipboard_copy_button_pressed(self, instance):
        Clipboard.put(self.RSAkey_view.text)

    def address_book_clipboard_paste_button_pressed(self, instance):
        self.recipientKey_input.text = Clipboard.paste()

    def send_button_pressed(self, instance):
        self.core.sendMessage(self.send_message_input.text, self.interlocutor, self.addressBook.getKey(self.interlocutor))
        self.dialogsBook.newMessage(self.interlocutor, self.send_message_input.text, "You")
        self.send_message_input.text = ""
        self.DialogViewUpdate()

    def address_book_add_button_pressed(self, instance):
        self.addressBook.newAddress(self.recipientName_input.text, self.recipientKey_input.text)
        self.recipientName_input.text = ""
        self.recipientKey_input.text = ""
        self.AddressBookViewUpdate()

    def connect_button_pressed(self, instance):
        self.core.connect(self.nameInput.text, self.serverIPInput.text, int(self.serverPORTInput.text))
        self.conn_activity_view.text = "Connect to " + self.serverIPInput.text + ":" + self.serverPORTInput.text + " with username: " + self.nameInput.text
        _thread.start_new_thread(self.printMessages, ())

    def disconnect_button_pressed(self, instance):
        self.core.disconnect()
        self.conn_activity_view.text = "No connections"
        self.dialog_view.text = ""
        self.send_message_input.text = ""
        self.send_recipient_input.text = ""

    def conn_add_button_pressed(self, instance):
        self.connectBook.newServer(self.conn_add_input.text, self.serverIPInput.text, self.serverPORTInput.text)
        self.ConnectBookViewUpdate()

    def AddressBookViewItemButton_pressed(self, instance, name):
        self.addressBook.deleteAddress(name)
        self.AddressBookViewUpdate()

    def ConnectBookViewItemButtonDelete_pressed(self, instanse, name):
        self.connectBook.deleteServer(name)
        self.ConnectBookViewUpdate()

    def ConnectBookViewItemButtonChoice_pressed(self, instance, name):
        self.serverIPInput.text = self.connectBook.getServer(name)[0]
        self.serverPORTInput.text = str(self.connectBook.getServer(name)[1])

    def DialogsViewItemButtonDelete_pressed(self, instance, name):
        self.dialogsBook.deleteDialog(name)
        self.DialogsBookViewUpdate()

    def dialog_button_pressed(self, instance):
        self.interlocutor = instance.text
        self.DialogViewUpdate()
        self.screenManager.switch_to(self.DialogScreen)

    def new_dialog_button_pressed(self, instance):
        self.screenManager.switch_to(self.NewDialogScreen)

    def create_dialog_button_pressed(self, instance):
        self.dialogsBook.newDialog(self.create_dialog_recipient_input.text)
        self.create_dialog_recipient_input.text = ""
        self.DialogsBookViewUpdate()
        self.screenManager.switch_to(self.MainScreen)

    def back_button_pressed(self, instance, screen):
        self.screenManager.switch_to(screen)

    def printMessages(self):
        while True:
            data = self.core.getMessage()
            if (data != ""):
                self.dialogsBook.newMessage(self.interlocutor, data, self.interlocutor)
                self.DialogViewUpdate()

#Updaters

    def AddressBookViewUpdate(self):
        self.AddressBookView.remove_widget(self.AddressBookViewItems)

        self.AddressBookViewItems = BoxLayout(orientation="vertical")

        for name in self.addressBook.getNames():
            viewItem = BoxLayout()
            view = Label(text=name)
            AddressBookViewItemButton = Button(text="delete", background_color=(.18, .56, .81, 1))
            AddressBookViewItemButton.bind(on_press=partial(self.AddressBookViewItemButton_pressed, name=name))
            viewItem.add_widget(view)
            viewItem.add_widget(AddressBookViewItemButton)
            self.AddressBookViewItems.add_widget(viewItem)

        self.AddressBookView.add_widget(self.AddressBookViewItems)

    def ConnectBookViewUpdate(self):
        self.ConnectView.remove_widget(self.ConnectViewItems)

        self.ConnectViewItems = BoxLayout(orientation="vertical")

        for name in self.connectBook.getServers():
            viewItem = BoxLayout()
            view = Label(text=name)
            ConnectBookViewItemButtonChoice = Button(text="choise", background_color=(.18, .56, .81, 1))
            ConnectBookViewItemButtonChoice.bind(on_press=partial(self.ConnectBookViewItemButtonChoice_pressed, name=name))
            ConnectBookViewItemButtonDelete = Button(text="delete", background_color=(.18, .56, .81, 1))
            ConnectBookViewItemButtonDelete.bind(on_press=partial(self.ConnectBookViewItemButtonDelete_pressed, name=name))
            viewItem.add_widget(view)
            viewItem.add_widget(ConnectBookViewItemButtonChoice)
            viewItem.add_widget(ConnectBookViewItemButtonDelete)
            self.ConnectViewItems.add_widget(viewItem)

        self.ConnectView.add_widget(self.ConnectViewItems)

    def DialogsBookViewUpdate(self):
        self.DialogsView.remove_widget(self.DialogsViewItems)

        self.DialogsViewItems = BoxLayout(orientation="vertical")

        for dialog in self.dialogsBook.getDialogs():
            viewItem = BoxLayout()
            dialog_button = Button(text=dialog, background_color=(.39, .78, 1, 1))
            dialog_button.bind(on_press=self.dialog_button_pressed)
            DialogsViewItemButtonDelete = Button(text="delete", background_color=(.18, .56, .81, 1))
            DialogsViewItemButtonDelete.bind(on_press=partial(self.DialogsViewItemButtonDelete_pressed, name=dialog))
            viewItem.add_widget(dialog_button)
            viewItem.add_widget(DialogsViewItemButtonDelete)
            self.DialogsViewItems.add_widget(viewItem)

        self.DialogsView.add_widget(self.DialogsViewItems)

    def DialogViewUpdate(self):
        self.DialogView.remove_widget(self.DialogViewItems)

        self.DialogViewItems = BoxLayout(orientation="vertical")

        for message in self.dialogsBook.getDialog(self.interlocutor):
            viewItem = BoxLayout()
            view = Label(text=message)
            viewItem.add_widget(view)
            self.DialogViewItems.add_widget(viewItem)

        self.DialogView.add_widget(self.DialogViewItems)

if __name__=="__main__":
    app = Libressege()
    app.run() 
