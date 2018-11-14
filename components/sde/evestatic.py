import json
import yaml
import datetime
import os
import re

class FileWrapper:
	def __init__(self,path):
		self.basepath = path
	def getRawFile(self, path):
		try:
			return open(self.basepath+path).read()
		except:
			print "[ERROR] COULD NOT OPEN RAW FILE: %s" % path
	def getYamlFile(self,path):
		try:
			return yaml.load(open(self.basepath+path))
		except:
			print "[ERROR] COULD NOT OPEN YAML FILE: %s" % path
	def getJSONFile(self,path):
		try:
			return json.load(open(self.basepath+path))
		except:
			print "[ERROR] COULD NOT OPEN JSON FILE: %s" % path
	def getTree(self, path):
		return os.listdir(self.basepath+path)
		
class StaticData:
	def __init__(self, path):
		self.fw = FileWrapper(path)
		self.LoadTypeID()
		self.LoadRegionID()
		self.LoadSolarSystems()
	def LoadRegionID(self):
		print "[%s] Loading Region IDs..." % datetime.datetime.now()
		self.regionID = {}
		region_names = self.fw.getTree("/fsd/universe/eve/")
		for region_name in region_names:
			data = self.fw.getRawFile("/fsd/universe/eve/%s/region.staticdata"%region_name)
			match = re.search("regionID: (\d*)", data, flags=re.M|re.S)
			if(match):
				self.regionID[region_name] = int(match.group(1))
			else:
				print "[WARNING] Did not found LoadRegionID match for region %s" % region_name
	def LoadSolarSystems(self):
		print "[%s] Loading System IDs..." % datetime.datetime.now()
		self.systems = {}
		for region_name in self.fw.getTree("/fsd/universe/eve/"):
			for constelation_name in filter(lambda x: "." not in x,self.fw.getTree("/fsd/universe/eve/%s/"%region_name)):
				for system_name in filter(lambda x: "." not in x,self.fw.getTree("/fsd/universe/eve/%s/%s/"%(region_name,constelation_name))):
					data= self.fw.getRawFile("/fsd/universe/eve/%s/%s/%s/solarsystem.staticdata"%(region_name,constelation_name,system_name))

					security_match = re.search("security: (-?\d.\d*)", data, flags=re.M)				
					match = re.search("solarSystemID: (\d*)", data, flags=re.M|re.S)
					if(match and security_match):
						self.systems[int(match.group(1))] = {"name": system_name, "security": float(security_match.group(1))}
					else:
						print "[WARNING] Did not found solarSystemID match for system %s/%s/%s" % (region_name,constelation_name,system_name)
						
						
					
	def LoadTypeID(self):
		print "[%s] Loading TypeIDs" % datetime.datetime.now()
		self.Item = self.fw.getJSONFile("/converted/typeIDs.json")
	def getRegionID(self,region_name):
		return self.regionID[region_name]
	def getItem(self,item_id):
		return self.Item.get(str(item_id),{"name": "Unknown", "volume": -1})
	def getSystem(self, system_id):
		return self.systems.get(int(system_id),"UnknownSystem")