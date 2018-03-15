from pymongo import MongoClient
with open('outputacm.txt') as f:
	f_contents = f.readlines()

paperId = []
paperTitle = []
authors = []
year = []
citations={}
domain = []

soft = ["acm transactions on software engineering and methodology","asia pacific software engineering conference","component based software engineering","european conference on object oriented programming","fase","ieee software","ieee transactions on software engineering","international conference on automated software engineering","international conference on software engineering","international conference on software testing and analysis","international symposium on software reliability engineering","international symposium on the foundations of software","journal of systems and software","knowledge based software engineering conference","object oriented programming systems language and applications","working conference on software architecture"]

os = ["asid","asplos","computational logic","eurosys","hotpower","operating system review","osdi","soap","sysml","usenix annual technical conference","usenix microkernels and other","usenix summer","usenix winter","workshop on hot topics in operating systems"]

database = ["computer architecture","damap","database business","dbtest","ecml","ecml pkdd","edbt","erow","ewsl","icdb","icdm","icdt","icml","kdd","kdd workshop","kdd workshop cyber","kdd workshop human","kdd workshop knowledge","kdd workshop visual","large scale","mcd","nnp","pais","pinkdd","pkdd","sdm","sigfidet workshop","sigmod record","snakdd","ssps","webkdd","wsdm","software engineering for tailor made data management"]

ai = ["aaai","adaption learning","adaptive agents","agent modeling","ai magazine","aisb","alife","applied artificial","artificial life","autonomous agents","cognitive science","computational intelligence","eai","ecai","encyclopedia artificial","executable modal","fuzzy logic","fuzzy logic artificial intelligence","icml","icra","ictai","ieee expert","ieee intelligent systems","ieee transactions robotics","ijcai","intelligent information integration","itwp","learning natural language processing","machine learning","nesy","robotics autonomous systems","uai"]

networking = ["ieee transactions on wireless communications","ieee/acm transactions on networking","ieee transactions on mobile computing","ieee transactions on communications","computer networks","journal of network and computer applications","ieee international conference on communications","computer communications","ad hoc networks","international conference on information processing in sensor networks"]


client = MongoClient('mongodb://localhost:27017/')
db = client.citationDataset

iterator = 0
found = 0
authorId=0

for i in xrange(len(f_contents)):

	line = f_contents[i]

	if line.startswith("#*"):
		paper_name = line[2:].strip()

		if found == 0:
			for j in os:
				if j in paper_name:
					# file.write(paper_name+" was found in OS\n")
					domain.append("Operating System")
					found=1
					break

		if found == 0:
			for j in soft:
				if j in paper_name:
					# file.write(paper_name+" was found in Software Engineering\n")
					domain.append("Software Engineering")
					found=1
					break

		if found == 0:
			for j in database:
				if j in paper_name:
					# file.write(paper_name+" was found in DBMS\n")
					domain.append("Database Management Systems")
					found=1
					break
		if found == 0:
			for j in ai:
				if j in paper_name:
					# file.write(paper_name+" was found in AI\n")
					domain.append("Artificial Intelligence")
					found=1
					break

		if found == 0:
			for j in networking:
				if j in paper_name:
					# file.write(paper_name+" was found in networking\n")
					domain.append("Networking")
					found=1
					break
		if found == 1:
			paperTitle.append(paper_name)
	if found == 1:
		if line.startswith("#index"):
			paperId.append(int(line[6:]))
			found=0
			if f_contents[i+1].startswith("#%"):
				j=1
				citor = []
				citor.append(int(f_contents[i+j][2:]))
				while f_contents[i+j].startswith("#%") and f_contents[i+j+1].startswith("#%"):
					citor.append(int(f_contents[i+j+1][2:]))
					j+=1
				citations[paperId[-1]] = citor

		if line.startswith("#@"):
			listAuthors = line[2:].strip().split(",")
			# listAuthors_with_id=[]
			author_dict={}
			for author_name in listAuthors:
				author_dict[str(authorId)]=author_name
				authorId+=1
			authors.append(author_dict)

		if line.startswith("#t"):
			year.append(int(line[2:]))

	iterator += 1

objects = {}

# print citations
# print paperTitle
# print paperId
# print domain

for i in xrange(len(paperId)):
	if i in citations:
		paper = {
			"paperId" : paperId[i],
			"paper" : paperTitle[i],
			"domain" : domain[i],
			"author" : authors[i],
			"year" : year[i],
			"citations" : citations[i]
		}
	else:
		paper = {
			"paperId" : paperId[i],
			"paper" : paperTitle[i],
			"domain" : domain[i],
			"author" : authors[i],
			"year" : year[i],
			"citations" : []
		}
	objects[i] = paper

# print len(objects)
print objects[151]
print objects[160]
# print objects[2020]
# print objects[2362]
# print objects[1089]
# print objects[2040]
# print objects[1000]
# print objects[3700]


# first create a collection named 'dataset'
# i=0
for key,value in objects.iteritems():
	db.db2.insert(value)
	# i+=1
# 	# if i == 10:
# 	# 	break

# print objects[0]
# print objects[628134]
print objects[205]
print objects[690]

'''
#* --- paperTitle
#@ --- Authors
#t ---- Year
#c  --- publication venue
#index 00---- index id of this paper
#% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
#! --- Abstract
'''