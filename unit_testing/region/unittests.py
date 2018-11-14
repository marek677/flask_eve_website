from components.sde import evestatic
import datetime
import json


def print_stuff(sd,region_name):
	data = json.load(open("unit_testing/region/local_dumps/%s_orders.json"%region_name))
	for d in data:
		system = sd.getSystem(d["system"])
		earnperdst = d["earn"] if d["m3"]* d["volumetotal"] < 60000 else d["earnperm3"] * 60000
		earnperjf = d["earn"] if d["m3"]* d["volumetotal"] < 300000 else d["earnperm3"] * 300000
		investment = d["price"] * d["volumetotal"]
		print "%.2f"%system["security"],"(%d)"%d["jumps"], system["name"], sd.getItem(d["item"])["name"]
def unit_test():
	print "[%s] Starting Loading components..." % datetime.datetime.now()
	sd = evestatic.StaticData("components/sde/sdefiles")		
	search_regions = [
		"Aridia",
		"Black Rise",
		"Derelik",
		"Devoid",
		"Domain",
		"Essence",
		"Everyshore",
		"Genesis",
		"Heimatar",
		"Kador",
		"Khanid",
		"Kor-Azor",
		"Lonetrek",
		"Metropolis",
		"Molden Heath",
		"Placid",
		"Sinq Laison",
		"Solitude",
		"Tash-Murkon",
		"The Bleak Lands",
		"The Citadel",
		"The Forge",
		"Verge Vendor"
	]
	for region_name in search_regions:
		print_stuff(sd,region_name.replace(" ",""))