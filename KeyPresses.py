def sendKey(app, key):
    app.type_keys(key)
    # app is the object of the window

def holdDown(app, key):
    sendKey(app, "{" + key + " down}")
    print("Pressing down " + key)

def letUp(app, key):
    sendKey(app, "{" + key + " up}")
    print("Letting up on " + key)
