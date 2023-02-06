#! /bin/python
# from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

from flask_wtf import FlaskForm
from flask import Blueprint, send_from_directory

# from .config import app, db
from src.config import *
from src.models import *
# from .routing.route import *
from src.router import *

from src.handlers.views import *
import os

port = os.environ.get("PORT") if os.environ.get("PORT") else PORT


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'home/static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')


# from apscheduler.schedulers.background import BackgroundScheduler
# import time
# import atexit

# def print_date_time(a):
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


# scheduler = BackgroundScheduler()
# # scheduler.add_job(func=print_date_time, trigger="interval", seconds=5)
# scheduler.add_job(func=print_date_time, trigger="date", run_date=, args=["a"])
# scheduler.start()



if __name__ == '__main__':
    
    app.run(debug=False, use_reloader=True, port=port, host="0.0.0.0")