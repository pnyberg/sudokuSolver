from sys import argv
import math

def acceptedRow(matrix, row):
	size = len(matrix)

	testRow = [False for x in range(size)]
	for k in range(size):
		number = matrix[row][k]
		if number == 0:
			continue
		if testRow[number-1]:
			return False
		testRow[number-1] = True

	return True

def acceptedColumn(matrix, column):
	size = len(matrix)

	testColumn = [False for y in range(size)]
	for k in range(size):
		number = matrix[k][column]
		if number == 0:
			continue
		if testColumn[number-1]:
			return False
		testColumn[number-1] = True

	return True

def acceptedBox(matrix, boxX, boxY):
	size = len(matrix)
	boxSize = int(math.sqrt(size))

	testBox = [False for b in range(size)]
	for y in range(boxSize):
		for x in range(boxSize):
#			print str(boxY * boxSize) + " + " + str(y) + " , " + str(boxX * boxSize) + " + " + str(x)
			number = matrix[boxY * boxSize + y][boxX * boxSize + x]
			if number == 0:
				continue
			if testBox[number-1]:
				return False
			testBox[number-1] = True

	return True

def acceptableSolution(matrix):
	size = len(matrix)
	boxSize = int(math.sqrt(size))
	
	for n in range(size):
		# check rows
		if not acceptedRow(matrix, n):
			return False

		# check columns
		if not acceptedColumn(matrix, n):
			return False

	# check boxes
	for boxY in range(boxSize):
		for boxX in range(boxSize):
			if not acceptedBox(matrix, boxX, boxY):
				return False

	return True

def solveSudoku(matrix, x, y):
	size = len(matrix)
	boxSize = int(math.sqrt(size))

	# if at end, check if this works
	if x == 0 and y == size:
		return acceptableSolution(matrix)

	newX = (x + 1) % size
	newY = y
	if newX == 0:
		newY += 1

	# test all numbers for this position
	accept = False
	if matrix[y][x] == 0:
		for i in range(1, size+1):
			matrix[y][x] = i

#			print "--> Testing " + str(i) + " at position (" + str(x) + "," + str(y) + ")"

			if not acceptedRow(matrix, y):
				continue
			if not acceptedColumn(matrix, x):
				continue
			if not acceptedBox(matrix, x/boxSize, y/boxSize):
				continue

			accept = solveSudoku(matrix, newX, newY)

			if accept:
				break
		if not accept:
			matrix[y][x] = 0 # resets variable
	else:
		return solveSudoku(matrix, newX, newY)

	return accept

###### Code starts ###########

# --- Read in matrix -----------------
inputFileName = argv[1]

fileFile = open(inputFileName)
fileContent = fileFile.read()

tokens = fileContent.split()

# --- Create matrix -----------------
size = int(tokens[0])

matrixSize = int(pow(size,2))
sudokuMatrix = [[0 for x in range(matrixSize)] for y in range(matrixSize)]

c = 1
for i in range(len(sudokuMatrix)):
	for j in range(len(sudokuMatrix[i])):
		number = int(tokens[c])
		if (number < 0 or number > pow(size, 2)):
			print "Unaccepted number at row " + str(i+1) + " and column " + str(j+1)
			exit(0)
		sudokuMatrix[i][j] = number
		c += 1

# --- Solve matrix -----------------

solutionExists = solveSudoku(sudokuMatrix, 0, 0)

# --- Print solution -----------------

for i in range(matrixSize):
	for j in range(matrixSize):
		print sudokuMatrix[i][j],
		if (j+1)%size == 0 and (j+1) != matrixSize:
			print "|",
	if (i+1)%size == 0 and (i+1) != matrixSize:
		print ""
		for k in range(matrixSize + size - 1):
			print "-",
	print ""