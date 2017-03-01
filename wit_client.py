from wit import Wit

def send(request, response):
	import pdb
	pdb.set_trace()
	print(response)

def getScore(request):
	import pdb
	pdb.set_trace()
	print(request)


actions = {
	'send' : send,
	'getScore' : getScore
}	

client = Wit(access_token='REPASDYTEYYSAPQ5477TGMP7VZ2KHDRX', actions=actions)

response = client.message('Chelsea score')
print(response)

#response = client.converse('sessionid1', 'Manchester United score', {})
#print(response)

