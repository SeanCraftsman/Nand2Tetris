// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

	
	@ 24575
	D = A
	@ MAX
	M = D

(BEGIN)
	
	
	@ SCREEN
	D = A
	@ ADDR
	M = D // ADDR = SCREEN

	@ KBD
	D = M
	@ NotEqual
	D; JNE

	@ COLOR
	M = 0

	@ DRAW
	0; JMP

(NotEqual)
	@ COLOR
	M = -1

(DRAW)

	@ ADDR
	D = M
	@ MAX
	D = D - M
	@ BEGIN
	D; JGT // if ADDR > MAX goto BEGIN

	@ COLOR
	D = M
	@ ADDR
	A = M
	M = D // RAM[A] = COLOR

	@ ADDR
	M = M + 1 // ADDR = ADDR + 1

	@ DRAW
	0; JMP


