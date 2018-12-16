from flask import Blueprint
from flask import render_template
from flask import g
#print '%s.evestatic.evestatic'%(__name__.split(".")[0])
import importlib
evestatic = importlib.import_module('%s.evestatic.evestatic'%(__name__.split(".")[0]))
import json
import pkg_resources
import datetime
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
def calc_compression(item_id,sd,minerals,data):
	itemname = sd.getItem(item_id)["name"]
	if not "I" in itemname.split(" ") and "II" not in itemname.split(" "):
		return ["",0]
	compressable_items = ["Tritanium",'Pyerite','Mexallon','Isogen','Nocxium','Zydrine','Megacyte']
	sum_func = lambda items: sum( map( lambda item: minerals.get(item["typeID"],sd.getItem(item["typeID"]))["volume"] * item['quantity'], items))
	m3_materials = sum_func(filter(lambda item: item["typeID"] in minerals ,data[str(item_id)]["activities"]['manufacturing']["materials"]))
	m3_products =sum_func(data[str(item_id)]["activities"]['manufacturing']["products"])
	return [itemname, m3_materials/m3_products]

@industry.route('/indy_compression')
def indy_compression():
	sd = evestatic.get_evestatic()
	a = getJSON_blueprints()
	ff = filter(lambda b_id: "manufacturing" in a[b_id]["activities"] and "products" in a[b_id]["activities"]["manufacturing"] and "materials" in a[b_id]["activities"]["manufacturing"] ,a)
	temp = {item_id : sd.getItem(item_id) for item_id in [34,35,36,37,38,39,40] }
	table = map(lambda b_id: calc_compression(b_id,sd,temp,a), ff)
	lit_table = sorted(table,key=lambda x:x[1],reverse=True)[:100]
	return render_template('indy_test.html', my_table = lit_table)