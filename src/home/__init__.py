from flask import Blueprint, url_for
from src.config import app

home = Blueprint('home', __name__, template_folder='templates', 
		static_folder="static", 
		static_url_path="/home/static")

from . import router