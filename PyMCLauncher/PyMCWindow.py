from gi.repository import Gtk
import PyMCLibs
import json

class PyMCWindow():
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("PYMC Launcher.glade")
        self.window = self.builder.get_object("pymclauncher")
        self.window.show_all()
        self.libsInst = PyMCLibs.PyMCLibs()
        self.handlerdict = {
            "on_pymclauncher_destroy" : Gtk.main_quit,
            "on_login_clicked" : self.onLoginClicked,
            "on_setting_clicked": self.onSettingClicked,
            "on_setsapply_clicked": self.onSetsApplyClicked,
            "on_setscancel_clicked": self.onSetsCancelClicked,
            "on_relorsnap_changed": self.onRelOrSnapChanged
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
        self.username = self.usernameob.get_text() #Gets username to be used throughout
        self.password = self.passwordob.get_text() #Gets password to be used during login
        self.UUID = self.libsInst.getUUID(self.username) #Gets UUID to be used during login
        if(self.UUID=="-inet"):
            self.loginstatus.push(4, "No internet connection")
            self.spinner.stop()
            self.usernameob.set_can_focus(True)
            self.passwordob.set_can_focus(True)
            return
        elif(self.UUID=="wun"):
            self.loginstatus.push(8, "Non-existant username")
            self.spinner.stop()
            self.usernameob.set_can_focus(True)
            self.passwordob.set_can_focus(True)
            return
        self.version = self.libsInst.getVersion() #Gets version to use during files/launch
        retval = self.libsInst.getFiles(self.version) #Gets/ensures files for current version exist
        if(retval=="nof"):
            self.loginstatus.push(9, "No internet & No offline files")
            self.spinner.stop()
            self.usernameob.set_can_focus(True)
            self.passwordob.set_can_focus(True)
            return
        
        loginresponse = self.libsInst.login(self.username, self.password)
        if(loginresponse=="-un&pw"):
            self.loginstatus.push(1, "Please enter a Username and Password")
            self.spinner.stop()
            self.usernameob.set_can_focus(True)
            self.passwordob.set_can_focus(True)
            return
        elif(loginresponse=="-un"):
            self.loginstatus.push(2, "Please enter a Username")
            self.spinner.stop()
            self.usernameob.set_can_focus(True)
            self.passwordob.set_can_focus(True)
            return
        elif(loginresponse=="-pw"):
            self.loginstatus.push(3, "Please enter a Password")
            self.spinner.stop()
            self.usernameob.set_can_focus(True)
            self.passwordob.set_can_focus(True)
            return
        elif(loginresponse=="-inet"):
            self.loginstatus.push(4, "No internet connection")
            self.spinner.stop()
            self.usernameob.set_can_focus(True)
            self.passwordob.set_can_focus(True)
            return
        elif(loginresponse=="wun"):
            self.loginstatus.push(5, "Incorrect username/password")
            self.spinner.stop()
            self.usernameob.set_can_focus(True)
            self.passwordob.set_can_focus(True)
            return
        elif(loginresponse[:15]=='{"accessToken":'):
            self.loginstatus.push(6, "Successful login, launching")
            self.spinner.stop()
            self.usernameob.set_can_focus(True)
            self.passwordob.set_can_focus(True)
            retDict = json.loads(loginresponse)
            self.libsInst.launch(self.username, self.version, self.UUID, retDict["accessToken"])
        else:
            self.loginstatus.push(7, "An unknown error has occured, please contact a developer with this code: "+loginstatus)
            self.spinner.stop()
            self.usernameob.set_can_focus(True)
            self.passwordob.set_can_focus(True)
            return
    def onSettingClicked(self, uselessarg):
        self.setWin = self.builder.get_object("settings")
        self.setWin.show_all()
        self.relorsnap = self.builder.get_object("relorsnap")
    def onSetsApplyClicked(self, uselessarg):
        pass
    def onSetsCancelClicked(self, uselessarg):
        self.setWin.hide()
    def onRelOrSnapChanged(self, uselessarg):
        text = self.relorsnap.get_active_text()
        print(text)
instance = PyMCWindow()

