from flask import Blueprint
from flask import render_template
evestatic = __import__('%s.evestatic.evestatic'%(__name__.split(".")[0]))
import json
import pkg_resources
region = Blueprint("region",__name__,template_folder='templates')

@region.app_template_filter()
def getSysSecurityColor(value):
    return "w3-text-green" if float(value)>0.40 else "w3-text-orange"
@region.app_template_filter()
def getM3Color(value):
    return "w3-text-red" if int(value[:-1]) > 60 else "w3-text-orange" if  int(value[:-1]) > 10 else "w3-text-green"
	
def parse_stuff():
	sd = evestatic.get_evestatic()
	ret = []
	for region_name in evestatic.getAllRegionNames():
		data = json.load(open(pkg_resources.resource_filename(__name__,"static/local_dumps/%s_orders.json"%region_name.replace(" ",""))))
		for d in data:
			system = sd.getSystem(d["system"])
			earnperdst = d["earn"] if d["m3"]* d["volumetotal"] < 60000 else d["earnperm3"] * 60000
			earnperjf = d["earn"] if d["m3"]* d["volumetotal"] < 300000 else d["earnperm3"] * 300000
			investment = d["price"] * d["volumetotal"]
			ret.append({
				"region_name" : region_name,
				"sys_name": system["name"],
				"sys_security": "%.2f"%system["security"],
				"jumps": d["jumps"],
				"item":  sd.getItem(d["item"])["name"],
				"m3_total" : "%dk"%(d["m3"]* d["volumetotal"]/1000),
				"DST" : "%.2f"%(earnperdst/1000000),
				"JF"  : "%.2f"%(earnperjf/1000000),
				"inv"  : "%.2f"%(investment/1000000),
				"price"  : d["price"],
				"return_percent"  : "%d" % (d["earn"]*100/investment),
				"volume_total": d["volumetotal"],
				})
		#print "\tDST: %.2f JF:%.2f Inv: %.2f RetDST: %d RetJF: %d (%d)"%(
		#	,, investment/1000000,
		#	earnperdst*100/investment,earnperjf*100/investment,(earnperjf-155000000)*100/investment)
		#print "\tprice:", d["price"], "volumetotal:", d["volumetotal"]
	
	return sorted(filter(lambda x: float(x["JF"])>155 or float(x["DST"])>x["jumps"]*2,ret), key = lambda x: x["sys_name"] )
@region.route('/region')
def region_main():
	evestatic.get_evestatic()
	return render_template('region.html',order_table=parse_stuff())