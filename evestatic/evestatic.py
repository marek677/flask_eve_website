import sqlite3
from sqlite3 import Error
import pkg_resources
from flask import g	

def get_evestatic():
    evestatic_db = getattr(g, '_evestatic', None)
    if evestatic_db is None:
        evestatic_db = g._evestatic = StaticData()
    return evestatic_db
	
def close_evestatic():
	evestatic_db = getattr(g, '_evestatic', None)
	if evestatic_db is not None:
		evestatic_db.c.close()
		
class StaticData():
	def __init__(self):
		self.conn = sqlite3.connect(pkg_resources.resource_filename(__name__,"evestatic.db"))
		self.c = self.conn.cursor()
	def getRaw(self, table_name,column_name, val):
		self.c.execute("SELECT * FROM %s WHERE %s=?"%(table_name, column_name), ((val,)))
		rows = self.c.fetchall()
		return rows
	def getRegionID(self,region_name):
		r = self.getRaw("regions","name",region_name)
		if(len(r) == 1):
			return r[0][0]
		else:
			return -1
	def getItem(self,item_id):
		r = self.getRaw("items","id",item_id)
		if(len(r) == 1):
			return {"name": r[0][1], "volume": r[0][2]}
		else:
			return {"name": "Unknown", "volume": -1}
	def getSystem(self, system_id):
		r = self.getRaw("systems","id",system_id)
		if(len(r) == 1):
			return {"name": r[0][1], "security": float(r[0][2])}
		else:
			return {"name": "Unknown", "security": 10.0}
def getAllRegionNames():
	return [
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
if __name__ == "__main__":		
	es = StaticData()
	print es.getRaw("items","id",13829)
	print es.getItem(13829)
	print es.getRaw("regions","name","Aridia")
	print es.getRaw("regions","id",10000054)
	print es.getRegionID("Aridia")
	print es.getRaw("systems","name","Jita")
	print es.getSystem(30000142)