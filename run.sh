#copy user file
#cp userfile.c testing_c_file.c

# remove #includes
sed '/^\s*\#.*include.*/d' ./testing_c_file.c > temp.c

# preprocess input c file
cpp temp.c > temp1.c
rm temp.c
mv temp1.c temp.c
# mv temp1.c testing_c_file.c

# run main code
python3 C_TO_IR.py > out # give file as param
rm temp.c
python3 removeMultipleInvar.py out > out1
rm out
mv out1 out

# remove sentinals (endIf, endWhile, endFor)
python3 removeSentinal.py 	# give file as param
