import sys
from time import sleep
import re
import json

slp=50
nastmp=""
inputFile="nope"
compiledOut=False
compiledOutFile=False
coGiven=False
if len(sys.argv)>2:
	nastmp=sys.argv[2]
	inputFile=sys.argv[1]
else:
	raise ValueError("Not enough arguments given")

codestr=""
nastro=[]
index=0
state=0
instructions={}
acts=0

shownrange=40

if "-f" in sys.argv: # Gets input file name
	inputFile=sys.argv[sys.argv.index("-f")+1]
	if sys.argv.index("-f") < 3:
		if not "-n" in sys.argv:
			raise ValueError("Input not given")

if "-n" in sys.argv: # Gets the input text
	nastmp=sys.argv[sys.argv.index("-n")+1]

if "-s" in sys.argv: # Gets the delay in ms between the actions
	slp=float(sys.argv[sys.argv.index("-s")+1])
	if sys.argv.index("-s") < 3:
		if not "-n" in sys.argv:
			raise ValueError("Input not given")

if "-c" in sys.argv: # Gets the raw input code to execute
	codestr=sys.argv[sys.argv.index("-c")+1]
	if sys.argv.index("-c") < 3:
		if not "-n" in sys.argv:
			raise ValueError("Input not given")

if "-o" in sys.argv: # If you want raw compiled text put the "-o" option
	compiledOut=True
	try:
		if sys.argv[sys.argv.index("-o")+1].endswith(".json"):
			compiledOutFile=True
	except IndexError:
		pass
	if sys.argv.index("-o") < 3:
		if not "-n" in sys.argv:
			raise ValueError("Input not given")

if "-ci" in sys.argv: # If you want to run an already compiled code
	with open(sys.argv[sys.argv.index("-ci")+1], "r") as f:
		#print(f.read())
		instructions = json.load(f)
	coGiven=True


for l in nastmp:
	nastro.append(l.upper())


def getRange(s): # Decodes string into a string range (0..9 => 0123456789, 0..9ab => 0123456789ab)
    if ".." not in s:
        return s
    parti = s.split("..", 1)
    
    rr = ""
    for i in range(ord(parti[0][-1]), ord(parti[1][0]) + 1):
        rr += chr(i)
    return parti[0][:-1] + rr + parti[1][1:]

def pnastro(): # Prints the formatted tape 
	print("Nastro: ", end="")
	expected=2*shownrange+1
	for l in range(len(nastro)):
		if(l == index):
			print(mainBG+nastro[l].replace("-", " "), end="")
			expected-=1
		else:
			if(abs(index-l)<shownrange):
				print(normalBG+nastro[l].replace("-", " "), end="")
				expected-=1
	for i in range(expected):
		print(normalBG+" ", end="")
	print(resetBG,"Stato: ",state, end="         \r")

# Sets the colors to display in the formatted tape
# White: 7, blue: 44, red: 41, green: 42, yellow: 43, magenta: 45, cyan: 46
mainBG="\033[41m"
normalBG="\033[44m"
resetBG="\033[0m"

pattern = r"^\(([^,()\[\]{}]+,){4}[<>/ -]\)$" # Pattern to recognize in the code
instructionsRaw=[]
try:
	with open(inputFile, "r") as f:
		instructionsRaw=f.readlines() # Tries to read an input file if possible
except:
	pass

if codestr: # If a raw code string is given, it's used (if both a file and raw code are given, the raw code will be chosen)
	if ";" in codestr:
		instructionsRaw=codestr.split(";")
	else:
		instructionsRaw=codestr.split("\n")


if not coGiven: # Checks if a compiled code has already been given
	for rawIst in instructionsRaw: # Reads every instruction
		ist=rawIst.split("#")[0] # Removes any comment if present
		if re.match(pattern, ist.strip()): # Checks if the line is a valid pattern. If it isn't it just skips the line
			instruction=ist.upper().strip()
			raw=instruction.replace("\n", "")[1:-1].split(",")
			raw[1]=getRange(raw[1])
			raw[3]=getRange(raw[3])
			if raw[0] not in instructions: # Puts the instruction in the formatted instruction set
				instructions[raw[0]] = {}
			if len(raw[1])>1: # If a range is given as an option in the code, it's checked here
				for r in range(len(raw[1])):
					if len(raw[3]) == 1:
						instructions[raw[0]][raw[1][r]]=raw[2:]
					elif len(raw[3]) == len(raw[1]):
						instructions[raw[0]][raw[1][r]]=[raw[2], raw[3][r], raw[4]]
					else:
						raise ValueError("invalid range - "+instruction)
			elif len(raw[3]) > 1:
				raise ValueError("Invalid range - "+instruction)
			else:
				instructions[raw[0]][raw[1]] = raw[2:]

if compiledOut:
	co=json.dumps(instructions, indent=4, sort_keys=True)
	if compiledOutFile:
		with open(sys.argv[sys.argv.index("-o")+1], "w") as w:
			w.write(co)
	else:
		print("==== Compiled code ====")
		print(co)
		print("======= Output ========")

running=True
pnastro()
sleep(slp/1000)
while running:
	for r in range(len(nastro)):
		nastro[r]=nastro[r].replace(" ","-") # Cleans the tape
	if str(state) in instructions: # Checks if the actual state is a valid state. If it isn't it ends the program
		if nastro[index] in instructions[str(state)]: # Checks if the current tape element is a valid input in the given case. If it isn't it ends the program
			nn=instructions[str(state)][nastro[index]][1] # Gets the new value for the tape
			oi=index # Gets the new index
			if instructions[str(state)][nastro[index]][2] == "<": # Checks if it needs to move left
				if index == 0: # If it's at the very beginning of the tape, it adds one element to the left and shifts the new index by one
					nastro=["-"]+nastro
					oi+=1
				else:
					index-=1
			elif instructions[str(state)][nastro[index]][2] == ">": # CHecks if it needs to move right
				if index == len(nastro)-1: # If it's at the end of the tape it adds one element to the right
					nastro.append("-")
				index+=1
			elif instructions[str(state)][nastro[index]][2] == "-": # Checks if it needs to stay where it is
				index=index
			else:
				raise ValueError("Unsupported movement - "+instructions[str(state)][nastro[index]][2]) # If it's not a valid movement it throws an error
			state=instructions[str(state)][nastro[oi]][0] # Writes in the new state
			nastro[oi]=nn # Writes in the new value
			acts+=1
		else:
			running=False
	else:
		running=False

	pnastro() # Prints the tape
	#print(nastro, end="           \r")
	sleep(slp/1000) # Pauses for slp milliseconds

print("\nEnded with",acts,"actions")
