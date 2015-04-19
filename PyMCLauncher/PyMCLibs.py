from gi.repository import Gtk
import urllib.request
import json
import platform
import os
class PyMCLibs:
    def __init__(self):
        settingsnonjson = open("settings.json").read()
        settings = json.loads(settingsnonjson)
        self.home = os.path.expanduser("~")
        self.assetdir = self.home+"/.minecraft/assets"
        if platform.system() == "Linux":
            self.nativestr = "linux"
        elif platform.system() == "Windows":
            self.nativestr = "windows"
        elif platform.system() == "Darwin":
            self.nativestr = "osx"
        self.settingsbranch = settings["branch"]
    def login(self,username, password):
        #Halts the login if either box or both are left empty.
        if(username+password==""):
            return "-un&pw"
        elif(username==""):
            return "-un"
        elif(password==""):
            return "-pw"
        
        nonjsondata = {"username": username,"password": password,"clientToken": "foobar"}
        datanonenc = json.dumps(nonjsondata)
        data = datanonenc.encode("utf-8")
        authurl = "https://authserver.mojang.com"
        headers = {"Content-Type" : "application/json"}
        authreq = urllib.request.Request(authurl+"/authenticate", data, headers)
        #Error handling for the Mojang Login request.
        try:
            authopenurl = urllib.request.urlopen(authreq)
            authresponse = authopenurl.read().decode("utf-8")
            print(authresponse)
        except urllib.error.HTTPError as e:
            if(e.code==403):
                loginstatus.push(3, "Incorrect Username/Password (Code 403)")
                spinner.stop()
                usernameob.set_can_focus(True)
                passwordob.set_can_focus(True)
                return
            else:
                loginstatus.push(4, "An unknown error has occured, please post this data on the launcher thread: "+ e)
                spinner.stop()
                usernameob.set_can_focus(True)
                passwordob.set_can_focus(True)
                return
        except urllib.error.URLError:
            loginstatus.push(5, "No internet connection")
            spinner.stop()
            usernameob.set_can_focus(True)
            passwordob.set_can_focus(True)
            return
        #Sets the username & password entry boxes back to an editable mode.
    #    usernameob.set_can_focus(True)
    #    passwordob.set_can_focus(True)
        
    def getUUID(username):
        uuidurl = "https://api.mojang.com/users/profiles/minecraft/"+username
        uuidreq = urllib.request.Request(uuidurl)
        try:
            uuidopenurl = urllib.request.urlopen(uuidreq)
            uuidresp = uuidopenurl.read()
            uuidlibj = uuidresp.decode()
            uuidlib = json.loads(uuidlibj)
        except urllib.error.URLError:
            return("noconn") #Return an error - No internet connection
        except ValueError:
            return("wun") #Return an error - Non-existant username
        except AttributeError:
            pass
        uuid = uuidlib["id"]
        return(uuid) #Success - Returns the UUID requested
            
    def getVersion(self):
        try:
            versionsurl = "http://s3.amazonaws.com/Minecraft.Download/versions/versions.json"
            versionsreq = urllib.request.Request(versionsurl)
            versionsby = urllib.request.urlopen(versionsreq).read()
            versionsnonjson = versionsby.decode("utf-8")
            versions = json.loads(versionsnonjson)
            versionsnum = versions["latest"]
            with open(self.home+"/.minecraft/versions.json", "w+") as versionsjson:
                versionsjson.write(versionsnonjson)
            return(versionsnum)
        except urllib.error.URLError:
            if os.path.isfile(self.home+"/.minecraft/versions.json"):
                with open(self.home+"/.minecraft/versions.json", "w+") as versionsjsonoffline:
                    versionsoffline = json.loads(versionsjsonoffline)
                    versionsnum = versionsoffline["latest"]
                    return(versionsnum)
            else:
                return("nof") #Return an error - No internet and no offline file for versions
    def getFiles(self):
        versionsnum = self.getVersion()
        if(versionsnum=="nof"):
            return("nof")
        else:
            pass
        if self.settingsbranch=="release":
                version = versionsnum["release"]
        elif self.settingsbranch=="snapshot":
                version = versionsnum["snapshot"]
                
        if not os.path.isdir(self.home+"/.minecraft/versions"):
            os.makedirs(self.home+"/.minecraft/versions")
            
        if not os.path.isdir(self.home+"/.minecraft/versions/"+version):
            os.mkdir(self.home+"/.minecraft/versions/"+version)
            
        if not os.path.isfile(self.home+"/.minecraft/versions/"+version+"/"+version+".jar"):
            try:
                filejarurl = "http://s3.amazonaws.com/Minecraft.Download/versions/"+version+"/"+version+".jar"
                filejarreq = urllib.request.Request(filejarurl)
                with open(self.home+"/.minecraft/versions/"+version+"/"+version+".jar", "wb") as jar:
                    jar.write(urllib.request.urlopen(filejarreq).read())
            except urllib.error.URLError:
                return("nof") #Return an error - No internet and no offline file for main JAR
                
        if not os.path.isfile(self.home+"/.minecraft/versions/"+version+"/"+version+".json"):
            try:
                filejsonurl = "http://s3.amazonaws.com/Minecraft.Download/versions/"+version+"/"+version+".json"
                filejsonreq = urllib.request.Request(filejsonurl)            
                with open(self.home+"/.minecraft/versions/"+version+"/"+version+".json", "w") as fjson:
                    fjson.write(urllib.request.urlopen(filejsonreq).read().decode("utf-8"))
            except urllib.error.URLError:
                return("nof") #Return an error - No internet and no offline file for index
                
        if not os.path.isdir(self.home+"/.minecraft/assets"):
            os.mkdir(self.home+"/.minecraft/assets")
        with open(self.home+"/.minecraft/versions/"+version+"/"+version+".json") as dljson:
            dllibsdata = dljson.read()
            dllibsd = json.loads(dllibsdata)
            dllibraries = dllibsd['libraries']
            for item in dllibraries:
                dlsplititem = item['name'].split(":")
                dlsplititem[0] = dlsplititem[0].replace(".", "/")
                dlnearfullpath = "/".join(dlsplititem)

                rul = item.get("rules")
                if not rul:
                    pass
                else:
                    print(rul)
                nat = item.get("natives")
                if not nat:
                        dlfullpath = dlnearfullpath+"/"+dlsplititem[-2]+"-"+dlsplititem[-1]+".jar"
                else:
                        dlfullpath = dlnearfullpath+"/"+dlsplititem[-2]+"-"+dlsplititem[-1]+"-"+nat[self.nativestr]+".jar"  
                if not os.path.isdir(self.assetdir+"/"+dlnearfullpath):
                    os.makedirs(self.assetdir+"/"+dlnearfullpath)
                dlfurl = "https://libraries.minecraft.net/"+dlfullpath
                print(dlfurl)
                dlfreq = urllib.request.Request(dlfurl)
                if not os.path.isfile(self.assetdir+"/"+dlfullpath):
                    with open(self.assetdir+"/"+dlfullpath, "wb") as dlfile:
                        dlfile.write(urllib.request.urlopen(dlfreq).read())
                    

    def launch(self,username, version, uuid, accesstoken):
        f2 = open(home+"/.minecraft/versions/"+version+"/"+version+".json", "r")
        libsdata = f2.read()
        libsd = json.loads(libsdata)
        libraries = libsd['libraries']
        libsl = []
        for item in libraries:
            splititem = item['name'].split(":")
            splititem[0] = splititem[0].replace(".", "/")
            nearfullpath = "/".join(splititem)
            fullpath = home+"/"+nearfullpath+"/"+splititem[-2]+"-"+splititem[-1]+".jar:"
            libsl.append(fullpath)
            libs = "".join(libsl)
        print(libs)
