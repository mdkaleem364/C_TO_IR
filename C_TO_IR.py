import sys
from c_ast import *
from c_parser import CParser

"""
for testing print added in 
c_ast.c
	line : 695 and 937

"""

# returns all variable names from the quation binaryOpObj
def getIDsFromBinaryOp(binaryOpObj):
	ret = []
	for i in binaryOpObj:
		if type(i) is ID:
			ret.append(i.getName())
		if type(i) is BinaryOp:
			ret.extend(getIDsFromBinaryOp(i))
	return ret
	
# handles 'a=b*d/c*10'
def handleBinaryOp(leftNode, BinaryOpObj):
	
	ids = getIDsFromBinaryOp(BinaryOpObj)
	
	for i in leftNode:
		print('assign', i, end=" ")
	
		for id in ids:
			print(id, end=" ")
		print()
	pass

# handles 'a=b=c=...'
def handleMultiAssign(leftNodes, assignmentObj):

	leftChild = assignmentObj.children()[0][1]
	rightChild = assignmentObj.children()[1][1]

	leftNodes.append(leftChild.getName())		

	if type(rightChild) is Assignment:
		handleMultiAssign(leftNodes, rightChild)

	elif type(rightChild) is Constant:
		for id in leftNodes:
			print('assign',id)

	elif type(rightChild) is ID:
		for id in leftNodes:
			print('assign', id, rightChild.getName())
	
	elif type(rightChild) is BinaryOp:	# a = b*c
		ids = getIDsFromBinaryOp(rightChild)
		
		for id in leftNodes:			
			print('assign',id, end=' ')
			for id1 in ids:
				print(id1, end=' ')
			print()
		
	pass

# handling (l = r) stmts
def handleAssignmentOp(assignmentObj):

	leftChild = assignmentObj.children()[0][1]
	rightChild = assignmentObj.children()[1][1]

	leftSide = [leftChild.getName()]

	op = assignmentObj.getOperator()
	if op in ['+=', '-=', '*=', '/=', '>>=', '<<=', '%=', '|=', '&=', '^=']:
		leftSide += [leftChild.getName()]

	# a=b || a+=b
	if type(rightChild) is ID:
		print('assign', end=' ')
		for id in leftSide:
			print(id, end=' ')
		print(rightChild.getName())

	# a=b=c || a+=b=c ?
	elif type(rightChild) is Assignment:
		handleMultiAssign([leftChild.getName()], rightChild)
	
	# a = b*c || a += b*c
	elif type(rightChild) is BinaryOp:
		ids = getIDsFromBinaryOp(rightChild)
		print('assign', end=' ')
		for id in leftSide:
			print(id, end=' ')
		for id in ids:
			print(id,end=' ')
		print()

	# a=10 || a += 5
	elif type(rightChild) is Constant:
		print('assign', end=' ')
		for id in leftSide:
			print(id, end=' ')
		print()	
	pass	


def handleWhileLoops(nodeObj):
	
	ids = getIDsFromBinaryOp(nodeObj.children()[0])
	print('loop', end=' ')
	for id in ids:
		print(id, end=' ')
	
	# while with braces {}
	if type(nodeObj.children()[1][1]) is Compound:	
		print(len(nodeObj.children()[1][1].children()))
	
	# while without braces (only 1 stmt)
	else:
		print('1')

	dfs(nodeObj.children()[1][1])
	pass


def handleScanf(scanfObj):
	print('input', end=' ')
	for expr in scanfObj.children()[1][1].children():
		if type(expr[1]) is UnaryOp:
			print(expr[1].children()[0][1].getName(), end=' ')
	print()

	pass

def handlePrintf(printfObj):

	# no vars is printed in printf
	if len(printfObj.children()[1][1].children()) < 2:
		print("invar")

	else:
		print("output", end=' ')
		for expr in printfObj.children()[1][1].children():
			
			if type(expr[1]) is ID:
				print(expr[1].getName(), end=' ')
			
			elif type(expr[1]) is BinaryOp:
				ids = getIDsFromBinaryOp(expr)
				for id in ids:
					print(id,end=' ')

		print()
	pass


# printf, scanf, anyother fn call
def handleFunctionCalls(fnCallObj):
	if fnCallObj.children()[0][1].getName() == 'scanf':
		handleScanf(fnCallObj)

	elif fnCallObj.children()[0][1].getName() == 'printf':
		handlePrintf(fnCallObj)

	pass


def handleIfElse(nodeObj):

	# print("ID",nodeObj.children()[2][1].children())

	ids = getIDsFromBinaryOp(nodeObj.children()[0])
	print('if', end=' ')
	for id in ids:
		print(id,end=' ')
	
	followedLines = 0
	# if block with braces {}
	if type(nodeObj.children()[1][1]) is Compound:
		followedLines += len(nodeObj.children()[1][1].children())
	
	# if block without braces
	else:
		followedLines += 1

	# if there is a 'else' or 'else if'
	followedLines += abs(len(nodeObj.children()) - 2)

	print(followedLines)

	# recur on stmts inside 'if' block
	dfs(nodeObj.children()[1][1])
	
	# check if 'else' or 'else if' block exists
	if len(nodeObj.children()) > 2:

		print('else',end='')

		# check if 'else if' stmt
		if type(nodeObj.children()[2][1]) is If:
			handleIfElse(nodeObj.children()[2][1])

		else:
			followedLines = 0
			# else block with  braces { }
			if type(nodeObj.children()[2][1]) is Compound:
				followedLines += len(nodeObj.children()[2][1].children())
			
			# else block without braces
			else:
				followedLines += 1

			# if there is a 'else' or 'else if'
			followedLines += abs(len(nodeObj.children()[2][1].children()) - 2)

			print(followedLines)

			# recur on stmts inside 'else' block
			dfs(nodeObj.children()[2][1])		
	pass


def handleForLoops(forLoopObj):
	ind = 0
	## init - optional
	if forLoopObj.children()[ind][0] == 'init':	
		dfs(forLoopObj.children()[0][1])
		
		# DeclList (can have assignment stmts)
		# int i=0,j=k;
		# if type(forLoopObj.children()[0][1]) is DeclList:
		# 	for declObj in forLoopObj.children()[0][1]:
		# 		handleDeclerations(declObj)
		
		# # ExprList (can have assignment stmts)
		# # i=0, j=k;
		# elif type(forLoopObj.children()[0][1]) is ExprList:
		# 	for exp in forLoopObj.children()[0][1]:
		# 		# if type(exp[1]) is Assignment:			
		# 		handleAssignmentOp(exp)

		# # Assignment
		# # i = j;
		# elif type(forLoopObj.children()[0][1]) is Assignment:
		# 	handleAssignmentOp(forLoopObj.children()[0][1])

		ind += 1

	## cond - optional
	# not handled - ( 1||a=b )
	if forLoopObj.children()[ind][0] == 'cond':	
		# dfs(forLoopObj.children()[0][1])
		# (can have assignment stmts)
		# handleAssignmentsInBinaryOps()
		ind += 1

	## next - optional
	if forLoopObj.children()[ind][0] == 'next':
		# (can have assignment stmts)
		dfs(forLoopObj.children()[0][1])

		ind += 1		

	## stmt - Empty/Compound/(Single line)
	# incomplete

	pass


def getIDsFromInitList(initListObj):
	ids = []
	for obj in initListObj.children():

		# int i={j,k}
		if type(obj[1]) is ID:
			ids += [obj[1].getName()]

		# int i={j*2, k}
		elif type(obj[1]) is BinaryOp:
			ids += getIDsFromBinaryOp(obj[1])

	return ids


def handleDeclerations(declObj):
	
	if type(declObj.children()[0][1]) is TypeDecl:
		
		# int i;
		if len(declObj.children()) == 1:
			print('Invar')

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
			ids = getIDsFromBinaryOp(declObj.children()[1][1])						
			if ids:
				print('assign', declObj.children()[0][1].getName(), end=' ')				
				for id in ids:
					print(id, end=' ')
			print()

		# int i={3*k}
		elif type(declObj.children()[1][1]) is InitList:
			ids = getIDsFromInitList(declObj.children()[1][1])
			if ids:
				print('assign', declObj.children()[0][1].getName(), end=' ')				
				for id in ids:
					print(id, end=' ')
			print()			

	pass


def handleUnaryOp(UnaryObj):
	op = UnaryObj.getOperator()

	# ++i, i++, --i, i--;
	if op in ['++', 'p++', '--', 'p--']:
		print('assign',UnaryObj.children()[0][1].getName(),UnaryObj.children()[0][1].getName())
		pass
	pass


## MAIN FN

def dfs(nodeObj):

	if(nodeObj):		
		if type(nodeObj) is Assignment:
			handleAssignmentOp(nodeObj)
			pass
		
		elif type(nodeObj) is While or type(nodeObj) is DoWhile:
			handleWhileLoops(nodeObj)

		elif type(nodeObj) is FuncCall:
			handleFunctionCalls(nodeObj)
	
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


parser = CParser()
with open("testing_c_file.c", 'rU') as f:
	text = f.read()
syntaxTree=parser.parse(text, "testing_c_file.c")


dfs(syntaxTree)
