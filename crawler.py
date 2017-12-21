from pymongo import MongoClient
with open('outputacm.txt') as f:
	f_contents = f.readlines()

paperId = []
paperTitle = []
authors = []
year = []
citations={}

client = MongoClient('mongodb://localhost:27017/')
db = client.citationDataset

iterator = 0

for i in xrange(len(f_contents)):

	line = f_contents[i]

	if line.startswith("#index"):
		paperId.append(int(line[6:]))
		if f_contents[i+1].startswith("#%"):
			j=1
			citor = []
			citor.append(int(f_contents[i+j][2:]))
			while f_contents[i+j].startswith("#%") and f_contents[i+j+1].startswith("#%"):
				citor.append(int(f_contents[i+j+1][2:]))
				j+=1
			citations[paperId[-1]] = citor

	if line.startswith("#*"):
		paperTitle.append(line[2:].strip())

	if line.startswith("#@"):
		listAuthors = line[2:].strip().split(",")
		authors.append(listAuthors)

	if line.startswith("#t"):
		year.append(int(line[2:]))

	iterator += 1

objects = {}

# print citations

for i in xrange(len(paperId)):
	if i in citations:
		paper = {
			"paperId" : paperId[i],
			"paper" : paperTitle[i],
			"author" : authors[i],
			"year" : year[i],
			"citations" : citations[i]
		}
	else:
		paper = {
			"paperId" : paperId[i],
			"paper" : paperTitle[i],
			"author" : authors[i],
			"year" : year[i],
			"citations" : []
		}
	objects[i] = paper

print objects[5]
print objects[6]

#first create a collection named 'dataset'
# i=0
for key,value in objects.iteritems():
	db.dataset.insert(value)
# 	# i+=1
# 	# if i == 10:
# 	# 	break

# print objects[0]
# print objects[628134]
# print objects[5]
# print objects[6]

'''
#* --- paperTitle
#@ --- Authors
#t ---- Year
#c  --- publication venue
#index 00---- index id of this paper
#% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
#! --- Abstract
'''