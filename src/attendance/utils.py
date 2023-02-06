from flask import render_template, redirect, session, url_for, request, flash, render_template_string, json
from src.config import db,  app, lang


def json_response(content, code=200):
	response = app.response_class(
	        response=json.dumps(content),
	        status=code,
	        mimetype='application/json'
	    )
	return response