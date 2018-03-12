from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt

client = MongoClient('mongodb://localhost:27017/')
db = client.citationDataset

paperNetwork = db['dataset']

peeps = paperNetwork.find()

G = nx.DiGraph()

for i in peeps:
	for j in i['citations']:
		G.add_edge(int(i['paperId']),int(j))

print nx.info(G)
nx.write_pajek(G,"paperPaperNetwork.net")
# nx.draw(G,with_labels=True)
# plt.show()