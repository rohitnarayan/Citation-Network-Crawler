from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt

client = MongoClient('mongodb://localhost:27017/')
db = client.citationDataset

collection = db.db2

peeps = collection.find()
length = peeps.count()
# peeps2 = peeps

G = nx.DiGraph()

# print peeps2[0]

for record in xrange(length):
	authors = peeps[record]['author']
	parent_citors = peeps[record]['citations']
	if len(parent_citors) !=0:
		for parentId,parent in authors.iteritems():
			for child in parent_citors:
				child_authors = peeps[child]['author']
				for child_author_id,author_name in child_authors.iteritems():
					G.add_edge(int(parentId),int(child_author_id))
					print int(parentId),int(child_author_id)
					print nx.info(G)



print nx.info(G)
nx.write_pajek(G,"authorAuthorNetwork.net")