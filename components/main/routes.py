from flask import Blueprint
from flask import render_template

main = Blueprint("main",__name__,template_folder='templates')
@main.route('/')
def dashboard():
	return render_template('dashboard.html')