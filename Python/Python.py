import sys

# if parameter is wrong print error and exit
if len(sys.argv) != 3:		# �Ķ������ ������ 3�����ƴ� �� ����ó��
	print("parameter error")
	exit()

# if fail to open file print error and exit
try:
	# file readHandle
	readHandle = open(sys.argv[1])	# readHandle�� �̿��� �ҽ��ڵ� ������ �������� ó��
	writeHandle = open(sys.argv[2], mode = 'w')	# writeHandle�� �̿��� �ҽ��ڵ� ������ �������� ó��
except:
	print("file open error")		# ���� ��¿� ���� ����ó��
	exit()



# key: label name (str)		  key �� label�� �̸�
# value: label address (int)  value�� ���� �ѹ�(lable�� address)
labelTable = dict()			# ���� �����ϱ����� labelTable�� ������ dictŸ������ ����

# store all source code in class
srcCode = list()			# ��� �ҽ��ڵ带 �����ϱ� ���� srcCode�� ����Ʈ Ÿ������ ����
# store all source code in str
originalSrcCode = list()

#
class instr:
	opcode = int()		# ��ɾ �ޱ����� opcode�� intŸ��
	operand = tuple()	# �Ķ���͵��� �޴� operand�� tupleŸ��(�Ķ���� ������ �ٸ��Ƿ�)
	
	def __init__(self, opcode, operand):
		self.opcode = opcode
		self.operand = operand

i = 0
# extract label			# handle�ȿ� �ִ� ������� ���پ� �����´�.
for s in readHandle:
	originalSrcCode.append(s[:-1])
	tmp = s.split()		# �� ���� �ҽ��ڵ带 split()�� �̿��Ͽ� �ɰ���.
	if len(tmp) == 0:	# ������ ��� ����
		continue
	elif s[0] is not '\t' and s[0] is not ' ':	# ���� ù��°(���� ��ġ)�� ������ �ƴ� ���
		labelTable[tmp[0]] = i		# ���� key�� ���� ��ġ�� �ٹ�ȣ�� Value�� labelTable�� ����
		srcCode.append(tmp[1:])		# ���� ������ �κ��� srcCode�� append
	else:
		srcCode.append(tmp)			# ù��°�� ������ ��� �׳� srcCode�� append
	i += 1

# add special label
#������ ���ǵ� ���̱⿡ ���Ƿ� ������ ó��
labelTable["lf"] = -1
labelTable["write"] = -2
labelTable["read"] = -3

# define opcodes list and build dict
#�켱 opCodes�� ��� Ucode��ɾ �ִ´�.
opCodes = ["notop", "neg", "inc", "dec", "dup", "add", "sub", "mult", "div", "mod", \
	"swp", "and", "or", "gt", "lt", "ge", "le", "eq", "ne", "lod", "str", "ldc", \
	"lda", "ujp", "tjp", "fjp", "chkh", "chkl", "ldi", "sti", "call", "ret", "retv", \
	"ldp", "proc", "end", "nop", "bgn", "sym", "dump"]

# opCodeDict�� ������ ������ opCodes�� �ִ� ���ڷε� Opcode�� Key�� �ϰ� �װͿ� ���� Integer ���� Value�� ���� dictŸ�� 
opCodeDict = dict()
for i, s in enumerate(opCodes):
	opCodeDict[s] = i
	
dynamicInstrCount = [0] * len(opCodes)
staticInstrCount = [0] * len(opCodes)

# program counter
pc = int()

# extract parameter
# and convert opcode to integer
for i, tmpList in enumerate(srcCode):
	op = opCodeDict[tmpList[0]]		# �ش� Opcode�� ���� ��ȣ�� op�� ����
	staticInstrCount[op] += 1

	## �Ķ������ ������ �������� ������ ##

	# no parameter
	# �Ķ���Ͱ� ���� ���, �Ķ���ͺκп� None(�Ķ���͸� ������ ������ ��Ÿ��)���� �ؼ� instr ���·� scrCode�� ����.
	if (0 <= op <= 18) or op in [28, 29, 31, 32, 33, 35, 36, 39]:
		srcCode[i] = instr(op, None)

	# 3 parameter
	# ������ �Ķ���Ͱ� 3�� �ִ� ���, �Ķ���ͺκп��� 3���� ������ ���µ�
	# tmpList�� String�̹Ƿ� int������ �ٲ��ְ� 3���� ���� Ʃ�û��·� �ؼ� instr ���·� scrCode�� ����.
	elif op == 38 or op == 34:
		srcCode[i] = instr(op, (int(tmpList[1]), int(tmpList[2]), int(tmpList[3])))

	# 1 integer parameter
	# ������ �Ķ���Ͱ� 1�� �ִ� ���
	elif op in [21, 26, 27, 37]:
		srcCode[i] = instr(op, (int(tmpList[1]), ))
		# if op is bgn
		# bgn(op=37)�� ��� bgn�� ��ġ�� ���� ��ȣ�� pc�� �ȴ�.
		if op is 37:
			pc = i

	# 1 label parameter
	# �Ķ���Ͱ� 1���ִ� ���, 1���� �Ķ���Ͱ� ���� ���
	elif op in [23, 24, 25, 30]:
		srcCode[i] = instr(op, (labelTable[tmpList[1]], ))

	# 2 parameter
	# ������ �Ķ���Ͱ� 2�� �ִ� ���
	else:
		srcCode[i] = instr(op, (int(tmpList[1]), int(tmpList[2])))


# �ҽ� �ڵ� ���
writeHandle.write("Line\t object\t\t ucode source program\n\n")
for i, l in enumerate(srcCode):
	writeHandle.write("{0:3}\t({1}  {2})\t{3}\n".format(i, l.opcode, l.operand, originalSrcCode[i]))


class Stack:
	arr = list()
	# �ƹ��͵� ������� ���� ���
	sp = -1

	# ������
	# ������ ũ�� ����
	def __init__(self, size):
		self.arr = [0]*size

	# Top���ִ� ���� ������ ����
	def pop(self):
		self.sp -= 1
		return self.arr[self.sp + 1]

	# ���� Top+1�� �Ѱ��� ���� �ִ´�.
	def push(self, val):
		self.sp += 1
		# ����, sp�� arr���̺��� Ŭ ��� arr�� �߰� �Ҵ�
		if self.sp >= len(self.arr):
			self.arr.append(val)
		# �ƴ� ��� sp�� ��ġ�ϴ� ���� ���� �ִ´�.
		else:
			self.arr[self.sp] = val

	# ���ϴ� ��ġ�� ���� �������� ���� �Լ�
	def __getitem__(self, i):
		if i < 0:
			# sp������ ���� �ε����� ���� �����������ؼ�
			# �� (������ -1�� ���, arr���� ����ڿ� ��ġ�ϹǷ� i = sp+1+(-1)
			i += self.sp + 1
		return self.arr[i]

	# ���ϴ� ��ġ�� ���� �ֱ� ���� �Լ�
	def __setitem__(self, i, value):
		if i >= 0:
			self.arr[i] = value
		else:
			# sp�� �ִ� ���� ���� ����
			self.arr[self.sp + i + 1] = value

	# sp�� �������ֱ����� �Լ�
	def setSP(self, val):
		# sp�� ��ġ�� ���� ���� �Ҵ���� ���� ���̶��
		if val >= len(self.arr):
			# arr �߰� �Ҵ�
			self.arr.extend([0] * (val - len(self.arr) + 1))
		self.sp = val

stack = Stack(10)

# �Լ������ּҸ� �˱����� 
curntFuncStartP = int()

# ldp�� �Ұ�쿡 �ش�κ��� �����ּҸ� �˱�����
spBackUp = int()

# input buffer
buffer = list()



# �ڱⰡ ���ϴ� �ּҸ� ã���ִ� �Լ�
def findAddress(address):
	tmp = curntFuncStartP	# �����Լ��� �����ּҸ� tmp�� ����

	# ���� 0��° ����� �����Ϸ��� �� ����� ����ó��
	if tmp < 0 or (address[0] == 0):
		print("wrong memory access")
		exit(1)
	# operand[0](��Ϲ�ȣ)�� ���� block ��ȣ�� ���� �� ���� �ݺ� 
	while address[0] != stack[tmp + 3]:
		tmp = stack[tmp]	# �����ּҿ� �ִ� ��(Lexical-1�� ���� block��ȣ�� ���� ���� �����ּ�)�� tmp�� ����
		# ������°�� �����Ϸ��� �� ���� ����ó��
		if tmp < 1:
			print("wrong memory access")
			exit(1)
	return tmp + 3 + address[1]	# �� block��ȣ�� ���� �Լ��� offset(address[1])�� �ش�Ǵ� �ּҸ� ����


writeHandle.write("\n*****  Result  *****\n\n")

while True:
	op = srcCode[pc].opcode
	operand = srcCode[pc].operand
	dynamicInstrCount[op] += 1
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
		if stack[-1] is 0:
			print("can't divide by 0")
			exit(1)
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
		# operand�� �ش�Ǵ� stack������ �ּ�
		address = findAddress(operand)
		# stack���� address�� �ش�Ǵ� ���� ���� �����´�.
		value = stack[address]
		# �׸��� �� ���� �ٽ� top�� push
		stack.push(value)
	# str
	# operand�� �ش�Ǵ� stack�� �ּҿ� ���� ���� ���� �־��ش�.
	elif op == 20:
		# operand�� �ش�Ǵ� stack������ �ּ�
		address = findAddress(operand)
		# stack���� address�� �ش�Ǵ� ���� top�� �ִ� ���� ����
		stack[address] = stack.pop()
	# ldc
	elif op == 21:
		stack.push(operand[0])
	# lda
	elif op == 22:
		address = findAddress(operand)
		stack.push(address)
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
			print("error chkh")
			exit(1)
	# chkl
	elif op == 27:
		if stack[-1] < operand[0]:
			print("error chkl")
			exit(1)
	# ldi
	elif op == 28:
		address = stack.pop()		# ���� top�� �ִ� ���� �ּҷ�
		stack.push(stack[address])	# �� �ּҿ� �´� ���� ���� top�� �ٽ�����
	# sti
	elif op == 29:
		dataToSave = stack.pop()	# ���� top�� �ִ� ���� dataToSave�� �ְ�
		address = stack.pop()		# �״����� top�� �ִ� ���� �ּҷ� ����
		stack[address] = dataToSave	# stack���� �ش� �ּҿ� �ִ� ���� dataToSave ���� �ִ´�.
	# call
	elif op == 30:
		# lf �ٹٲ�
		if operand[0] == -1:
			writeHandle.write("\n")
		# write ������ �� ��� 
		elif operand[0] == -2:
			writeHandle.write("{0} ".format(stack[-1]))
			stack.setSP(spBackUp - 1)
		# read 
		elif operand[0] == -3:
			while len(buffer) == 0:	# ���ۿ� ���� ���� ����
				# map�� �̿��Ͽ� split()�� �������� �Է°� ���� ���� int�Լ��� ���ϰ�, list�������� buffer�� ���� 
				buffer = list(map(int, input().split()))
			address = stack.pop()			# top�� �ִ� ���� ������ address���ϰ�
			stack[address] = buffer.pop(0)	# stack���� �� address�� �ش��ϴ� �κп� ���ۿ� ù��°�ִ� ���� pop�ؼ� �ִ´�.
			stack.setSP(spBackUp - 1)
		else:
			stack[spBackUp + 2] = pc + 1			# ���ƿ� ��ġ(call �ٷ� �ؿ� ���γѹ��� ��)�� �����ص�
			stack[spBackUp + 1] = curntFuncStartP	# ���� ����� ������ġ
			curntFuncStartP = spBackUp				# ���� �Լ��� ������ġ�� curntFuncStartP�� ����
			pc = operand[0] - 1		# �ش� �Լ�(��)�� srcCode�� ������ġ�� pc�� �صд�. while�Ҷ����� +1�� ���ֱ� ������ -1�� ���ִ� ���̴�.
	# ret
	elif op == 31:
		stack.setSP(curntFuncStartP - 1)			# ���� �Լ��� ������� �ϱ� ���� sp����
		pc = stack[curntFuncStartP + 2] - 1			# �ٽ� ���ư� PC������ PC����
		curntFuncStartP = stack[curntFuncStartP + 1]# ���� ����� �����ּҸ� curntFuncStratP�� �ص�.( call�ϱ� ������ ���� �����ּҷ� ����)
	# retv
	elif op == 32:
		tmp = stack[-1]						#  ���� �Լ��� ������ ���� tmp������
		stack.setSP(curntFuncStartP - 1)	# ���� �Լ��� ������� �ϱ� ���� sp����
		stack.push(tmp)					# ���� �Լ��� ������ ���� �ٽ� ������ SP�� push
		pc = stack[curntFuncStartP + 2] - 1	# �ٽ� ���ư� PC������ PC����
		# ���� ����� �����ּҸ� curntFuncStratP�� �ص�.( call�ϱ� ������ ���� �����ּҷ� ����)
		curntFuncStartP = stack[curntFuncStartP + 1]
	# ldp
	elif op == 33:
		spBackUp = stack.sp + 1		# �ش� �Լ��� ������ġ�� �����ϱ� ����
		stack.setSP(stack.sp + 4)	# �ش� �Լ��� ������ �����ϱ� ���ؼ�
	# proc
	elif op == 34:
		stack[curntFuncStartP + 3] = operand[1]			# �ڽ��� ��ϳѹ��� �ֱ� ����
		stack.setSP(curntFuncStartP + operand[0] + 3)	# �Ҵ� ���� ����ŭ sp�� �÷��ش�.
		tmp = stack[curntFuncStartP + 1]				# ���� ����� �����ּ�
		while operand[2] - 1 != stack[tmp + 3]:	# ���� Lexical-1�� ���� �����ȣ�� ������������ �ݺ�
			tmp = stack[tmp]					# ���� ����� �����ּҿ� �ش��ϴ� ���� tmp�� �־�д�
		stack[curntFuncStartP] = tmp			# ���� Lexical-1�� ���� �����ȣ�� ���� ���� �����ּ�
	# end
	# ���α׷� ����
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
		stack.setSP(stack.sp + operand[0])	# stack.sp= 3 + bgn�� �Ķ����
	# sym
	# ���� �ڵ忡���� �ǹ̾���
	elif op == 38:
		pass
	# dump
	# ����� �� opCode(���� Stack�� �ִ� ������ ��������)
	elif op == 39:
		for i, v in enumerate(stack.arr):
			if i > stack.sp: break
			# stack������ ��ġ�� �ش���ġ�� ���� ���
			print("({0}, {1})".format(i, v), end=' ')
		print("")

	#�ݺ��Ҷ����� pc+1
	pc += 1



writeHandle.write("\n\n\n\t*****  Statistics  *****\n\n")
writeHandle.write("\n*****  Static Instruction Counts  *****\n\n")

for i in range(0, 40, 4):
	writeHandle.write("{0:5} = {1}\t".format(opCodes[i], staticInstrCount[i]))
	writeHandle.write("{0:5} = {1}\t".format(opCodes[i + 1], staticInstrCount[i + 1]))
	writeHandle.write("{0:5} = {1}\t".format(opCodes[i + 2], staticInstrCount[i + 2]))
	writeHandle.write("{0:5} = {1}\n".format(opCodes[i + 3], staticInstrCount[i + 3]))

writeHandle.write("\n\n*****  Dynamic instruction counts  *****\n\n")
for i in range(0, 40, 4):
	writeHandle.write("{0:5} = {1}\t".format(opCodes[i], dynamicInstrCount[i]))
	writeHandle.write("{0:5} = {1}\t".format(opCodes[i + 1], dynamicInstrCount[i + 1]))
	writeHandle.write("{0:5} = {1}\t".format(opCodes[i + 2], dynamicInstrCount[i + 2]))
	writeHandle.write("{0:5} = {1}\n".format(opCodes[i + 3], dynamicInstrCount[i + 3]))