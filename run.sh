python3 C_TO_IR.py > out
python3 removeMultipleInvar.py out > out1
rm out
mv out1 out
python3 removeSentinal.py
