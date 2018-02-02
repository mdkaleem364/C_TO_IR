inpFile = []

with open('out','r') as f:
	temp = f.readlines()

	for line in temp:
		inpFile.append(line.strip('\n'))

	f.close()



def getLoopEndLineNo(ind):

	startInd = ind
	innerLines = 0
	
	while( ind<len(inpFile) and inpFile[ind] not in ['endFor', 'endWhile']):
		if inpFile[ind].split()[0] in ['loop']:
			# get last line of inner loop
			endLine = getLoopEndLineNo(ind+1)			
			
			# remove inner loops size
			innerLines += endLine - ind
			
			
			ind = endLine + 1	
		else:
			ind += 1

	# update inner loop 'line'
	inpFile[startInd-1] += str(ind-startInd-innerLines)

	return ind

lineNo = 0
ret = getLoopEndLineNo(0)

print(inpFile)