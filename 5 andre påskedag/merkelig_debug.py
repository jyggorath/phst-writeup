#!/usr/bin/python3
import sys
import os

digits = {"🎲": 0, "🍫": 1,  "🎮": 2, "🎧": 3, "🎨": 4, "🍬": 5}
base = len(digits)

def parse_num(code):
	num = 0
	for i,c in enumerate(code):
		num += digits[c] * base**i
	return num


# ############################################################
def resolve_emoji(e):
	if e == '🐰':	return 'PSH'	# Push output on stack
	elif e == '🐤':	return 'OUT'	# Output to STDOUT from stack
	elif e == '🐣':	return 'IN '	# Read user input from STDIN
	elif e == '🌻':	return 'DEC'	# Decrease/subtract stack value (and do modulus)
	elif e == '🌱':	return 'INC'	# Increas/add to stack value (and do modulus)
	elif e == '🥚':	return 'XOR'	# XOR on stack value
	elif e == '🐥':	return 'CPY'	# Copy stack value to other stack index
	elif e == '🐇':	return 'JMP'	# Jump using code pointer (pc)
	elif e == '🌞':	return 'EXI'	# Exit condition
	else:			return '   '

def get_chr(c):
	try:
		if '\\x' in chr(c).__repr__():
			return '.'
		if chr(c) == '\n' or chr(c) == '\t' or chr(c) == '\r':
			return ' '
		else:
			return chr(c)
	except ValueError:
		return '.'

def int_to_str(i, l):
	s = str(i)
	while len(s) < l:
		s = ' ' + s
	return s

def dump_stack(op, sp, pc, stack):
	print(resolve_emoji(op) + ' ' + int_to_str(sp, 2) + ' ' + int_to_str(pc, 4) + ' ', end='')
	for s in stack:
		print(get_chr(s), end='')
	print('')

def get_ascii_beforafter(val):
	return str(val) + '/' + get_chr(val)

def dump_operation(op, operation, val1, operator, val2, doval2=True):
	if doval2:
		print('  %s: %s: %s %s %s  =>  ' % (resolve_emoji(op), operation, get_ascii_beforafter(val1), operator, get_ascii_beforafter(val2)), end='')
	else:
		print('  %s: %s: %s %s %s  =>  ' % (resolve_emoji(op), operation, get_ascii_beforafter(val1), operator, val2), end='')
def dump_operation_result(val):
	print(get_ascii_beforafter(val))
def dump_flow_fail(failval, counter, sp, pc):
	print('!  JMP Fail after ' + str(counter) + ' successful operations: stack[sp] is ' + get_ascii_beforafter(failval) + ', should be 0. sp=' + str(sp) + ', pc=' + str(pc))
# ############################################################


if len(sys.argv) < 2:
	print("Mangler programfil!")
	exit(1)

code = open(sys.argv[1], "rt", encoding="utf8").read()
pc = 0
prev_op = ''

stack = [0] * 256
sp = 0

flowchange_counter = 0
print('Emo  SP  PC  Stack')
print('='*268)

while pc < len(code):
	op = code[pc]
	pc += 1
	dump_stack(op, sp, pc, stack)
	
	if op == "🐰": # PSH
		stack[sp] = parse_num(code[pc:pc+4])
		sp += 1
		pc += 4
	elif op == "🐥": # CPY
		stack[sp] = stack[sp-1]
		sp += 1
	elif op == "🌱":# INC
		sp -= 1
		
		# Uncomment to view operation and changes
		dump_operation(op, 'stack[sp-1] += stack[sp]', stack[sp-1], '+=', stack[sp])
		stack[sp-1] += stack[sp]
		dump_operation_result(stack[sp-1])

		# Uncomment to view operation and changes
		dump_operation(op, 'stack[sp-1] %= base**4', stack[sp-1], '%=', base**4, doval2=False)
		stack[sp-1] %= base**4
		dump_operation_result(stack[sp-1])
	elif op == "🌻": # DEC
		sp -= 1

		# Uncomment to view operation and changes
		dump_operation(op, 'stack[sp-1] -= stack[sp]', stack[sp-1], '-=', stack[sp])
		stack[sp-1] -= stack[sp]
		dump_operation_result(stack[sp-1])
		
		# Uncomment to view operation and changes
		dump_operation(op, '', stack[sp-1], '%=', base**4, doval2=False)
		stack[sp-1] %= base**4
		dump_operation_result(stack[sp-1])
	elif op == "🐇": # JMP
		sp -= 1
		if stack[sp] != 0:
			dump_flow_fail(stack[sp], flowchange_counter, sp, pc)
			pc += parse_num(code[pc:pc+4])
		else:
			pc += 4
			flowchange_counter += 1
	elif op == "🥚": # XOR
		sp -= 1
		# Uncomment to view operation and changes
		dump_operation(op, '', stack[sp-1], '^=', stack[sp])
		stack[sp-1] ^= stack[sp]
		dump_operation_result(stack[sp-1])
	elif op == "🐤": # OUT
		sp -= 1
		# Uncomment to enable "normal" output
		# os.write(1, bytes([stack[sp]]))
	elif op == "🐣": # IN
		line = sys.stdin.buffer.readline().strip()
		for c in line:
			stack[sp] = c
			sp += 1
		stack[sp] = len(line)
		sp += 1
	elif op == "🌞": # EXI
		exit(0)
	
	prev_op = op

