from flask import Blueprint, url_for
from src.config import app

# index_page = Blueprint('home', __name__, template_folder='templates', 
# 		static_folder="static", 
# 		static_url_path="/home/static")

# from . import router

participant = Blueprint('participant', __name__, template_folder='templates', 
		static_folder="static", 
		static_url_path="/participant/static")

from . import router