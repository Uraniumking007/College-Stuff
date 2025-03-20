LXI H,0009H
MVI C,0AH
add_numbers: MOV B,M
ADD B
DCX H
DCR C
JNZ add_numbers
HLT