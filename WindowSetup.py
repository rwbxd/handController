from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pywinauto import application
from pywinauto import findwindows
import psutil

def get_application_path():
    Tk().withdraw() # Hide frame
    filename = askopenfilename(title="Select the .exe for your game")
    # This brings up the Windows file selection prompt and records
    # the path to the file in the variable filename, which we then return
    return filename

def get_application(gamepath=""):
    if gamepath == "": gamepath = get_application_path()
    # this is mainly for debugging, the function will generally get called with
    # no known path, so get_application()
    try:
        app = application.Application().connect(path=gamepath)
        # connect to already running instance
    except:
        app = application.Application().start(gamepath)
        # start game that isn't already running


    # we can't use the filepath to send keyboard inputs to the window, so we
    # have to find the window
    for i in range(100):
        for pid in psutil.pids(): # check all running processes
            try:
                if psutil.Process(pid).exe().replace("\\", "") == gamepath.replace("/", ""):
                    # if the process originated from our selected file
                    windowName = findwindows.find_element(process=pid).name
                    return app[windowName]
                    # return the object we send keyboard inputs to
            except:
                pass


    # if you don't get it here, you don't get it at all
