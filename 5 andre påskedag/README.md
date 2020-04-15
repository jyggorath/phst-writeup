# Andre påskedag
30 points

### Table of contents
1. [The Task](#the-task)
2. [The code](#the-code)
	1. [General](#general)
	2. [Input and output](#input-and-output)
	3. [The magic parts](#the-magic-parts)
	4. [Other](#other)
3. [Solution](#solution)
	1. [Modifications and "debugging"](#modifications-and-debugging)
	2. [Controlling the flow](#controlling-the-flow)

## The Task
>Oppdatert påskevurdering: Det er “sannsynlig” at det blir en god påske. Påske HAREN er friskmeldt.
>
>Basert på tidligere innsamlet informasjon, har påskekyllingbetjentene lagt sammen både to og tre, og funnet fram til hvor de stjålne eggene blir oppbevart. Når de ankommer stedet oppdager de imidlertid at adgang til lokalet er styrt av et hjemmelaget og hittil ukjent adgangssystem.
>
>Påskekyllingbetjentene har klart å koble seg på systemet og fått lastet ned to filer, men skjønner lite av det de ser. Kan du hjelpe de med å få tilgang?
>
>Flaggformat: PHST{tekst her}

[Attachment: merkelig.py](merkelig.py)

[Attachment: underfundig](underfundig)

[Attachment: paskekyllingbetjenter.png](paskekyllingbetjenter.png)

## The code
The task at hand is to figure out how merkelig.py works in combination with the file "underfundig". The paskekyllingbetjenter.png image is not used for anything.

### General
The Python code is at first glance relatively simple 60 or so lines of code. The file "underfundig" contains a single looong line of emojis.

This is the result of running the code. It prompts for a password, and tells you it's wrong in Norwegian:
```
user@host:~/phst$ python3 ./merkelig.py underfundig
Passord: password123
Ikke riktig :(
user@host:~/phst$
```

One of the firs things the code does, is read the content of "underfundig", declare a list of zeroes, and two additional int variables holding zeroes:

```python
code = open(sys.argv[1], "rt", encoding="utf8").read()
pc = 0

stack = [0] * 256
sp = 0
```

Note the naming of the variables, and how they're grouped together. From the rest of the code, it is apparent that if the list is a "stack", then the `sp` variable would be a stack pointer. I can't think of a better description for `pc` than "code pointer.

The main part of the code consists of a while loop. Here is the loop condition, as well as the first part:

```python
while pc < len(code):
    op = code[pc]
    pc += 1
```

So, for each iteration, it selects an emoji from `code` and puts into the `op` variable.

The next part of the while loop is a switch-case-like list of if-elif's to tell the code to do various things depending on what emoji `op` contains in the current iteration. I'm not going to list them all, [view the raw file](merkelig.py) if you want to.

### Input and output
The following if-case is responsible for pushing values on the stack, based on the current value of `pc`.

```python
if op == "🐰":
	stack[sp] = parse_num(code[pc:pc+4])
	sp += 1
	pc += 4
```

Here's the parse_num function and the global variables it depends on:

```python
digits = {"🎲": 0, "🍫": 1,  "🎮": 2, "🎧": 3, "🎨": 4, "🍬": 5}
base = len(digits)

def parse_num(code):
    num = 0
    for i,c in enumerate(code):
        num += digits[c] * base**i
    return num
```

`parse_num` is only ever called with `code[pc:pc+4]` as argument, so it only retrieves integer values based on the current value of `pc`. The values of `digits` and `base` never change. When called from `op == "🐰"`, the ints returned from `parse_num` are almost always valid ASCII codes, in other words, they can serve as printable chars. In that context this function is used to push text onto the stack.

Another thing to note here is that `sp` is incremented. However, in the other if-cases that usually runs in the iterations just after/before this one, `sp` is decremented, meaning the output of `parse_num` are usually always pushed onto the same stack index. Note also that `pc` is increased by 4 here, meaning the loop is not a basic step-for-step iteration, it jumps ahead various distances based on which emoji it hits.

Here's the if-case responsible for generating output:

```python
elif op == "🐤":
	sp -= 1
	os.write(1, bytes([stack[sp]]))
```

This baffled me for a second, as `os.write` is supposed to take a file handle as the first argument. However, based on how the code runs, I can only assume that `1` evaluates to STDOUT, as this function call is used basically as:
```python
print(chr(stack[sp]), end='')
```

Also take note that `sp` is decremented. All the parts of the loop which generates output calls `op == "🐤"` and `op == "🐰"` after each other. This means that all the output resides in the same stack index. The output is printed one char at a time and is then overwritten with the next.

Input is handled by this if-case:

```python
elif op == "🐣":
	line = sys.stdin.buffer.readline().strip()
	for c in line:
		stack[sp] = c
		sp += 1
	stack[sp] = len(line)
	sp += 1
```

What this does, is read a line of input from STDIN, excluding newline, and push it onto the stack starting at `sp` (at the time this if-case is reached, that is *always* 0 (so the beginning of the stack)).
Then, after the input, the length of the input is pushed on the stack as well. So, if the word `"wrong"` where to be given as input, the resulting stack would look like this:
```python
[119, 114, 111, 110, 103, 5, 0, 0, 0, 0, ..., 0]
```
(The first five values are the ASCII codes for `"wrong"`, followed by `5` which is the result of `len("wrong")`, and then the rest is zeroes (which is the default values of the stack indexes)).

### The magic parts
The first "magic" if-case is this one:

```python
elif op == "🐇":
	sp -= 1
	if stack[sp] != 0:
		pc += parse_num(code[pc:pc+4])
	else:
		pc += 4
```

The purpose of this if-case is to increase the "code pointer" `pc`, based on the values on the stack. It will either be increased with the output of `parse_num` (see the details on `op == "🐰"` in [2.2 Input and output](#input-and-output)) which will always be quite much, or 4.

This is perhaps the one if-case that is most "magic", because it effectively controls the "flow" of the code. More on that later.

Next comes two if-cases which does almost exactly the same, but with a small difference. These two if-cases modify the stack, based on the values on the stack:

```python
elif op == "🌱":
	sp -= 1
	stack[sp-1] += stack[sp]
	stack[sp-1] %= base**4
elif op == "🌻":
	sp -= 1
	stack[sp-1] -= stack[sp]
	stack[sp-1] %= base**4
```

The only difference between these two are the difference between `+=` and `-=`.
Short operation description:
1. Decrement stack pointer `sp`.
2. Operate on the *previous* stack index and add/subtract the value of the current stack index.
3. Again, operate on the *previous* stack index, and set it equal to the modulus value of itself modulus `base**4` (note: Because `base` never change, `base**4` will *always* be `1296`).

Next comes two if-cases that also modifies the stack based on the values on the stack, but somewhat simpler:

```python
elif op == "🐥":
	stack[sp] = stack[sp-1]
	sp += 1
```

Everyone should understand this one, but just to do it properly: It copies the value in the current stack index, to the previous one. Then it increments the stack pointer `sp`.

```python
elif op == "🥚":
	sp -= 1
	stack[sp-1] ^= stack[sp]
```

This one decrements the stack pointer `sp`. Then, operating on the previous stack index, it xor's it with the value of the current stack index.

### Other
The only if-case not described already is this one, which is the exit condition:

```python
elif op == "🌞":
    exit(0)
```

## Solution
### Modifications and "debugging"
In order to better track the flow in the code, I modified a copy of the script with additional output to be able to view which if-cases where being run in which order, and view the changes to the stack, as well as `sp` and `pc`.

Here is the resulting script (cleaned up a bit, it was far more nasty while I was actually working on the challenge): [merkelig_debug.py](merkelig_debug.py) (I'm sorry, it's ugly) (Warning: Prints 268 characters pr line, you might need to disable line wrapping/use a big monitor/reduce font size/pipe to file)

As part of the code, I gave each emoji if-case a "name", as emojis doesn't display well in the terminal. Some of the "names" might give associations to assembly, but rest assured they could be called anything, and the operations within have nothing to do with assembly:

```python
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
```

![stackdump.png](stackdump.png?raw=true)

Notice among other things how there is a massive jump in the value of `pc` following the last JMP which "fails", compared to the 4 before. Notice also how the output behaves, both before the input, and after the "failed" JMP.

### Controlling the flow
Remember JMP (`elif op == "🐇":`) in [2.3 The magic parts](#the-magic-parts)? If the checked value on the stack is **not 0**, it adds output from `parse_num` to `pc`, increasing it drastically. However, if the value it checks turns out to be 0, it will only add 4. It turns out that if `pc` is increased using `parse_num`, the flow changes to outputting the error message "Ikke riktig :(" *("Not right :(" in English)*. In other words, the value checked in JMP **have to be 0 if we are to succeed**.

[Initially I wasn't able to get the flow past the first JMP](stackdump_beginningfail.png). However, I noticed that DEC preceded JMP, and that due to the resulting position of the stack pointer `ps` after the input and the first PSH after the input, as well as the first operation in DEC, DEC would end up operating on the stack index that held the length of the user input. And because JMP follows immediately after DEC, this also turns out to be the value that JMP checks.

So how can we get this to be 0? Well, the final operation on DEC is this:
```python
stack[sp-1] %= base**4
```
As stated earlier, `base**4` will **always** be 1296. So, I just had to find which value that results in 0 when modulus'd with 1296. Luckily, it had to be a value in the range 0-255, as it was derived from user input. I'm bad at math, so I solved this by brute forcing:
```
>>> for i in range(255):
...  if i % 1296 == 0:
...    print('Yay: %d' % i)
...
Yay: 0
>>>
```

Whataya know, its 0. So that entire line is practically worthless.

Let's look at the second to last operation in DEC then:
```python
stack[sp-1] -= stack[sp]
```

It sets `stack[sp-1]` equal to itself minus the next (actually current) stack value. So, for the result to be 0, those two stack values need to be the same prior to this operation.

As we can see from [a recreation of my first attempts](stackdump_beginningfail.png), DEC is preceded by PSH. I noticed that the first value pushed on stack following the reading of user input, is **always '"'** (double quote), or 34. The value just before that one, originates from the operations in IN, and is the _length of the user input_. These are the two values that are used in the `-=` operation in DEC.

In other words, to get past the first JMP, **the length of the user input must be 34**.

The second JMP derives the checked value not from a value manipulated only by DEC, but from a value manipulated from the following chain: XOR->INC->DEC (there are other operations involved, but these are the ones that are necessary to track). I therefor placed output functions in these if-cases to better be able to understand what was going on (these are commented out in the published version of the script):

[Visual explanation](op_details_wred.png) (and a [version without the markings](op_details_.png) so everything is plainly visible)

So, what happens to the user input, is that in XOR it is XORed with a value that changes for each iteration. Then, in INC, 42 is added to the result from XOR. Then, in DEC, a value that changes for each iteration is subtracted. If the result is 0, the user input that was used in XOR was correct.

The XOR if-case contains an XOR operation like this: `a ^= b`. `a` *after* the XOR operation is known, it is the value in `stack[sp-1]` from `stack[sp-1] += stack[sp]` in INC. `b` change for each iteration, but always to the same values, so it can be found easily by dumping from the stack. The unknown here is what the value of `a` should be *before* the XOR operation.

As stated earlier, I'm bad at math, so I prefer to just bruteforce my way through such problems. Where `xor_with` is `b`, and `target_val` is `a` *after*:
```python
for i in range(256):
	if i ^ xor_with == target_val:
		print('Input: ' + chr(i))
		break
```

Here is the procedure for finding the correct user input:
1. Find the value that is subtracted in DEC (`stack[sp]`)
2. Find the result of the value from step 1, minus 42.
3. Put the result from step 2, and the `xor_with` value into the XOR bruteforce script and run it. The Resulting character should be the next correct char in the user input.

And one more thing: All this is done in reverse. The first step is to input 34 characters (can be all A's for instance), after running through the procedure you will get the last correct character, and then once more the second to last character, and so on, until you have them all.

**The flag is:** `PHST{Mitt navn er Gwyn. Pen Gwyn.}`

*Final note: Compared to the other challenges, this one was quite challenging. I'm sure there is a **much** more efficient way to solve it, perhaps automate it more. But this is the way I actually solved it, I'm not gonna pretend I solved it in a smarter way than what I actually did.*