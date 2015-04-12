from gi.repository import Gtk
import urllib.request
import json
import platform
import os
def __init__():
    settingsnonjson = open("settings.json").read()
    settings = json.loads(settingsnonjson)
    home = os.path.expanduser("~")
    assetdir = home+"/.minecraft/assets"
    if platform.system() == "Linux":
        nativestr = "linux"
    elif platform.system() == "Windows":
        nativestr = "windows"
    elif platform.system() == "Darwin":
        nativestr = "osx"
    settingsbranch = settings["branch"]
def login(username, password):
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
        oginstatus.push(6, "Unable to connect to UUID API. Please check your connection")
    except ValueError:
        return("wun")
    except AttributeError:
        pass
    uuid = uuidlib["id"]
    return(uuid)
        
def getVersion():
    try:
        versionsurl = "http://s3.amazonaws.com/Minecraft.Download/versions/versions.json"
        versionsreq = urllib.request.Request(versionsurl)
        versionsby = urllib.request.urlopen(versionsreq).read()
        versionsnonjson = versionsby.decode("utf-8")
        versions = json.loads(versionsnonjson)
        versionsnum = versions["latest"]
        with open(home+"/.minecraft/versions.json") as versionsjson:
            versionsf.write(versionsnonjson)
    except urllib.error.URLError:
        if os.path.isfile(home+"/.minecraft/versions.json"):
            with open(home+"/.minecraft/versions.json") as versionsjsonoffline:
                versionsoffline = json.loads(versionsjsonoffline)
                versionsnum = versionsoffline["latest"]
        else:
            return "4" #Return an error - No internet and no offline file for versions.
def getFiles():
    if settingsbranch=="release":
            version = versionsnum["release"]
    elif settingsbranch=="snapshot":
            version = versionsnum["snapshot"]
            
    if not os.path.isdir(home+"/.minecraft/versions"):
        os.makedirs(home+"/.minecraft/versions")
        
    if not os.path.isdir(home+"/.minecraft/versions/"+version):
        os.mkdir(home+"/.minecraft/versions/"+version)
        
    if not os.path.isfile(home+"/.minecraft/versions/"+sversion+"/"+version+".jar"):
        filejarurl = "http://s3.amazonaws.com/Minecraft.Download/versions/"+self.version+"/"+self.version+".jar"
        filejarreq = urllib.request.Request(filejarurl)
        with open(home+"/.minecraft/versions/"+version+"/"+version+".jar", "wb") as jar:
            jar.write(urllib.request.urlopen(filejarreq).read())
            
    if not os.path.isfile(home+"/.minecraft/versions/"+version+"/"+version+".json"):
        filejsonurl = "http://s3.amazonaws.com/Minecraft.Download/versions/"+self.version+"/"+self.version+".json"
        filejsonreq = urllib.request.Request(filejsonurl)            
        with open(home+"/.minecraft/versions/"+version+"/"+version+".json", "w") as fjson:
            fjson.write(urllib.request.urlopen(filejsonreq).read().decode("utf-8"))
            
    if not os.path.isdir(home+"/.minecraft/assets"):
        os.mkdir(home+"/.minecraft/assets")
    with open(home+"/.minecraft/versions/"+version+"/"+version+".json") as dljson:
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
                    dlfullpath = dlnearfullpath+"/"+dlsplititem[-2]+"-"+dlsplititem[-1]+"-"+nat[nativestr]+".jar"  
            if not os.path.isdir(assetdir+"/"+dlnearfullpath):
                os.makedirs(assetdir+"/"+dlnearfullpath)
            dlfurl = "https://libraries.minecraft.net/"+dlfullpath
            print(dlfurl)
            dlfreq = urllib.request.Request(dlfurl)
            if not os.path.isfile(assetdir+"/"+dlfullpath):
                with open(assetdir+"/"+dlfullpath, "wb") as dlfile:
                    write(urllib.request.urlopen(dlfreq).read())
                

def launch(username, version, uuid, accesstoken):
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
