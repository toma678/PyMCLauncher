from gi.repository import Gtk
import PyMCLibs
class PyMCWindow():
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("PYMC Launcher.glade")
        self.window = self.builder.get_object("pymclauncher")
        self.window.show_all()
        self.handlerdict = {
            "on_pymclauncher_destroy" : Gtk.main_quit,
            "on_login_clicked" : self.onLoginClicked
            }
        self.builder.connect_signals(self.handlerdict)
        Gtk.main()
    def onLoginClicked(self, uselessarg):
        #Gets objects to be used later
        self.usernameob = self.builder.get_object("username")
        self.passwordob = self.builder.get_object("password")
        self.spinner = self.builder.get_object("spinner")
        self.loginstatus = self.builder.get_object("loginstatus")
        #Greys out the username & password entry boxes so they can't be edited whilst logging in & starts the spinner.
        self.usernameob.set_can_focus(False)
        self.passwordob.set_can_focus(False)
        self.spinner.start()
        self.username = self.usernameob.get_text()
        self.password = self.passwordob.get_text()
        loginresponse = PyMCLibs.login(self.username, self.password)
        if(loginresponse=="-un&pw"):
            loginstatus.push(1, "Please enter a Username and Password")
            spinner.stop()
            usernameob.set_can_focus(True)
            passwordob.set_can_focus(True)
            return
        elif(loginresponse=="-un"):
            loginstatus.push(2, "Please enter a Username")
            spinner.stop()
            usernameob.set_can_focus(True)
            passwordob.set_can_focus(True)
            return
        elif(loginresponse=="-pw"):
            loginstatus.push(3, "Please enter a Password")
            spinner.stop()
            usernameob.set_can_focus(True)
            passwordob.set_can_focus(True)
            return
instance = PyMCWindow()

