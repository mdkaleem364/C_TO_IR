from c_ast import *


def getIdFromUnaryOp(UnaryObj):
	return UnaryObj.children()[0][1].getName()


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

	return list(set(ret))


def getIDsFromInitList(initListObj):
	ids = []
	for obj in initListObj.children():
		ids += getIdsFromObject(obj[1])
		
	return list(set(ids))


# get list of vars inside any obj
def getIdsFromObject(obj):

	if type(obj) is ID:
		return [obj.getName()]
	
	elif type(obj) is BinaryOp:
		return list(set(getIDsFromBinaryOp(obj)))
	
	# elif type(obj) is UnaryOp:
	# 	return getIdFromUnaryOp(obj)
	# 	pass

	elif type(obj) is ArrayRef:
		return list(set( getIdsFromObject(obj.getId())+getIdsFromObject(obj.getSubscript()) ))

	elif type(obj) is ExprList:
		ids = []
		for expr in obj:
			ids += getIdsFromObject(expr)
		return list(set(ids))

	# constant
	elif type(obj) is Constant:
		return []

	else:
		res = []
		for i in obj:
			res += getIdsFromObject(i)
		return list(set(res))
	pass

