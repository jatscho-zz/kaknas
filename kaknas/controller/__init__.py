from flask import current_app as app

def index():
    return app.send_static_file('index.html')
