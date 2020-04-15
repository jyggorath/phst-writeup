#!/usr/bin/python3
from var_dump import var_dump

digits = {"🎲": 0, "🍫": 1,  "🎮": 2, "🎧": 3, "🎨": 4, "🍬": 5}
base = len(digits)

def parse_num(code):
	num = 0
	# i: iterator: 0->
	# c: foreach var
	for i,c in enumerate(code):
		num += digits[c] * base**i
	return num

# 0 -> 1295
print('Min: ' + str(parse_num('🎲🎲🎲🎲')))
print('Max: ' + str(parse_num('🍬🍬🍬🍬')))
