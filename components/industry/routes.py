from flask import Blueprint
from flask import render_template
from flask import g
#print '%s.evestatic.evestatic'%(__name__.split(".")[0])
import importlib
evestatic = importlib.import_module('%s.evestatic.evestatic'%(__name__.split(".")[0]))
import json
import pkg_resources
industry = Blueprint("industry",__name__,template_folder='templates', static_url_path="web/components/industry/static")

def getJSON_blueprints():
	blueprint_json = getattr(g, '_blueprint', None)
	if blueprint_json is None:
		blueprint_json = g._blueprint = json.load(open(pkg_resources.resource_filename(__name__,"blueprints.json")))#fw.getYamlFile("/fsd/blueprints.yaml")
	return blueprint_json

def get_evestatic():
    evestatic_db = getattr(g, '_evestatic', None)
    if evestatic_db is None:
        evestatic_db = g._evestatic = StaticData()
    return evestatic_db
def calc_compression(item_id):
	sd = evestatic.get_evestatic()
	data = getJSON_blueprints()
	compressable_items = ["Tritanium",'Pyerite','Mexallon','Isogen','Nocxium','Zydrine','Megacyte']
	sum_func = lambda items: sum( map( lambda item: sd.getItem(item["typeID"])["volume"] * item['quantity'], items))
	m3_materials = sum_func(filter(lambda item:sd.getItem(item["typeID"])["name"] in compressable_items ,data[str(item_id)]["activities"]['manufacturing']["materials"]))
	m3_products =sum_func(data[str(item_id)]["activities"]['manufacturing']["products"])
	return [sd.getItem(item_id)["name"], m3_materials/m3_products]

@industry.route('/indy_test')
def region_main():
	a = getJSON_blueprints()
	table = map(lambda b_id: calc_compression(b_id), filter(lambda b_id: "manufacturing" in a[b_id]["activities"] and "products" in a[b_id]["activities"]["manufacturing"] and "materials" in a[b_id]["activities"]["manufacturing"] ,a))
	return render_template('indy_test.html', my_table = sorted(table,key=lambda x:x[1],reverse=True))