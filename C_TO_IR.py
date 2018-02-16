import sys
from c_ast import *
from c_parser import CParser
from helper import *
import helper

"""
for testing print added in 
c_ast.c
	line : 695 and 937

"""

	
# handles 'a=b*d/c*10'
def handleBinaryOp(leftNodes, BinaryOpObj):
	
	ids = getIdsFromObject(BinaryOpObj)
	
	for i in leftNodes:
		print('assign', i, end=" ")
	
		for id in ids:
			print(id, end=" ")
		print()
	pass


# handles 'a=b=c=...'
def handleMultiAssign(leftNodes, assignmentObj):

	leftChild = assignmentObj.children()[0][1]
	rightChild = assignmentObj.children()[1][1]

	if type(leftChild) is ArrayRef:
		leftNodes += [getIdsFromObject(leftChild)]
	else:
		leftNodes += [getIdsFromObject(leftChild)]

	# check for unary ops
	op = assignmentObj.getOperator()
	if op in ['+=', '-=', '*=', '/=', '>>=', '<<=', '%=', '|=', '&=', '^=']:
		leftNodes[-1] += leftNodes[-1]

	# a=b || a+=b
	# a = b[i]
	# a = b*c || a += b*c
	if type(rightChild) in [ID, BinaryOp, ArrayRef]:
		for id in leftNodes:		
			print('assign', end=' ')			
			handleGenericList(id)
			handleGenericList(getIdsFromObject(rightChild))
			print()

	# a=b=c || a+=b=c ?
	elif type(rightChild) is Assignment:
		handleMultiAssign(leftNodes, rightChild)

	# a=10 || a += 5
	elif type(rightChild) is Constant:
		for id in leftNodes:
			print('assign',end=' ')
			handleGenericList(id)
			print()
	
	elif type(rightChild) is FuncCall:
		handleFunctionCalls(leftNodes, rightChild, 'rcall')

	pass


def handleWhileLoops(nodeObj):
	global dollarCounter
	currCounter = dollarCounter

	ids = getIdsFromObject(nodeObj.children()[0][1])
	print('loop', end=' ')
	for id in ids:
		print(id, end=' ')
	print()

	dfs(nodeObj.children()[1][1])
	helper.dollarCounter = currCounter

	# again parse on cond stmts
	getIdsFromObject(nodeObj.children()[0][1])
	print('endWhile')
	pass


def handleIfElse(nodeObj):

	ids = getIdsFromObject(nodeObj.children()[0][1])
	print('if', end=' ')
	for id in ids:
		print(id,end=' ')
	print()
	
	# handle unary ops in if cond
	handlePreUnary(nodeObj.children()[0][1])
	handlePostUnary(nodeObj.children()[0][1])

	# recur on stmts inside 'if' block
	dfs(nodeObj.children()[1][1])
	print('endIf')
	# check if 'else' or 'else if' block exists
	if len(nodeObj.children()) > 2:

		print('else',end='')

		# check if 'else if' stmt
		if type(nodeObj.children()[2][1]) is If:
			handleIfElse(nodeObj.children()[2][1])

		else:
			print()

			# recur on stmts inside 'else' block
			dfs(nodeObj.children()[2][1])		
			print('endElse')
	pass


# return no of lines of initialisation of for loop (if any) inside this obj
def getInnerForLoopLines(obj):

	res = 0
	if type(obj) is Compound:
		for line in obj:
			if type(line) is For and line.children()[0][0] == 'init':
				res += getInnerForLoopLines(line)

	elif type(obj) is For and obj.children()[0][0] == 'init':
		if type(obj.children()[0][1]) is ExprList:
			res += len(obj.children()[0][1].children())
		elif type(obj.children()[0][1]) is not Constant:
			res += 1

	return res


def handleForLoops(forLoopObj):

	ind = 0
	## init - optional
	if forLoopObj.children()[ind][0] == 'init':	
		dfs(forLoopObj.children()[ind][1])
		ind += 1

	## cond - optional
	condIds = []
	# not handled - ( 1||a=b )
	if forLoopObj.children()[ind][0] == 'cond':
		# (can have assignment stmts inside 'cond')
		# for fns inside cond stmts, if any
		dfs(forLoopObj.children()[ind][1])
		currCounter = helper.dollarCounter
		currInd = ind
		condIds = getIdsFromObject(forLoopObj.children()[ind][1])

		ind += 1

	## next - optional
	nextInd = -1
	if forLoopObj.children()[ind][0] == 'next':		
		nextInd = ind
		ind += 1		
	
	print('loop',end=' ')
	for id in condIds:
		print(id, end=' ')
	print()

	#print condition stmts after 'loop' line
	dfs(forLoopObj.children()[currInd][1])
	
	## stmt - Empty/Compound/(Single line)
	dfs(forLoopObj.children()[ind][1])	

	if nextInd != -1:
		dfs(forLoopObj.children()[nextInd][1])		
	

	# for fns inside cond stmts, if any
	helper.dollarCounter = currCounter
	getIdsFromObject(forLoopObj.children()[currInd][1])

	
	print('endFor')


def handleDeclerations(declObj):

	# handle preUnary
	handlePreUnary(declObj)	
	if type(declObj.children()[0][1]) is TypeDecl:

		# int i;
		if len(declObj.children()) == 1:
			print('invar')

		elif type(declObj.children()[1][1]) is Assignment:
			handleMultiAssign([declObj.children()[0][1].getName()], declObj.children()[1][1])

		# int i=5;
		elif type(declObj.children()[1][1]) is Constant:
			print('assign', declObj.children()[0][1].getName())

		# int i=j;
		elif type(declObj.children()[1][1]) is ID:
			print('assign', declObj.children()[0][1].getName(), declObj.children()[1][1].getName())

		# int i=(2*i*k);
		elif type(declObj.children()[1][1]) is BinaryOp:
			ids = getIdsFromObject(declObj.children()[1][1])						
			if ids:
				print('assign', declObj.children()[0][1].getName(), end=' ')				
				for id in ids:
					print(id, end=' ')
			print()

		# int i={3*k}
		elif type(declObj.children()[1][1]) is InitList:
			ids = getIDsFromInitList(declObj.children())
			print('assign', declObj.children()[0][1].getName(), end=' ')								
			if ids:
				for id in ids:
					print(id, end=' ')
			print()			

		elif type(declObj.children()[1][1]) is FuncCall:
			handleFunctionCalls(getIdsFromObject(declObj.children()[0][1]), declObj.children()[1][1], 'rcall')
		
	# int a[n] ...;
	elif type(declObj.children()[0][1]) is ArrayDecl:
		if len(declObj.children()) == 1:
			handlePreUnary(declObj.children()[0][1].children()[1][1])
			print('invar')
			handlePostUnary(declObj.children()[0][1].children()[1][1])
		
		# int a[n] = {i,j,k}
		elif type(declObj.children()[1][1]) is InitList:
			
			# ids = getIdsFromObject(declObj.children()[0][1].children()[0][1])
			print('assign', end=' ')			
			ids = getIdsFromObject(declObj.children()[0][1])
			for id in ids:
				print(id ,end=' ')
			
			ids = getIdsFromObject(declObj.children()[1][1])
			for id in ids:
				print(id ,end=' ')
			print()
		pass

	# handle postUnary
	handlePostUnary(declObj)	
	pass


def handleUnaryOp(UnaryObj):
	op = UnaryObj.getOperator()

	# ++i, i++, --i, i--;
	if op in ['++', 'p++', '--', 'p--']:
		print('assign',end=' ')
		for id in getIdFromUnaryOp(UnaryObj):
			print(id, end=' ')
		for id in getIdFromUnaryOp(UnaryObj):
			print(id, end=' ')
		print()
		pass
	pass


def handlePreUnary(obj):

	if type(obj) is UnaryOp:
		op = obj.getOperator()
		# ++i, --i;
		if op in ['++', '--']:
			handleUnaryOp(obj)
	for child in obj:
		handlePreUnary(child)
	pass


def handlePostUnary(obj):
	
	if type(obj) is UnaryOp:
		op = obj.getOperator()
		# i++, i--;
		if op in ['p++', 'p--']:
			handleUnaryOp(obj)
	for child in obj:
		handlePostUnary(child)
	pass


## MAIN FN

def dfs(nodeObj):

	if(nodeObj):		
		if type(nodeObj) is Assignment:
			handleMultiAssign([], nodeObj)
			# handleAssignmentOp(nodeObj)
		
		elif type(nodeObj) is While or type(nodeObj) is DoWhile:
			handleWhileLoops(nodeObj)

		elif type(nodeObj) is FuncCall:
			handleFunctionCalls([],nodeObj, 'call')
	
		elif type(nodeObj) is If:
			handleIfElse(nodeObj)

		elif type(nodeObj) is For:
			handleForLoops(nodeObj)
			
		elif type(nodeObj) is Decl:
			handleDeclerations(nodeObj)

		elif type(nodeObj) is UnaryOp:
			handleUnaryOp(nodeObj)

		else:
			# are all other objs iterable ??
			for child in nodeObj:
				dfs(child)


######################
## exec starts here
######################

parser = CParser()
with open("temp.c", 'rU') as f:
	text = f.read()
syntaxTree=parser.parse(text, "temp.c")


dfs(syntaxTree)

