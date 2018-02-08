#copy user file
#cp userfile.c testing_c_file.c

# remove #includes
sed '/^\#.*include.*/d' ./testing_c_file.c > temp.c

# preprocess input c file
cpp temp.c > temp1.c
mv temp1.c testing_c_file.c

python3 C_TO_IR.py > out
python3 removeMultipleInvar.py out > out1
rm out
mv out1 out

python3 removeSentinal.py
