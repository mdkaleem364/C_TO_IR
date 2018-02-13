from c_ast import *


# handles [b, [a,i], .. ] ids list
def handleGenericList(l):
	for i in l:
		if type(i) is list:
			for j in i:
				print(j, end=' ')
		else:
			print(i, end=' ')
	pass


def handlePrintf(printfObj):

	# no vars is printed in printf
	if len(printfObj.children()[1][1].children()) < 2:
		print("invar")

	else:
		print("output", end=' ')
		for expr in printfObj.children()[1][1].children():
			
			ids = getIdsFromObject(expr[1])
			for id in ids:
				print(id, end=' ')

		print()
	pass


def handleScanf(scanfObj):
	print('input', end=' ')
	for expr in scanfObj.children()[1][1].children():
		if type(expr[1]) is UnaryOp:
			ids = getIdsFromObject(expr[1])
			for id in ids:
				print(id, end=' ')
			print()
	
	pass

# printf, scanf, anyother fn call
def handleFunctionCalls(leftNodes, fnCallObj, callType):
	global dollarCounter
	currCounter=dollarCounter
	dollarCounter += 1

	if fnCallObj.children()[0][1].getName() == 'scanf':
		handleScanf(fnCallObj)

	elif fnCallObj.children()[0][1].getName() == 'printf':
		handlePrintf(fnCallObj)

	# for all other fns
	else:

		# recurse on fns, if any, inside args
		if len(fnCallObj.children()) > 1:
			ids = getIdsFromObject(fnCallObj.children()[1][1])

		print(callType, fnCallObj.children()[0][1].getName(), end=' ')			
		
		# Eg.. int a=max(a,b); 
		if len(leftNodes) > 0:
			# print left assignment val
			# 'a'
			if len(leftNodes) > 0:
				handleGenericList(leftNodes)
				# for node in leftNodes:
				# 	print(node, end=' ')
			else:
				print('$'+str(currCounter), end=' ')

			# check if fn has args
			if len(fnCallObj.children()) > 1:
				for id in ids:
					print(id, end=' ')
			print()

		# Eg.. noReturnFn(a,b,c);
		else:
			# check if fn has args
			if len(fnCallObj.children()) > 1:
				for id in ids:
					print(id, end=' ')
			print()			
		
	return currCounter


# returns list of distict elements
def getDistinctIds(idsList):

	s = set()
	res = []
	for id in idsList:
		if id not in s:
			res.append(id)
			s.add(id)

	return res


def getIdFromUnaryOp(unaryObj):
	return getIdsFromObject(unaryObj.children()[0][1])
	

def getIDsFromInitList(initListObj):
	ids = []
	for obj in initListObj.children():
		ids += getIdsFromObject(obj[1])
		
	return getDistinctIds(ids)


dollarCounter = 1	# global var

# get list of vars inside any obj
def getIdsFromObject(obj):

	resultList = []
	if type(obj) is ID:
		resultList = [obj.getName()]
	
	# elif type(obj) is BinaryOp:
	# 	resultList = getIDsFromBinaryOp(obj) 	# deleted fns
	
	# elif type(obj) is UnaryOp:
	# 	return getIdFromUnaryOp(obj)
	# 	pass

	elif type(obj) is ArrayRef:
		resultList =  getIdsFromObject(obj.getId())+getIdsFromObject(obj.getSubscript())

	elif type(obj) is ExprList:
		ids = []
		for expr in obj:
			ids += getIdsFromObject(expr)
		resultList = ids

	# constant
	elif type(obj) is Constant:
		resultList =  []

	elif type(obj) is InitList:
		resultList = getIDsFromInitList(obj)

	elif type(obj) is TypeDecl:		
		resultList = [obj.getName()]

	elif type(obj) is FuncCall:
		resultList = ['$'+str(handleFunctionCalls(['$'+str(dollarCounter)], obj, 'rcall'))]

	else:
		res = []
		for i in obj:
			res += getIdsFromObject(i)
		resultList = res

	return getDistinctIds(resultList)

