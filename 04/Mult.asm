// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
	
	@ A
	M = 0
	@ R1
	D = M
	@ B
	M = D

(LOOP)
	@ B
	D = M
	@ STOP
	D; JLE
	@ R0
	D = M
	@ A
	M = M + D
	@ B
	M = M - 1
	@ LOOP
	0; JMP

(STOP)
	@ A
	D = M
	@ R2
	M = D

(END)
	@ END
	0;JMP