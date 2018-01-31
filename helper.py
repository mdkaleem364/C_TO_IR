from c_ast import *

# returns list of distict elements
def getDistinctIds(idsList):

	s = set()
	res = []
	for id in idsList:
		if id not in s:
			res.append(id)
			s.add(id)
	return res


def getIdFromUnaryOp(UnaryObj):
	return getIdsFromObject(UnaryObj.children()[0][1])
	

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

	else:
		res = []
		for i in obj:
			res += getIdsFromObject(i)
		resultList = res

	return getDistinctIds(resultList)
	pass

