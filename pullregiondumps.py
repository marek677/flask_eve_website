import json
import requests
import os
import re
import yaml
import datetime
from evestatic import evejumps
import time
from evestatic import evestatic	
import threading	
import pkg_resources

class ESI:
	def __init__(self):
		self.s = requests.session()
	def get(self,url):
		r = self.s.get("https://esi.evetech.net/latest/%s"%url)
		#print r.text.encode("utf-8")
		for i in xrange(5):
			try:
				return json.loads(r.text.encode("utf-8"))
			except:
				print "[ERROR] Retry: %i Esi_raw_get_error:\n %s" % (i,r.text.encode("utf-8"))
				time.sleep(10)

class ESIMarket:
	def __init__(self, esi, sd):
		self.esi = esi
		self.sd = sd
	#returns json-object
	def getRawRegionPage(self,region_id, page_id):
		return self.esi.get("markets/%d/orders/?datasource=tranquility&page=%d"%(region_id,page_id))
	def getRegion(self,region_name, start_page = 1):
		print "[%s] Pulling region %s..." % (datetime.datetime.now(), region_name)
		orders = []
		page_id = start_page
		while(True):
			#print "[%s] Pulling page %d for region %s..." % (datetime.datetime.now(),page_id, region_name)
			raw_market_data = self.getRawRegionPage(self.sd.getRegionID(region_name),page_id)
			if raw_market_data == None:
				print "[ERROR] - Did not get the page."
				continue
			if "error" in raw_market_data:
				print "[ERROR] Error on pulling page %d for region %s : %s " %(page_id,region_name,raw_market_data["error"])
				break
			if(raw_market_data == []):
				break
			else:
				for order_raw in raw_market_data:
					order = {
						"item"   	: int(order_raw["type_id"]),
						"price"  	: order_raw["price"],
						"system"	: int(order_raw["system_id"]),
						"isBuy"		: order_raw["is_buy_order"],
						"volumetotal" : order_raw['volume_remain']
					}
					orders.append(order)
			page_id = page_id + 1
		return orders

def PullJitaBuys(em):
	orders_all = em.getRegion("TheForge")
	jita_buy = filter(lambda order: order["isBuy"] == True and order["system"] == 30000142, orders_all)
	map( lambda order: order.update({"m3" : sd.getItem(order["item"])["volume"]})  ,jita_buy)
	#map( lambda order: order.update({"security" : sd.getSystem(order["system"])["security"]})  ,jita_buy)
	jita_buys = {}
	for order in jita_buy:
		#print order
		if order["item"] not in jita_buys:
			jita_buys[order["item"]] = []
		jita_buys[order["item"]].append(order)
	with open('jita_buys.json', 'wb') as outfile:
		json.dump(jita_buys, outfile)
	for x in jita_buys:
		jita_buys[x] = sorted(jita_buys[x],key=lambda xx : xx["price"],reverse=True)
	return jita_buys
def PullRegionOrders(em,region_name, filter_func):
	aridia_sell = em.getRegion(region_name)
	#Adding volume (m3) information later on...
	#map( lambda order: order.update({"volume" : sd.getItem(order["item"])["volume"]})  ,aridia_sell)
	map( lambda order: order.update({"security" : sd.getSystem(order["system"])["security"]})  ,aridia_sell)
	return filter(filter_func, aridia_sell)

def doRegionCalc(region_name):
	aridia_orders = PullRegionOrders(em,region_name,lambda order: order["isBuy"] == False)
	deals = []
	print "[%s] Calculating profit..." % datetime.datetime.now()
	for order in aridia_orders:
		earn = 0
		volume_counter = order['volumetotal']
		if(order["item"] in jita_buys):
			for jita_order in jita_buys[order["item"]]:
				this_transaction_volume = volume_counter if volume_counter <= jita_order['volumetotal'] else jita_order['volumetotal']
				#print "+", this_transaction_volume * (jita_order['price'] - order['price'])
				earn = earn + this_transaction_volume * (jita_order['price'] - order['price'])
				volume_counter = volume_counter - this_transaction_volume
				if(volume_counter <= 0):
					break;
		order.update({"earn": earn})
	aridia_orders = filter(lambda x: x["earn"] > 1000000,aridia_orders) # only earning more than 1m.
	print "[%s] Qualified Order count: %d" % (datetime.datetime.now(),len(aridia_orders))
	#print aridia_orders[0]
	print "[%s] Adding jump information..." % datetime.datetime.now()
	list(map(lambda x: x.update({"jumps": jf.FindRoute(x["system"],30000142)}), aridia_orders))
	list(map(lambda x: x.update({"earnperjump": x["earn"]/x["jumps"]}), aridia_orders))
	#print aridia_orders[0]
	print "[%s] Adding m3 information..." % datetime.datetime.now()
	list(map(lambda x: x.update({"m3": sd.getItem(x["item"])["volume"]}), aridia_orders))
	list(map(lambda x: x.update({"earnperm3": x["earn"]/(x["volumetotal"]*x["m3"])}), aridia_orders))

	#print aridia_orders[0]
	#print jita_buys[list(set(jita_buys))[0]]
	#Adding jump information
	#jumps = jf.FindRoute(order["system"],30000142)
	print "[%s] File dump..." % datetime.datetime.now()
	with open(pkg_resources.resource_filename(__name__,'components/region/static/local_dumps/%s_orders.json'%region_name.replace(" ","_")), 'wb') as outfile:
		json.dump(aridia_orders, outfile)
	print "[%s] Region %s finished..." % (datetime.datetime.now(),region_name)
	
print "[%s] Starting Loading components..." % datetime.datetime.now()
sd = evestatic.StaticData()
esi = ESI()
em = ESIMarket(esi,sd)
jf = evejumps.JumpFinder()
print "[%s] All components Loaded..." % datetime.datetime.now()
jita_buys = PullJitaBuys(em)
for region_name in evestatic.getAllRegionNames():
	doRegionCalc(region_name.replace(" ",""))

print "[%s] All finished..." % datetime.datetime.now()
