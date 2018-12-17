from flask import Blueprint
from flask import render_template
print '%s.evestatic.evestatic'%(__name__.split(".")[0])
import importlib
evestatic = importlib.import_module('%s.evestatic.evestatic'%(__name__.split(".")[0]))
import json
import pkg_resources

from flask import current_app as app
import datetime

region = Blueprint("region",__name__,template_folder='templates', static_url_path="web/components/region/static")

@region.app_template_filter()
def getSysSecurityColor(value):
    return "w3-text-green" if float(value)>0.40 else "w3-text-orange"
@region.app_template_filter()
def getM3Color(value):
    return "w3-text-red" if int(value[:-1]) > 60 else "w3-text-orange" if  int(value[:-1]) > 10 else "w3-text-green"

def getBestM3():
	sd = evestatic.get_evestatic()
	ret = []
	data = json.load(open(app.config["BASE_DIR"] + "/dumps/regional_trading.json"))
	systems = list(set(map( lambda d: d["system"],data)))
	for system in systems:
		system_deals = sorted(filter(lambda d: d["system"] == system, data), key=lambda d: d["earnperm3"],reverse=True )
		left_dst = 60000
		earn_dst = 0
		for system_deal in system_deals:
			earn_dst = earn_dst + system_deal["earn"] if system_deal["m3"]* system_deal["volumetotal"] < left_dst else system_deal["earnperm3"] * left_dst
			left_dst = left_dst - system_deal["m3"]* system_deal["volumetotal"]
			if(left_dst <= 0):
				break
		ret.append([sd.getSystem(system_deal["system"])["name"],system_deal["jumps"], earn_dst/1000000, earn_dst/system_deal["jumps"]/1000000])
	return ret
def parse_stuff():
	sd = evestatic.get_evestatic()
	ret = []
	data = json.load(open(app.config["BASE_DIR"] + "/dumps/regional_trading.json"))
	print datetime.datetime.now().time(),"Loaded File...", len(data)
	for d in data:
		system = sd.getSystem(d["system"])
		earnperdst = d["earn"] if d["m3"]* d["volumetotal"] < 60000 else d["earnperm3"] * 60000
		earnperjf = d["earn"] if d["m3"]* d["volumetotal"] < 300000 else d["earnperm3"] * 300000
		investment = d["price"] * d["volumetotal"]
		ret.append({
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
	print datetime.datetime.now().time(),"Parsed..."
	return sorted(filter(lambda x: float(x["JF"])>155 or float(x["DST"])>x["jumps"]*0.5,ret), key = lambda x: x["sys_name"] )
@region.route("/region_summary")
def region_summary():
	return render_template('region_summary.html',order_table=sorted(getBestM3(),key= lambda x: x[3], reverse=True))
@region.route('/region')
def region_main():
	return render_template('region.html',order_table=parse_stuff())