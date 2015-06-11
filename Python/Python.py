import sys
import struct
import datetime

# if parameter is wrong print error and exit
if len(sys.argv) != 3:		# 파라미터의 개수가 3개가아닐 때 예외처리
	print("parameter error")
	exit()

# if fail to open file print error and exit
try:
	# file readHandle
	readHandle = open(sys.argv[1])				# readHandle을 이용한 소스코드 파일을 열기위한 처리
	writeHandle = open(sys.argv[2], mode='w')	# writeHandle을 이용한 소스코드 파일을 열기위한 처리
except:
	print("file open error")		# 파일 출력에 대한 예외처리
	exit()



# key: label name (str)		  key 는 label의 이름
# value: label address (int)  value는 라인 넘버(lable의 address)
labelTable = dict()			# 라벨을 저장하기위한 labelTable의 형식을 dict타입으로 선언

# store all source code in class
srcCode = list()			# 모든 소스코드를 저장하기 위한 srcCode는 리스트 타입으로 선언
# store all source code in str
originalSrcCode = list()

#
class instr:
	opcode = int()		# 명령어를 받기위한 opcode는 int타입
	operand = tuple()	# 파라미터들을 받는 operand는 tuple타입(파라미터 갯수가 다르므로)

	def __init__(self, opcode, operand):
		self.opcode = opcode
		self.operand = operand

i = 0
# extract label			# handle안에 있는 내용들을 한줄씩 가져온다.
for s in readHandle:
	originalSrcCode.append(s[:-1])
	tmp = s.split()		# 각 줄의 소스코드를 split()를 이용하여 쪼갠다.
	if len(tmp) == 0:	# 빈줄일 경우 무시
		continue
	elif s[0] is not '\t' and s[0] is not ' ':	# 만약 첫번째(라벨의 위치)가 공백이 아닐 경우
		labelTable[tmp[0]] = i		# 라벨을 key로 라벨이 위치한 줄번호를 Value로 labelTable에 저장
		srcCode.append(tmp[1:])		# 라벨을 제외한 부분은 srcCode에 append
	else:
		srcCode.append(tmp)			# 첫번째가 공백일 경우 그냥 srcCode에 append
	i += 1

# add special label
#기존의 정의된 것이기에 임의로 음수로 처리
labelTable["lf"] = -1
labelTable["write"] = -2
labelTable["read"] = -3
labelTable["addFloat"] = -4
labelTable["subFloat"] = -5
labelTable["mulFloat"] = -6
labelTable["divFloat"] = -7
labelTable["modFloat"] = -8
labelTable["negFloat"] = -9
labelTable["F2I"] = -10
labelTable["I2F"] = -11
labelTable["writeF"] = -12
labelTable["writeC"] = -13
labelTable["writeT"] = -14
labelTable["writeD"] = -15


# define opcodes list and build dict
#우선 opCodes에 모든 Ucode명령어를 넣는다.
opCodes = ["notop", "neg", "inc", "dec", "dup", "add", "sub", "mult", "div", "mod", \
	"swp", "and", "or", "gt", "lt", "ge", "le", "eq", "ne", "lod", "str", "ldc", \
	"lda", "ujp", "tjp", "fjp", "chkh", "chkl", "ldi", "sti", "call", "ret", "retv", \
	"ldp", "proc", "end", "nop", "bgn", "sym", "dump"]

# opCodeDict는 위에서 정의한 opCodes에 있는 문자로된 Opcode를 Key로 하고 그것에 대한 Integer 값을 Value로 갖는 dict타입 
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
	op = opCodeDict[tmpList[0]]		# 해당 Opcode에 대한 번호를 op이 가짐
	staticInstrCount[op] += 1

	## 파라미터의 개수를 기준으로 나눈다 ##

	# no parameter
	# 파라미터가 없을 경우, 파라미터부분에 None(파라미터를 가지지 않음을 나타냄)으로 해서 instr 형태로 scrCode에 저장.
	if (0 <= op <= 18) or op in [28, 29, 31, 32, 33, 35, 36, 39]:
		srcCode[i] = instr(op, None)

	# 3 parameter
	# 정수형 파라미터가 3개 있는 경우, 파라미터부분에는 3개의 값들이 오는데
	# tmpList는 String이므로 int형으로 바꿔주고 3개를 묶어 튜플상태로 해서 instr 형태로 scrCode에 저장.
	elif op == 38 or op == 34:
		srcCode[i] = instr(op, (int(tmpList[1]), int(tmpList[2]), int(tmpList[3])))

	# 1 integer parameter
	# 정수형 파라미터가 1개 있는 경우
	elif op in [21, 26, 27, 37]:
		srcCode[i] = instr(op, (int(tmpList[1]), ))
		# if op is bgn
		# bgn(op=37)의 경우 bgn이 위치한 줄의 번호가 pc가 된다.
		if op is 37:
			pc = i

	# 1 label parameter
	# 파라미터가 1개있는 경우, 1개인 파라미터가 라벨인 경우
	elif op in [23, 24, 25, 30]:
		srcCode[i] = instr(op, (labelTable[tmpList[1]], ))

	# 2 parameter
	# 정수형 파라미터가 2개 있는 경우
	else:
		srcCode[i] = instr(op, (int(tmpList[1]), int(tmpList[2])))


# 소스 코드 출력
writeHandle.write("Line\t object\t\t ucode source program\n\n")
for i, l in enumerate(srcCode):
	writeHandle.write("{0:3}\t({1}  {2})\t{3}\n".format(i, l.opcode, l.operand, originalSrcCode[i]))


class Stack:
	arr = list()
	# 아무것도 저장되지 않을 경우
	sp = -1

	# 생성자
	# 스택의 크기 설정
	def __init__(self, size):
		self.arr = [0]*size

	# Top에있는 것을 꺼내기 위함
	def pop(self):
		self.sp -= 1
		return self.arr[self.sp + 1]

	# 현재 Top+1을 한곳에 값을 넣는다.
	def push(self, val):
		self.sp += 1
		# 만약, sp가 arr길이보다 클 경우 arr을 추가 할당
		if self.sp >= len(self.arr):
			self.arr.append(val)
		# 아닌 경우 sp가 위치하는 곳에 값을 넣는다.
		else:
			self.arr[self.sp] = val

	# 원하는 위치에 값을 가져오기 위한 함수
	def __getitem__(self, i):
		if i < 0:
			# sp에서의 음수 인덱스의 값을 가져오기위해서
			# 예 (실제로 -1일 경우, arr에서 가장뒤에 위치하므로 i = sp+1+(-1)
			i += self.sp + 1
		return self.arr[i]

	# 원하는 위치에 값을 넣기 위한 함수
	def __setitem__(self, i, value):
		if i >= 0:
			self.arr[i] = value
		else:
			# sp에 있는 곳에 값을 설정
			self.arr[self.sp + i + 1] = value

	# sp를 설정해주기위한 함수
	def setSP(self, val):
		# sp가 위치할 곳이 아직 할당받지 않은 곳이라면
		if val >= len(self.arr):
			# arr 추가 할당
			self.arr.extend([0] * (val - len(self.arr) + 1))
		self.sp = val

stack = Stack(10)

# 함수시작주소를 알기위해 
curntFuncStartP = int()

# ldp를 할경우에 해당부분의 시작주소를 알기위해
spBackUp = int()

# input buffer
buffer = list()



# 자기가 원하는 주소를 찾아주는 함수
def findAddress(address):
	tmp = curntFuncStartP	# 현재함수의 시작주소를 tmp에 저장

	# 만약 0번째 블록을 접근하려고 할 경우의 예외처리
	if tmp < 0 or (address[0] == 0):
		print("wrong memory access")
		exit(1)
	# operand[0](블록번호)와 같은 block 번호를 가질 때 까지 반복 
	while address[0] != stack[tmp + 3]:
		tmp = stack[tmp]	# 시작주소에 있는 값(Lexical-1과 같은 block번호를 갖는 곳의 시작주소)을 tmp에 저장
		# 음수번째에 접근하려고 할 때의 예외처리
		if tmp < 0:
			print("wrong memory access")
			exit(1)
	return tmp + 4 + address[1]	# 그 block번호를 갖는 함수의 offset(address[1])에 해당되는 주소를 리턴


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
		# operand에 해당되는 stack에서의 주소
		address = findAddress(operand)
		# stack에서 address에 해당되는 곳에 값을 가져온다.
		value = stack[address]
		# 그리고 그 값을 다시 top에 push
		stack.push(value)
	# str
	# operand에 해당되는 stack의 주소에 가장 위에 값을 넣어준다.
	elif op == 20:
		# operand에 해당되는 stack에서의 주소
		address = findAddress(operand)
		# stack에서 address에 해당되는 곳에 top에 있는 값을 저장
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
		address = stack.pop()		# 현재 top에 있는 값을 주소로
		stack.push(stack[address])	# 그 주소에 맞는 곳의 값을 top에 다시저장
	# sti
	elif op == 29:
		dataToSave = stack.pop()	# 현재 top에 있는 값을 dataToSave에 넣고
		address = stack.pop()		# 그다음에 top에 있는 값을 주소로 설정
		stack[address] = dataToSave	# stack에서 해당 주소에 있는 곳에 dataToSave 값을 넣는다.
	# call
	elif op == 30:
		# lf 줄바꿈
		if operand[0] == -1:
			writeHandle.write("\n")

		# write 마지막 값 출력 
		elif operand[0] == -2:
			writeHandle.write("{0} ".format(stack[-1]))
			stack.setSP(spBackUp - 1)

		# read 
		elif operand[0] == -3:
			while len(buffer) == 0:	# 버퍼에 값이 없는 동안
				# map을 이용하여 split()로 나누어진 입력값 들을 각각 int함수로 취하고, list형식으로 buffer에 저장 
				buffer = list(map(int, input().split()))
			address = stack.pop()			# top에 있는 값을 가져와 address로하고
			stack[address] = buffer.pop(0)	# stack에서 그 address에 해당하는 부분에 버퍼에 첫번째있는 것을 pop해서 넣는다.
			stack.setSP(spBackUp - 1)

		# addFloat 실수 두개 더함
		elif operand[0] == -4:
			s = struct.pack('>i', stack[-1])
			r1 = struct.unpack('>f', s)[0]
			s = struct.pack('>i', stack[-2])
			r2 = struct.unpack('>f', s)[0]

			result = r1 + r2

			s = struct.pack('>f', result)
			r = struct.unpack('>i', s)[0]
			stack.setSP(spBackUp - 1)
			stack.push(r)

		# subFloat 실수 두개 뺌
		elif operand[0] == -5:
			s = struct.pack('>i', stack[-1])
			r1 = struct.unpack('>f', s)[0]
			s = struct.pack('>i', stack[-2])
			r2 = struct.unpack('>f', s)[0]

			result = r1 - r2

			s = struct.pack('>f', result)
			r = struct.unpack('>i', s)[0]
			stack.setSP(spBackUp - 1)
			stack.push(r)

		# mulFloat 실수 두개 곱함
		elif operand[0] == -6:
			s = struct.pack('>i', stack[-1])
			r1 = struct.unpack('>f', s)[0]
			s = struct.pack('>i', stack[-2])
			r2 = struct.unpack('>f', s)[0]

			result = r1 * r2

			s = struct.pack('>f', result)
			r = struct.unpack('>i', s)[0]
			stack.setSP(spBackUp - 1)
			stack.push(r)

		# divFloat 실수 두개 나눔
		elif operand[0] == -7:
			s = struct.pack('>i', stack[-1])
			r1 = struct.unpack('>f', s)[0]
			s = struct.pack('>i', stack[-2])
			r2 = struct.unpack('>f', s)[0]

			result = r1 / r2

			s = struct.pack('>f', result)
			r = struct.unpack('>i', s)[0]
			stack.setSP(spBackUp - 1)
			stack.push(r)

		# modFloat 실수 두개 mod연산
		elif operand[0] == -8:
			s = struct.pack('>i', stack[-1])
			r1 = struct.unpack('>f', s)[0]
			s = struct.pack('>i', stack[-2])
			r2 = struct.unpack('>f', s)[0]

			result = r1 % r2

			s = struct.pack('>f', result)
			r = struct.unpack('>i', s)[0]
			stack.setSP(spBackUp - 1)
			stack.push(r)

		# negFloat 실수 부호 바꿈
		elif operand[0] == -9:
			s = struct.pack('>i', stack[-1])
			r1 = struct.unpack('>f', s)[0]

			r1 = -r1

			s = struct.pack('>f', r1)
			r = struct.unpack('>i', s)[0]
			stack.setSP(spBackUp - 1)
			stack.push(r)

		# F2I 실수를 정수로
		elif operand[0] == -10:
			s = struct.pack('>i', stack[-1])
			r1 = struct.unpack('>f', s)[0]

			r1 = int(r1)

			stack.setSP(spBackUp - 1)
			stack.push(r1)

		# I2F 정수를 실수로
		elif operand[0] == -11:
			val = float(stack[-1])

			s = struct.pack('>f', val)
			r1 = struct.unpack('>i', s)[0]

			stack.setSP(spBackUp - 1)
			stack.push(r1)

		# writeF 실수 출력
		elif operand[0] == -12:
			s = struct.pack('>i', stack[-1])
			r1 = struct.unpack('>f', s)[0]

			writeHandle.write("{0} ".format(r1))
			stack.setSP(spBackUp - 1)

		# writeC 문자 출력
		elif operand[0] == -13:
			writeHandle.write("{0} ".format(chr(stack[-1])))
			stack.setSP(spBackUp - 1)

		# writeT time타입 출력
		elif operand[0] == -14:
			hour = stack[-1] // 3600
			minute = stack[-1] % 3600 // 60
			sec = stack[-1] % 60
			writeHandle.write("{0}:{1}:{2} ".format(hour, minute, sec))
			stack.setSP(spBackUp - 1)

		# writeD date타입 출력
		elif operand[0] == -15:
			days = stack[-1]
			d = (datetime.datetime.min + datetime.timedelta(days)).date()
			writeHandle.write("{0}/{1}/{2} ".format(d.year, d.month, d.day))
			stack.setSP(spBackUp - 1)

		else:
			stack[spBackUp + 2] = pc + 1			# 돌아올 위치(call 바로 밑에 라인넘버인 곳)를 저장해둠
			stack[spBackUp + 1] = curntFuncStartP	# 이전 블락의 시작위치
			curntFuncStartP = spBackUp				# 현재 함수의 시작위치를 curntFuncStartP로 설정
			pc = operand[0] - 1		# 해당 함수(라벨)의 srcCode의 시작위치로 pc를 해둔다. while할때마다 +1을 해주기 때문에 -1을 해주는 것이다.
	# ret
	elif op == 31:
		stack.setSP(curntFuncStartP - 1)			# 현재 함수를 사라지게 하기 위한 sp설정
		pc = stack[curntFuncStartP + 2] - 1			# 다시 돌아갈 PC값으로 PC설정
		curntFuncStartP = stack[curntFuncStartP + 1]# 이전 블락의 시작주소를 curntFuncStratP로 해둠.( call하기 이전인 곳의 시작주소로 설정)
	# retv
	elif op == 32:
		tmp = stack[-1]						#  현재 함수의 마지막 값을 tmp에저장
		stack.setSP(curntFuncStartP - 1)	# 현재 함수를 사라지게 하기 위한 sp설정
		stack.push(tmp)					# 현재 함수의 마지막 값을 다시 설정된 SP에 push
		pc = stack[curntFuncStartP + 2] - 1	# 다시 돌아갈 PC값으로 PC설정
		spBackUp = stack[curntFuncStartP + 4]
		# 이전 블락의 시작주소를 curntFuncStratP로 해둠.( call하기 이전인 곳의 시작주소로 설정)
		curntFuncStartP = stack[curntFuncStartP + 1]
	# ldp
	elif op == 33:
		tmp = spBackUp
		spBackUp = stack.sp + 1		# 해당 함수의 시작위치를 저장하기 위해
		stack.setSP(stack.sp + 5)	# 해당 함수의 정보를 저장하기 위해서
		stack[spBackUp + 4] = tmp
	# proc
	elif op == 34:
		stack[curntFuncStartP + 3] = operand[1]			# 자신의 블록넘버를 넣기 위해
		stack.setSP(curntFuncStartP + operand[0] + 4)	# 할당 받을 량만큼 sp를 늘려준다.
		tmp = stack[curntFuncStartP + 1]				# 이전 블락의 시작주소
		while operand[2] - 1 != stack[tmp + 3]:	# 현재 Lexical-1과 같은 블락번호를 같아질때까지 반복
			tmp = stack[tmp]					# 이전 블락의 시작주소에 해당하는 값을 tmp에 넣어둔다
		stack[curntFuncStartP] = tmp			# 현재 Lexical-1과 같은 블락번호를 같는 곳의 시작주소
	# end
	# 프로그램 종료
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
		stack.push(1)
		stack.setSP(stack.sp + operand[0])	# stack.sp= 3 + bgn의 파라미터
	# sym
	# 현재 코드에서는 의미없음
	elif op == 38:
		pass
	# dump
	# 만들어 낸 opCode(현재 Stack에 있는 값들을 보기위함)
	elif op == 39:
		for i, v in enumerate(stack.arr):
			if i > stack.sp: break
			# stack에서의 위치와 해당위치의 값을 출력
			print("({0}, {1})".format(i, v), end=' ')
		print("")

	#반복할때마다 pc+1
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