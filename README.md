# Python turing simulator

A compact and lightweight way to run Turing code locally
Syntax should be fully compatible with [turingsimulator.net](https://www.turingsimulator.net)

---

To run `python3 main.py inputFileName.tur inputTape`

Input file syntax `(initial state, reading value, final state, write value, movement)`
Acceptable movements: `<`, `-` and `>`
Comments available after the `#` character

Value ranges: `0..9` => `0123456789`, `0..9qse` => `0123456789qse`

---

### Valid options
1. `-f` input file name
2. `-n` input tape
3. `-c` raw input code (supports both new lines and inline with ; as a separator are accepted)
4. `-s` delay between actions (ms)
5. `-o` prints the compiled json code (if a file is specified it writes the compiled code inside of it)
6. `-ci` Runs the already compiled code from a specified json file

---

### Example code

```turing
(0,0,0,1,>) # State 0, if it reads 0 it writes 1, moves to the right and stays in state 0.
(0,1,0,0,>) # State 0, if it reads 1 it writes 0, moves to the right and stays in state 0.
(0,-,e,-,-) # State 0, if it reads nothing (-) it has arrived to the end of the number, it writes nothing, stays still and goes in the final state (e)
```

Input tape: `0101`
Output tape: `1010`

---

### Usage example

To run with raw code: `python3 main.py -c "(0,0,0,1,>);(0,1,0,0,>);(0,-,e,-,-)" -s 0 -n 1010`

To run with code file: `python3 main.py input.tur 1010` or `python3 main.py -f input.tur -n 1010`

To run with just the compiled code output: `python3 main.py input.tur 1010 -o`

To write the compiled code into a file: `python3 main.py input.tur 1010 -o compiled.json` (It has to be a json file for the code to work)

To run a pre-compiled code: `python3 main.py -ci compiled.json -n 1010`
