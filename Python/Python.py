import sys

# if parameter is wrong print error and exit
if len(sys.argv) != 2:
	print("parameter error")
	exit()

# if fail to open file print error and exit
try:
	# file handle
	handle = open(sys.argv[1])
except:
	print("file open error")
	exit()



# key: label name (str)
# value: lable address (int)
labelTable = dict()

# store all source code
srcCode = list()

#
class instr:
	opcode = int()
	operand = tuple()
	
	def __init__(self, opcode, operand):
		self.opcode = opcode
		self.operand = operand


# extract lable
for i, s in enumerate(handle):
	tmp = s.split()
	if s[0] is not '\t' and s[0] is not ' ':
		labelTable[tmp[0]] = i
		srcCode.append(tmp[1:])
	else:
		srcCode.append(tmp)

# add special lable
labelTable["lf"] = -1
labelTable["write"] = -2
labelTable["read"] = -3

# define opcodes list and build dict
opCodes = ["notop", "neg", "inc", "dec", "dup", "add", "sub", "mult", "div", "mod", \
	"swp", "and", "or", "gt", "lt", "ge", "le", "eq", "ne", "lod", "str", "ldc", \
	"lda", "ujp", "tjp", "fjp", "chkh", "chkl", "ldi", "sti", "call", "ret", "retv", \
	"ldp", "proc", "end", "nop", "bgn", "sym", "dump"]

opCodeDict = dict()
for i, s in enumerate(opCodes):
	opCodeDict[s] = i
	


# program counter
pc = int()

# extract parameter
# and convert opcode to integer
for i, tmpList in enumerate(srcCode):
	op = opCodeDict[tmpList[0]]

	# no parameter
	if (0 <= op <= 18) or op in [28, 29, 31, 32, 33, 35, 36, 39]:
		srcCode[i] = instr(op, None)

	# 3 parameter
	elif op == 38 or op == 34:
		srcCode[i] = instr(op, (int(tmpList[1]), int(tmpList[2]), int(tmpList[3])))

	# 1 integer parameter
	elif op in [21, 26, 27, 37]:
		srcCode[i] = instr(op, (int(tmpList[1]), ))
		# if op is bgn
		if op is 37:
			pc = i

	# 1 label parameter
	elif op in [23, 24, 25, 30]:
		srcCode[i] = instr(op, (labelTable[tmpList[1]], ))

	# 2 parameter
	else:
		srcCode[i] = instr(op, (int(tmpList[1]), int(tmpList[2])))

# DEBUG
#for l in srcCode:
#	print(l.opcode, "({0})".format(opCodes[l.opcode]), l.operand)
#

class Stack:
	arr = list()
	sp = -1

	def __init__(self, size):
		self.arr = [0]*size
	
	def __len__(self):
		return len(self.arr)

	def pop(self):
		self.sp -= 1
		return self.arr[self.sp + 1]

	def push(self, val):
		self.sp += 1
		if self.sp >= len(self.arr):
			self.arr.append(val)
		else:
			self.arr[self.sp] = val

	def __getitem__(self, i):
		if i < 0:
			i += self.sp + 1
		return self.arr[i]

	def __setitem__(self, i, value):
		if i >= 0:
			self.arr[i] = value
		else:
			self.arr[self.sp + i + 1] = value

	def setSP(self, val):
		if val >= len(self.arr):
			self.arr.extend([0] * (val - len(self.arr) + 1))
		self.sp = val

stack = Stack(10)
curntFuncStartP = int()
spBackUp = int()
# input buffer
buffer = list()



def findAddress(address):
	tmp = curntFuncStartP
	while address[0] != stack[tmp + 3]:
		tmp = stack[tmp]
	return tmp + 3 + address[1]




while True:
	op = srcCode[pc].opcode
	operand = srcCode[pc].operand
	#print("pc: {0}, {1} ({2})".format(pc, op, opCodes[op]))
	
	# notop
	if op == 0:
		if stack[-1] == 0:
			stack[-1] = 1
		else:
			stack[-1] = 0
	# neg
	elif op == 1:
		stack[-1] *= -1
	# inc
	elif op == 2:
		stack[-1] += 1
	# dec
	elif op == 3:
		stack[-1] -= 1
	# dup
	elif op == 4:
		stack.push(stack[-1])
	# add
	elif op == 5:
		stack[-2] += stack[-1]
		stack.pop()
	# sub
	elif op == 6:
		stack[-2] -= stack[-1]
		stack.pop()
	# multi
	elif op == 7:
		stack[-2] *= stack[-1]
		stack.pop()
	# div
	elif op == 8:
		stack[-2] //= stack[-1]
		stack.pop()
	# mod
	elif op == 9:
		stack[-2] %= stack[-1]
		stack.pop()
	# swp
	elif op == 10:
		stack[-1], stack[-2] = stack[-2], stack[-1]
	# and
	elif op == 11:
		stack[-2] = stack[-2] & stack[-1]
		stack.pop()
	# or
	elif op == 12:
		stack[-2] = stack[-2] | stack[-1]
		stack.pop()
	# gt
	elif op == 13:
		if stack[-2] > stack[-1]:
			stack[-2] = 1
		else:
			stack[-2] = 0
		stack.pop()
	# lt
	elif op == 14:
		if stack[-2] < stack[-1]:
			stack[-2] = 1
		else:
			stack[-2] = 0
		stack.pop()
	# ge
	elif op == 15:
		if stack[-2] >= stack[-1]:
			stack[-2] = 1
		else:
			stack[-2] = 0
		stack.pop()
	# le
	elif op == 16:
		if stack[-2] <= stack[-1]:
			stack[-2] = 1
		else:
			stack[-2] = 0
		stack.pop()
	# eq
	elif op == 17:
		if stack[-2] == stack[-1]:
			stack[-2] = 1
		else:
			stack[-2] = 0
		stack.pop()
	# ne
	elif op == 18:
		if stack[-2] != stack[-1]:
			stack[-2] = 1
		else:
			stack[-2] = 0
		stack.pop()
	# lod
	elif op == 19:
		stack.push(stack[findAddress(operand)])
	# str
	elif op == 20:
		stack[findAddress(operand)] = stack.pop()
	# ldc
	elif op == 21:
		stack.push(operand[0])
	# lda
	elif op == 22:
		stack.push(findAddress(operand))
	# ujp
	elif op == 23:
		pc = operand[0] - 1
	# tjp
	elif op == 24:
		if stack.pop() == 1:
			pc = operand[0] - 1
	# fjp
	elif op == 25:
		if stack.pop() == 0:
			pc = operand[0] - 1
	# chkh
	elif op == 26:
		if stack[-1] > operand[0]:
			print("chkh")
	# chkl
	elif op == 27:
		if stack[-1] < operand[0]:
			print("chkl")
	# ldi
	elif op == 28:
		stack[-1] = stack[stack[-1]]
	# sti
	elif op == 29:
		dataToSave = stack.pop()
		stack[stack[-1]] = dataToSave
		stack.pop()
	# call
	elif op == 30:
		if operand[0] == -1:
			print("")
		elif operand[0] == -2:
			print(stack[-1], end = " ")
			stack.setSP(spBackUp - 1)
		elif operand[0] == -3:
			while len(buffer) == 0:
				buffer = list(map(int, input().split()))
			stack[stack[-1]] = buffer.pop(0)
			stack.setSP(spBackUp - 1)
		else:
			stack[spBackUp + 2] = pc + 1
			stack[spBackUp + 1] = curntFuncStartP
			curntFuncStartP = spBackUp
			pc = operand[0] - 1
	# ret
	elif op == 31:
		stack.setSP(curntFuncStartP - 1)
		pc = stack[curntFuncStartP + 2] - 1
		curntFuncStartP = stack[curntFuncStartP + 1]
	# retv
	elif op == 32:
		tmp = stack[stack.sp]
		stack.setSP(curntFuncStartP - 1)
		stack.push(tmp)
		pc = stack[curntFuncStartP + 2] - 1
		curntFuncStartP = stack[curntFuncStartP + 1]
	# ldp
	elif op == 33:
		spBackUp = stack.sp + 1
		stack.setSP(stack.sp + 4)
	# proc
	elif op == 34:
		stack[curntFuncStartP + 3] = operand[2]
		stack.setSP(curntFuncStartP + operand[0] + 3)
		tmp = stack[curntFuncStartP + 1]
		while operand[2] - 1 != stack[tmp + 3]:
			tmp = stack[tmp]
		stack[curntFuncStartP] = tmp
	# end
	elif op == 35:
		break
	# nop
	elif op == 36:
		pass
	# bgn
	elif op == 37:
		curntFuncStartP = stack.sp + 1
		stack.push(0)
		stack.push(0)
		stack.push(-1)
		stack.push(1)
		stack.setSP(stack.sp + operand[0])
	# sym
	elif op == 38:
		pass
	# dump
	elif op == 39:
		for i, v in enumerate(stack.arr):
			if i > stack.sp: break
			print("({0}, {1})".format(i, v), end=' ')
		print("")

	pc += 1


#	for i, v in enumerate(stack.arr):
#		if i > stack.sp: break
#		print("({0}, {1})".format(i, v), end=' ')
#	print("")