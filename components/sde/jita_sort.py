import json

jita_buys = json.load(open("jita_buys.json"))
for item_id in jita_buys:
	jita_buys[item_id] =  sorted(jita_buys[item_id],key=lambda xx : xx["price"], reverse=True)

for item_id in jita_buys:
	print jita_buys[item_id][:3]
	break