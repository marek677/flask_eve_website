import json
from cachetools import cached, TTLCache
import time

JumpCache = TTLCache(maxsize=100, ttl=300)

class JumpFinder:
	def __init__(self):
		self.star_roadmap = json.load(open("roadmap.json"))
		for a in self.star_roadmap:
			self.star_roadmap[a] = map(lambda x: x[0],self.star_roadmap[a])
	@cached(JumpCache)
	def FindRoute(self,source,dest):
		source = str(source)
		dest = str(dest)
		jumps = 1
		try:
			old_stargates = self.star_roadmap[source]
			visited = []
			while(jumps<100):
				new_stargates = []
				visited = visited + old_stargates
				if dest in old_stargates:
					return jumps
				for s in old_stargates:
					new_stargates = new_stargates + filter(lambda x: x not in visited,self.star_roadmap[s])
				old_stargates = new_stargates
				jumps = jumps+1
		except:
			print "[ERROR] JUMP FINDER ERROR :("
		return -1

def unit_test():		
	jf = JumpFinder()
	source = "30004280"
	dest = "30000142"
	start = time.time()
	for i in xrange(1000):
		 jf.FindRoute(source,dest)	
	end = time.time()
	print(end - start)
	print jf.FindRoute(source,dest)	

if __name__ == "__main__":
	unit_test()