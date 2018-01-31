﻿

// TODO

1. ternary ops (omkar)

2. functions call in printf() - ‘$i’ -  $1 fine - parse output twice using sentinal

4. no cond var in for loop ? - direct no of lines

5. multiple invars - cannot be done - two versions of code

6. check assignments stmts in binary ops:
	for(   ;k<3 && (i=j);)

	assign i j
	loop k i 1
	assign i j

7. pointers – same as arrays (omkar - pointer example)

8. for loop cond section contains functions ? (same as above)

9. a[i][i][i] = a[i][i][i] + 1 ? => assign a i a  (only used are output once... changed are printed times)

// done 5. arrays - ‘a[i] = j’ => assign a i j

10. for loop initialization lines count if for loop is inside a function

11. a[++i] = j;
		 => assign i i
		assign a i j

12. merge assign and multiassign fns

13. structure

14. sed - remove multiple occurance of vars not changed in assignment stmts

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
