import sys
from c_parser import CParser

"""
for testing print added in 
c_ast.c
	line : 695 and 937

"""
parser = CParser()
with open("testing_c_file.c", 'rU') as f:
	text = f.read()
sytaxTree=parser.parse(text, "testing_c_file.c")


print sytaxTree
print sytaxTree.children()
print "first child"
temp1= sytaxTree.children()[0][1]
print temp1
temp2= temp1.children()[0][1]
print temp2
temp3= temp2.children()[0][1]
print temp3
print temp3.children()

print "second child"
temp0 =sytaxTree.children()[1][1]
print temp0
print temp0.children()
temp1= temp0.children()[0][1]
print "second-first child"
print temp1
temp2= temp1.children()[0][1]
print temp2
temp3= temp2.children()[0][1]
print temp3
temp4= temp3.children()[0][1]
print temp4
temp5 = temp4.children()
print temp5

print "second-second child"
temp6 =temp0.children()[1][1]
print temp6
temp7 =temp6.children()
print temp7