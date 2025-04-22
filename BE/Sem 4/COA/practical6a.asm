MVI C,0AH
MVI B,01H
add_number: ADD C
;INR B
DCR C
JNZ add_number
HLT