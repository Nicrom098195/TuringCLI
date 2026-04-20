package main

import (
	"fmt"
	"os"
	"bufio"
	"strings"
	"log"
	"time"
	"strconv"
	"regexp"
)

const mainBG="\033[41m"
const normalBG="\033[44m"
const fillBG="\033[44m"
const resetBG="\033[0m"

var pattern = regexp.MustCompile(`^\(([^,()\[\]{}]+,){4}[<>/ -]\)$`)

func expandRanges(s string) string {
	var result strings.Builder
	i := 0
	for i < len(s) {
		// Cerca il pattern X..Y a partire da i
		if i+3 < len(s) && s[i+1] == '.' && s[i+2] == '.' {
			start := s[i]
			end := s[i+3]
			if end >= start {
				for c := start; c <= end; c++ {
					result.WriteByte(c)
				}
				i += 4
				continue
			}
		}
		result.WriteByte(s[i])
		i++
	}
	return result.String()
}

func abs(n int) int{
	if n>0{
		return n
	}
	return -n
}

func ptape(tape []string, index int, state string, move int){
	fov := 30

	if index < fov{
		for i := 0; i<(fov-index); i++{
			fmt.Print(fillBG)
			fmt.Print(" ")
		}
	}
	for i := 0; i<len(tape); i++{
		if i == index{
			fmt.Print(mainBG)
			fmt.Print(strings.Replace(strings.ToUpper(tape[i]), "-", " ", -1))
		}else{
			if abs(i-index) < fov{
				fmt.Print(normalBG)
				fmt.Print(strings.Replace(strings.ToUpper(tape[i]), "-", " ", -1))
			}
		}
		
	}

	if (len(tape)-index) < fov{
		for i := 0; i<(fov-(len(tape)-index)); i++{
			fmt.Print(fillBG)
			fmt.Print(" ")
		}
	}

	fmt.Print(resetBG)
	fmt.Print(" State: ")
	fmt.Print(state)
	fmt.Print(" ")
	fmt.Print(move)
	fmt.Print("              \r");
}

func main(){
	// os.Args[n]

	if len(os.Args) < 3{
		fmt.Println("Error: not enough arguments")
		return
	}

	fname:=string(os.Args[1])

	// Initializes the tape

	tape:=make([]string, 0)

	state := "0"
	index := 0

	itape:=os.Args[2]

	ms := 50

	/*if len(os.Args)>3{
		var err error
		ms, err = strconv.Atoi(os.Args[3])
		if err != nil {
    		log.Fatal(err)
		}
	}*/


	// Checks for other arguments given
		for i := 1; i<(len(os.Args)-1); i++{
			ag := os.Args[i]

			/*fmt.Print("Checking arg ")
			fmt.Print(i)
			fmt.Print(" (")
			fmt.Print(ag)
			fmt.Println(")")*/

			if ag == "-n"{
				itape = os.Args[i+1]
			}else if ag == "-f"{
				fname = os.Args[i+1]
			}else if ag == "-s"{
				var err error
				ms, err = strconv.Atoi(os.Args[i+1])
				if err != nil {
	    			log.Fatal(err)
				}
			}
		}


	for i:=0; i<len(itape); i++{
		tape=append(tape, strings.ToLower(string(itape[i])))
	}

	// Initializes the maps

	states := make(map[string]map[string]string)
	outputs := make(map[string]map[string]string)
	moves := make(map[string]map[string]int)

	// Reads the input file and compiles the code into the maps

	f, err := os.Open(fname)
	if err != nil {
    	log.Fatal(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		raw := string(strings.Split(strings.ToLower(scanner.Text()), "#")[0])
		if(pattern.MatchString(raw)){
	    	line:=strings.Split(strings.Replace(strings.Replace(raw, "(", "", -1), ")", "", -1), ",")
    		line[1]=expandRanges(line[1])
    		line[3]=expandRanges(line[3])

    		if len(line[1]) != len(line[3]) && len(line[3]) != 1{
    			fmt.Println("Error: invalid input-output")
    			return
    		}


    		for j := 0; j<len(line[1]); j++{
    			if _, ok := states[string(line[0])]; !ok {
    				states[string(line[0])] = make(map[string]string)
    				outputs[string(line[0])] = make(map[string]string)
	    			moves[string(line[0])] = make(map[string]int)
				}
	    		states[string(line[0])][string(line[1][j])]=string(line[2])
	    		outputs[string(line[0])][string(line[1][j])]=string(line[3][j%len(line[3])])
	    		mv := strings.Replace(string(line[4]), " ", "", -1)
	    		if mv=="<"{
	    			moves[string(line[0])][string(line[1][j])]=-1
	    		}else if mv == "-"{
	    			moves[string(line[0])][string(line[1][j])]=0
	    		}else if mv == ">"{
	    			moves[string(line[0])][string(line[1][j])]=1
	    		}else{
	    			fmt.Print("Error: invalid movement ")
	    			fmt.Println(line[4])
	    			return
	    		}
	    	}
	    }
	}


	// Main loop

	runnable := true

	for runnable{
		val := string(strings.Replace(tape[index], " ", "-", -1))
		if _, ok := states[string(state)][val]; ok{ // Checks if the state the machine is in is possible

			// Gets updates
			newState := states[string(state)][val]
			newIndex := index + moves[string(state)][val]
			newText := outputs[string(state)][val]

			tape[index]=newText
			index=newIndex
			if index < 0{
				index++
				tape=append([]string{"-"}, tape...)
			}
			if index >= len(tape){
				tape=append(tape, " ")
			}
			state=newState
		}else{
			runnable = false
		}
		ptape(tape, index, state, moves[string(state)][val])
		time.Sleep(time.Duration(ms) * time.Millisecond)
	}



	fmt.Println();
}