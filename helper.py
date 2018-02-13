from c_ast import *


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
def handleFunctionCalls(fnCallObj):
	if fnCallObj.children()[0][1].getName() == 'scanf':
		handleScanf(fnCallObj)

	elif fnCallObj.children()[0][1].getName() == 'printf':
		handlePrintf(fnCallObj)

	else:
		print('call', end=' ')
		
	pass


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
	

# returns all variable names from the quation binaryOpObj
def getIDsFromBinaryOp(binaryOpObj):
	ret = []
	for i in binaryOpObj:
		if type(i) is ID:
			ret.append(i.getName())
		elif type(i) is UnaryOp:
			ret.extend(getIdFromUnaryOp(i))
		elif type(i) is BinaryOp:
			ret.extend(getIDsFromBinaryOp(i))
		elif type(i) is ArrayRef:
			ret.extend(getIdsFromObject(i))

	return getDistinctIds(ret)


def getIDsFromInitList(initListObj):
	ids = []
	for obj in initListObj.children():
		ids += getIdsFromObject(obj[1])
		
	return getDistinctIds(ids)


dollarCounter = 0	# global var

# get list of vars inside any obj
def getIdsFromObject(obj):

	resultList = []
	if type(obj) is ID:
		resultList = [obj.getName()]
	
	elif type(obj) is BinaryOp:
		resultList = getIDsFromBinaryOp(obj)
	
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
		resultList = []

	else:
		res = []
		for i in obj:
			res += getIdsFromObject(i)
		resultList = res

	return getDistinctIds(resultList)

