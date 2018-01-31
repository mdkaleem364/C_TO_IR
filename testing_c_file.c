
int main()	{
	int r,c,k,sum;
	int mtx_f[3][3], mtx_s[3][3], mtx_r[3][3];
 	printf("Enter elements of first NxN matrix\n");
	for (r = 0; r < 3; r++)
		for (c = 0; c < 3; c++)
			scanf("%d", &mtx_f[r][c]);
 
  	printf("Enter elements of second NxN matrix\n");
	for (r = 0; r < 3; r++)
		for (c = 0; c < 3; c++)
			scanf("%d", &mtx_s[r][c]);
    
	for (r = 0; r < 3; r++) 
		for (c = 0; c < 3; c++) {
			sum = 0;
			for (k = 0; k < 3; k++) 
				sum = sum + mtx_f[r][k]*mtx_s[k][c];
		    mtx_r[r][c] = sum;
		        
    		}
 

	printf("Product of two  matrices\n");
 	for (r = 0; r < 3; r++) {
		for (c = 0; c < 3; c++)
		        printf("%5d", mtx_r[r][c]);
	      printf("\n");
	}
  
  	r = mtx_r[0][0] + mtx_r[0][1] + mtx_r[0][2];
  	c = mtx_r[1][0] + mtx_r[1][1] + mtx_r[1][2];
  	k = mtx_r[2][0] + mtx_r[2][1] + mtx_r[2][2]; 
  	
  	if (r>c && r >k)
  		printf("1st Row Sum = [%d]", r);
  	else if(c>k)
  		printf("2nd Row Sum = [%d]",c);
  	else
  		printf("3rd Row Sum = [%d]",k); 
 
	return 0;
}
