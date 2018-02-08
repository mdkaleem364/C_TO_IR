import sys

inpFile = []
outFile = []

with open(sys.argv[1], 'r') as f:
	contentList = f.readlines()
	for line in contentList:
		inpFile.append(line.strip('\n'))

	f.close()

lastInvar = False

for line in inpFile:
	if lastInvar == True and line.strip() == 'invar':
		pass
	elif line.strip() == 'invar':
		outFile.append(line)
		lastInvar = True
	else:
		outFile.append(line)
		lastInvar = False
		pass

for line in outFile:
	print(line)