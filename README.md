﻿﻿

TODO
===
0. remove pre and post incr in 'if'

1. add space after else if there is no if.

0. switch (omkar)

1. elseif(++i) (omkar - where to put assign i i , under which block)

2. ternary ops (omkar)

3. while(scanf("%d",&x)){} => output? (omkar)

4. int a=printf("%s\n", c); => output? (omkar)

5. sentinal for fn calls - kaleem "not required" bol raha hai

6. check assignments stmts in binary ops:
	for(   ;k<3 && (i=j);)

	assign i j
	loop k i 1
	assign i j

7. pointers – same as arrays (omkar - pointer example)

8. procedures other than main

8. for loop cond section contains functions ? (same as above)

9. a[i][i][i] = a[i][i][i] + 1 ? => assign a i a  (only used are output once... changed are printed times)

10. for loop initialization lines count if funciton is inside a for loop

11. a[++i] = j;
		 => assign i i
		assign a i j

12. merge assign and multiassign fns

14. sed - remove multiple occurance of vars not changed in assignment stmts

15. int a[3], a[i];

16. int i = somefunction(a, b);

18. include handlePreUnary and PostUnary fns in for, while and assignment fns

19. if(i>4){
		printf("%s\n", c);
	}
	else if( ++i){
		scanf("%d", &n);
	} 
	(omkar)

n. make compatible with input names


a = max(i, j); --- rcall max a i j
max(i, j); call max i j
reset(a); --- call reset a 

a = i + j;
a[i] = j;


max(a, max(b,c));

$1 = max(b,c)  
max(a, $1)


====================

main :

	a int
	b array
	c struct
...


DONE 
=====

functions call in printf() - ‘$i’ -  $1 fine - parse output twice using sentinal

no cond var in for loop ? - direct no of lines

multiple invars - two versions of code

handle array decls.

arrays - ‘a[i] = j’ => assign a i j

handled fscanf and fprintf

handled multiple function declarations and definitions

handled preincrement and post increment ops in "if condition stmts"
handled preincrement and post increment ops in array and variable declarations

handled function calls during assignment stmts

structure


multiple assignments in one statement.



// not handled
===
int i = arr[++j];

int a = b+=c;


