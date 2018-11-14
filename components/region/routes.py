from flask import Blueprint
from flask import render_template

region = Blueprint("region",__name__,template_folder='templates')
@region.route('/region')
def region_main():
	return render_template('region.html')