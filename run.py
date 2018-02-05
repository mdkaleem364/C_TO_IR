inpFile = []

with open('out','r') as f:
	temp = f.readlines()

	for line in temp:
		inpFile.append(line.strip('\n'))

	f.close()



def getLoopEndLineNo(ind):

	startInd = ind
	innerLines = 0
	
	while( ind<len(inpFile) and inpFile[ind] not in ['endFor', 'endWhile','endIf','endElse']):
		if inpFile[ind].split()[0] in ['loop','if','else','elseif']:
			# get last line of inner loop
			endLine = getLoopEndLineNo(ind+1)			
			
			# remove inner loops size
			innerLines += endLine - ind
			if endLine+1<len(inpFile) and inpFile[endLine+1].split()[0] in ['else','elseif']:
				innerLines+=1
			
			ind = endLine + 1	
		else:
			ind += 1

	# update inner loop 'line'
	if ind+1<len(inpFile):
		if  inpFile[ind+1].split()[0] in ['else','elseif']:
			inpFile[startInd-1] += str(ind-startInd-innerLines+1)
		else:
			inpFile[startInd-1] += str(ind-startInd-innerLines)
	elif ind<len(inpFile) and inpFile[ind].split()[0] in ['endFor', 'endWhile','endIf','endElse']:
		inpFile[startInd-1] += str(ind-startInd-innerLines)
	return ind

lineNo = 0
ret = getLoopEndLineNo(0)

for line in inpFile:
	print(line)
